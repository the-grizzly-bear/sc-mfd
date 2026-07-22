import json
import shutil
from html import escape
from pathlib import Path
from urllib.parse import quote

from .model import Panel, Button

_VERSION = "5"


def _file(name: str) -> str:
    return "index.html" if name == "Main" else f"{name}.html"


def _nav(name: str) -> str:
    return "__prev__" if name == "Previous" else _file(name)


def _button(b: Button) -> str:
    src = "img/" + quote(b.img)
    style = f"left:{b.x*100:.3f}%;top:{b.y*100:.3f}%;width:{b.w*100:.3f}%;height:{b.h*100:.3f}%"
    if b.axis:
        return (f'<input type="range" class="slider" min="-1" max="1" step="0.01" value="0" '
                f'data-axis="{escape(b.axis)}" style="{style};background-image:url({escape(src)})">')
    attrs = ['class="btn"', f'style="{style}"', f'src="{escape(src)}"', f'data-up="{escape(src)}"']
    if b.down:
        attrs.append(f'data-down="img/{quote(b.down)}"')
    if b.press:
        attrs.append(f"data-press='{json.dumps(b.press)}'")
    if b.release:
        attrs.append(f"data-release='{json.dumps(b.release)}'")
    if b.nav:
        attrs.append(f'data-nav="{_nav(b.nav)}"')
    if b.toggle:
        attrs.append(f'data-toggle="{escape(b.toggle)}"')
    return f"<img {' '.join(attrs)} alt=\"\">"


def _page(panel: Panel) -> str:
    buttons = "\n".join(_button(b) for b in panel.buttons)
    return _PAGE.format(title=escape(panel.name), buttons=buttons, v=_VERSION)


def build(panels: list[Panel], assets_img: Path, out: Path) -> None:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(assets_img, out / "img")
    for panel in panels:
        (out / _file(panel.name)).write_text(_page(panel))
    (out / "style.css").write_text(_CSS)
    (out / "mfd.js").write_text(_JS)
    (out / "manifest.webmanifest").write_text(json.dumps({
        "name": "SC-MFD", "short_name": "SC-MFD", "start_url": "index.html",
        "display": "fullscreen", "orientation": "landscape",
        "background_color": "#05070a", "theme_color": "#05070a",
    }))


_PAGE = """<!doctype html><html><head><meta charset="utf-8">
<title>SC-MFD - {title}</title>
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#05070a">
<link rel="manifest" href="manifest.webmanifest">
<link rel="stylesheet" href="style.css?v={v}"></head>
<body><div id="stage">
{buttons}
</div><script src="mfd.js?v={v}"></script></body></html>"""

_CSS = """
* { box-sizing:border-box; -webkit-tap-highlight-color:transparent; }
html,body { margin:0; height:100%; background:#000; overflow:hidden;
  user-select:none; -webkit-user-select:none; touch-action:manipulation; }
#stage { position:relative; width:100vw; height:100vh; max-width:177.78vh;
  margin:0 auto; background:#05070a; aspect-ratio:16/9; }
.btn { position:absolute; transform:translate(-50%,-50%); object-fit:contain; cursor:pointer; }
.btn:active { filter:brightness(1.4); }
.slider { position:absolute; transform:translate(-50%,-50%); appearance:none; -webkit-appearance:none;
  background:center/100% 60% no-repeat; outline:none; }
.slider::-webkit-slider-thumb { -webkit-appearance:none; width:1.5%; height:120%; background:#e8eef4; border-radius:1px; }
.slider::-moz-range-thumb { width:1.5%; height:120%; background:#e8eef4; border:none; border-radius:1px; }
"""

_JS = """
function inj(c){ if(c&&c.length) fetch('/inject',{method:'POST',
  headers:{'Content-Type':'application/json'},body:JSON.stringify({commands:c})}).catch(function(){}); }
var stack=[location.pathname.split('/').pop()||'index.html'];
function load(url,push){ fetch(url).then(function(r){return r.text();}).then(function(t){
  var s=new DOMParser().parseFromString(t,'text/html').querySelector('#stage'); if(!s) return;
  document.querySelector('#stage').replaceWith(s); if(push) stack.push(url); bind(); fs(); }).catch(function(){}); }
function back(){ if(stack.length>1) stack.pop(); load(stack[stack.length-1],false); }
var T={};
function setGroup(g){ document.querySelectorAll('.btn[data-toggle="'+g+'"]').forEach(function(x){
  x.src=T[g]?x.getAttribute('data-down'):x.getAttribute('data-up'); }); }
function held(cmds){ var s={},o=[]; cmds.forEach(function(c){
  if(c.type==='down'){ if(!(c.value in s))o.push(c.value); s[c.value]=(s[c.value]||0)+1; }
  else if(c.type==='up') s[c.value]=(s[c.value]||0)-1; });
  return o.filter(function(k){return s[k]>0;}).reverse(); }
function bind(){ document.querySelectorAll('.btn').forEach(function(b){ if(b._b) return; b._b=1;
  var nav=b.getAttribute('data-nav'), rel=b.getAttribute('data-release'),
      up=b.getAttribute('data-up'), down=b.getAttribute('data-down'), tg=b.getAttribute('data-toggle');
  var pc=b.getAttribute('data-press'); pc=pc?JSON.parse(pc):null;
  b.addEventListener('pointerdown',function(e){ e.preventDefault(); if(navigator.vibrate)navigator.vibrate(30);
    if(pc)inj(pc); if(tg){ T[tg]=!T[tg]; setGroup(tg); } else if(down) b.src=down; });
  var release=function(){ if(rel)inj(JSON.parse(rel));
    if(pc){ var h=held(pc); if(h.length)inj(h.map(function(k){return{type:'up',value:k};})); }
    if(!tg&&up)b.src=up; };
  ['pointerup','pointerleave','pointercancel'].forEach(function(ev){ b.addEventListener(ev,release); });
  if(nav) b.addEventListener('click',function(){ var go=function(){ nav==='__prev__'?back():load(nav,true); };
    (pc||rel)?setTimeout(go,150):go(); }); });
  Object.keys(T).forEach(setGroup);
  document.querySelectorAll('.slider').forEach(function(s){ if(s._b) return; s._b=1;
    s.addEventListener('input',function(){ inj([{type:'axis',value:s.value}]); }); }); }
bind();
var fsbtn=document.createElement('div'); fsbtn.textContent='\\u26F6';
fsbtn.style.cssText='position:fixed;top:4px;right:4px;z-index:9;font-size:24px;color:#9a9a9a;'
  +'background:#000a;padding:2px 10px;border-radius:8px;cursor:pointer;';
fsbtn.addEventListener('click',function(e){ e.stopPropagation(); var el=document.documentElement;
  document.fullscreenElement ? document.exitFullscreen() : (el.requestFullscreen&&el.requestFullscreen()); });
document.body.appendChild(fsbtn);
function fs(){ fsbtn.style.display=(stack[stack.length-1]==='index.html'&&!document.fullscreenElement)?'block':'none'; }
document.addEventListener('fullscreenchange',fs); fs();
"""
