import os
from typing import Callable, Iterable, List, Tuple
from datetime import datetime
from abc import ABC, abstractmethod
from io import BytesIO

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

    def get_content(self):
        filename, ext = os.path.splitext(self.env["PATH_INFO"])
        print(filename, ext)

        if ext in ("", "html"):
            return self.get_html()
        else:
            return self.get_static(filename + ext)

    def get_static(self, filename: str) -> Tuple[List[bytes], bytes]:
        with open(DOCUMENT_ROOT + filename, "rb") as f:
            content = f.readlines()
            content_type = MIME_TYPES[os.path.splitext(f.name)[-1]]

        return (content, content_type)


    def get_html(self) -> Tuple[List[bytes], bytes]:
        path = self.env["PATH_INFO"]

        print(f"requested resource is {DOCUMENT_ROOT} {path}")

        if path == "/":
            return IndexView(self.env).dispath()

        if path == "/now.html":
            with open(os.path.join(DOCUMENT_ROOT, "now.html"), "wb") as f:
                f.writelines([datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode('utf-8')])
        elif path == "/header.html":
            with open(os.path.join(DOCUMENT_ROOT, "header.html"), "wb") as f:
                f.writelines([f"{key}: {value}<br>\n" for key, value in self.env.items()])
        elif path == "/parameters":
            with open(os.path.join(DOCUMENT_ROOT, "parameters.html"), "w") as f:
                if self.env["REQUEST_METHOD"] == "GET":
                    content = self.env["QUERY_STRING"].split("&")
                    f.write("<br>".join(content))
                elif self.env["REQUEST_METHOD"] == "POST":
                    content = self.env["wsgi.input"]
                    f.write(b"<br>".join(content.getvalue().split(b"\r\n")))
        with open(DOCUMENT_ROOT + path + ".html", "rb") as f:
            content = f.readlines()
            content_type = MIME_TYPES[os.path.splitext(f.name)[-1]]

        return content, content_type

class ViewBase(ABC):
    def __init__(self, env: dict) -> None:
        self.env = env

    def dispath(self, *args, **kwargs) -> callable:
        if self.env["REQUEST_METHOD"] == "GET":
            return self.get(args, kwargs)
        elif self.env["REQUEST_METHOD"] == "POST":
            return self.post(args, kwargs)
        else:
            raise ValueError(f'{self.env["REQUEST_METHOD"]} is not allowed.')

    def get(self, *args, **kwargs) -> Tuple[List[bytes], bytes]:
        raise ValueError("POST is not allowed.")

    def post(self, *args, **kwargs) -> Tuple[List[bytes], bytes]:
        raise ValueError("POST is not allowed.")


class IndexView(ViewBase):
    def get(self, *args, **kwargs) -> Tuple[List[bytes], bytes]:
        with open(os.path.join(DOCUMENT_ROOT + "/index.html"), "rb") as f:
            content = f.readlines()
            content_type = MIME_TYPES[".html"]

        return (content, content_type)

