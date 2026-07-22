# scmfd

Touchscreen MFD for Star Citizen. Panels are declared as JSON; a tablet browser
drives the game over a uinput virtual keyboard, which reaches the game under
Wayland where synthetic X11 input does not.

    scmfd build          # config/mfds/*.json -> webroot/
    scmfd serve [--port]  # build, then serve and inject

`serve` needs `/dev/uinput` writable. For `:80` as a normal user, set
`net.ipv4.ip_unprivileged_port_start=80`, otherwise `--port 8080`.

## Screenshots

![Main panel](docs/main-panel.jpg)

![Anvil panel](docs/anvil-panel.jpg)

## Panel spec

`config/mfds/<name>.json` — buttons over a 16:9 stage, coordinates as fractions
from the top-left.

```json
{
  "name": "Anvil",
  "buttons": [
    { "img": "Anvil Hornet/ANV_GEAR_OFF.png", "x": 0.14, "y": 0.85, "w": 0.13, "h": 0.09,
      "press": [{ "type": "press", "value": "n" }] },
    { "img": "Anvil Hornet/ANV_NAV_R.png", "x": 0.86, "y": 0.95, "w": 0.08, "h": 0.08,
      "nav": "Aegis" }
  ]
}
```

A button injects keys (`press`/`release`), navigates (`nav`, or `"Previous"`), or
both. Commands are `{"type": "down"|"up"|"press"|"delay", "value": "<key|ms>"}`;
key names are in `scmfd/keymap.py`.
