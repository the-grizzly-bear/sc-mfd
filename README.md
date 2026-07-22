# scmfd

Touchscreen MFD for Star Citizen. Panels are JSON; a tablet browser drives the
game over a uinput virtual keyboard, which reaches it under Wayland where
synthetic X11 input does not. Button art is generated from per-manufacturer
palettes.

    scmfd art            # config/palettes.json + assets/ -> assets/img/
    scmfd build          # config/mfds/*.json + art -> webroot/
    scmfd serve [--port] # build, then serve and inject

`serve` needs `/dev/uinput` writable. For `:80` as a normal user, set
`net.ipv4.ip_unprivileged_port_start=80`, otherwise `--port 8080`.

## Screenshots

![Main panel](docs/main-panel.jpg)

![Anvil panel](docs/anvil-panel.jpg)

## Panels

`config/mfds/<name>.json` — buttons over a 16:9 stage; coordinates are fractions
from the top-left.

```json
{
  "name": "Anvil",
  "buttons": [
    { "img": "Anvil Hornet/ANV_GEAR_OFF.png", "x": 0.14, "y": 0.85, "w": 0.13, "h": 0.09,
      "down": "Anvil Hornet/ANV_GEAR_ON.png", "toggle": "n",
      "press": [{ "type": "press", "value": "n" }] },
    { "img": "Anvil Hornet/ANV_NAV_R.png", "x": 0.86, "y": 0.95, "w": 0.1, "h": 0.08,
      "nav": "Aegis" }
  ]
}
```

A button injects keys, navigates (`nav`, or `"Previous"`), or both.

- **`press`** — commands run on touch; `release` runs on lift. A command is
  `{"type": "down"|"up"|"press"|"delay", "value": "<key|ms>", "modifier"?: "<key>"}`.
  Keys left held by `down` are auto-released on lift. Key names: `scmfd/keymap.py`.
- **`down`** — image shown while pressed / toggled on.
- **`toggle`** — a group id; tapping flips a persistent on/off state shared by
  every button with the same id, so linked buttons light together.

## Art

Buttons are generated, not stored. `scmfd art` recolors grayscale shape stencils
(`assets/stencils/`) with a per-manufacturer palette (`config/palettes.json`) into
`assets/img/`. Art that can't be recolored from a shape — logos, banners, sliders —
lives in `assets/fixed/`.
