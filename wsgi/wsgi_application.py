import os
from typing import Callable, Iterable, List
from datetime import datetime

DOCUMENT_ROOT = "./resource/server"

MIME_TYPES = {
    ".txt": b"text/plain",
    ".html": b"text/html",
    ".css": b"text/css",
    ".js": b"text/javascript",
}


class WSGIApplication:
    def __init__(self):
        self.env = {}

    def application(self, env: dict, start_response: Callable) -> Iterable[bytes]:
        self.env = env
        content, content_type = self.get_content()
        start_response(b"200 OK", [(b"Content-type", content_type)])
        return content

    def get_content(self) -> (List[bytes], bytes):
        path = self.env[b"PATH_INFO"].decode("utf-8")

        print(f"requested resource is {DOCUMENT_ROOT} {path}")

        if path == "/":
            path = "/index.html"

        if path == "/now.html":
            with open(os.path.join(DOCUMENT_ROOT, "now.html"), "wb") as f:
                f.writelines([datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode('utf-8')])
        elif path == "/header.html":
            with open(os.path.join(DOCUMENT_ROOT, "header.html"), "wb") as f:
                f.writelines([b"%s: %s<br>\n" % (key, value) for key, value in self.env.items()])

        with open(DOCUMENT_ROOT + path, "rb") as f:
            content = f.readlines()
            content_type = MIME_TYPES[os.path.splitext(f.name)[-1]]

        return content, content_type
