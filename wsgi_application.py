import os
from typing import Callable, Iterable, List
import enum

DOCUMENT_ROOT = "./resource/server"

MIME_TYPES = {
    ".txt": b"text/plain",
    ".html": b"text/html",
    ".css": b"text/css",
    ".js": b"text/javascript"
}


class WSGIApplication:
    def __init__(self):
        self.env = {}

    def application(self, env: dict, start_response: Callable) -> Iterable[bytes]:
        self.env = env
        content, content_type = self.get_content()
        start_response(b'200 OK', [(b'Content-type', content_type)])
        return content

    def get_content(self) -> (List[bytes], bytes):
        path = self.env["PATH_INFO"]

        print(f"requested resource is {DOCUMENT_ROOT} {path}")

        if path == "/":
            path = "/index.html"

        print(path)

        with open(DOCUMENT_ROOT + path, "rb") as f:
            content = f.readlines()
            content_type = MIME_TYPES[os.path.splitext(f.name)[-1]]

        return content, content_type

