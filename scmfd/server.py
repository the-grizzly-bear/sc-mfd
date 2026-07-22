import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .inject import VirtualKeyboard


class _Handler(SimpleHTTPRequestHandler):
    keyboard: VirtualKeyboard

    def do_POST(self) -> None:
        if self.path.rstrip("/") != "/inject":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        commands = json.loads(self.rfile.read(length) or b"{}").get("commands", [])
        self.keyboard.run(commands)
        self.send_response(204)
        self.end_headers()

    def log_message(self, *args) -> None:
        pass


def serve(webroot: Path, keyboard: VirtualKeyboard, port: int) -> None:
    _Handler.keyboard = keyboard
    handler = partial(_Handler, directory=str(webroot))
    ThreadingHTTPServer(("0.0.0.0", port), handler).serve_forever()
