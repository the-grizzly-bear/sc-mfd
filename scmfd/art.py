import re
import shutil
from pathlib import Path

import numpy as np
from PIL import Image

from . import model


_NAV = ("NAV", "MOBI", "HOME", "BACK", "CMBT")


def _role(name: str) -> str:
    if any(t in name for t in _NAV) or re.search(r"_(L|R)$", name):
        return "nav"
    if "YLW" in name:            # covers YLW and YLW_ACT; substring-safe (not "ACT" in FRACTURE)
        return "critical" if "RED" in name else "caution"
    if "RED" in name:
        return "critical"
    if name.endswith("OFF"):
        return "dim"
    return "primary"


def _rgb(h: str) -> tuple[int, int, int]:
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def _recolor(stencil: Path, color) -> Image.Image:
    la = np.array(Image.open(stencil).convert("LA"))
    g = la[:, :, 0:1].astype(np.float32) / 255
    out = np.dstack([(g * color).astype(np.uint8), la[:, :, 1]])
    return Image.fromarray(out, "RGBA")


def render(mfds: Path, palettes: dict, assets_img: Path) -> None:
    import json
    pal = json.loads(Path(palettes).read_text()) if not isinstance(palettes, dict) else palettes
    stencils, fixed = assets_img.parent / "stencils", assets_img.parent / "fixed"
    refs = {img for panel in model.load_panels(mfds) for b in panel.buttons
            for img in (b.img, b.down) if img}
    if assets_img.exists():
        shutil.rmtree(assets_img)
    for rel in refs:
        folder, fn = rel.split("/", 1)
        name = fn[:-4]
        dst = assets_img / folder / fn
        dst.parent.mkdir(parents=True, exist_ok=True)
        if (fixed / rel).exists():
            shutil.copyfile(fixed / rel, dst)
        else:
            key = re.sub(r"^[A-Z]{3}_", "", name)
            _recolor(stencils / f"{key}.png", _rgb(pal[folder][_role(name)])).save(dst)
