from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path

Command = dict[str, str]


@dataclass(frozen=True)
class Button:
    img: str
    x: float
    y: float
    w: float
    h: float
    down: str | None = None
    press: list[Command] = field(default_factory=list)
    release: list[Command] = field(default_factory=list)
    nav: str | None = None
    axis: str | None = None
    toggle: str | None = None


@dataclass(frozen=True)
class Panel:
    name: str
    buttons: list[Button]


def load_panels(mfds_dir: Path) -> list[Panel]:
    panels = []
    for path in sorted(mfds_dir.glob("*.json")):
        spec = json.loads(path.read_text())
        panels.append(Panel(spec["name"], [Button(**b) for b in spec["buttons"]]))
    return panels
