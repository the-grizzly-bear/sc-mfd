import argparse
from pathlib import Path

from . import model, site

ROOT = Path(__file__).resolve().parents[1]
MFDS = ROOT / "config" / "mfds"
ASSETS = ROOT / "assets" / "img"
WEBROOT = ROOT / "webroot"


def art() -> None:
    import json
    from . import art as art_module
    art_module.render(MFDS, json.loads((ROOT / "config" / "palettes.json").read_text()), ASSETS)
    print(f"generated art -> {ASSETS}")


def build() -> None:
    if not ASSETS.exists() or not any(ASSETS.iterdir()):
        art()
    panels = model.load_panels(MFDS)
    site.build(panels, ASSETS, WEBROOT)
    print(f"built {len(panels)} panels -> {WEBROOT}")


def serve(port: int | None) -> None:
    from .inject import VirtualKeyboard
    from .server import serve as run
    build()
    with VirtualKeyboard() as keyboard:
        for p in ([port] if port else [80, 8080]):
            try:
                print(f"serving on :{p}")
                run(WEBROOT, keyboard, p)
                return
            except (PermissionError, OSError):
                continue
        raise SystemExit("could not bind :80 or :8080 (try --port)")


def main() -> None:
    parser = argparse.ArgumentParser(prog="scmfd")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("art")
    sub.add_parser("build")
    sub.add_parser("serve").add_argument("--port", type=int)
    args = parser.parse_args()
    if args.cmd == "art":
        art()
    elif args.cmd == "build":
        build()
    elif args.cmd == "serve":
        serve(args.port)
