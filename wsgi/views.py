from abc import ABC
from cgi import FieldStorage
from datetime import datetime
from io import BytesIO
from typing import List, Tuple

from .settings import DOCUMENT_ROOT, MIME_TYPES


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
        raise ValueError("GET is not allowed.")

    def post(self, *args, **kwargs) -> Tuple[List[bytes], bytes]:
        raise ValueError("POST is not allowed.")


class IndexView(ViewBase):
    def get(self, *args, **kwargs) -> Tuple[List[bytes], bytes]:
        with open(os.path.join(DOCUMENT_ROOT + "/index.html"), "rb") as f:
            content = f.readlines()
            content_type = MIME_TYPES[".html"]

        return (content, content_type)


class NowView(ViewBase):
    def get(self, *args, **kwargs) -> Tuple[List[bytes], bytes]:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode("utf-8")
        return (BytesIO(now), MIME_TYPES[".html"])


class HeaderView(ViewBase):
    def get(self, *args, **kwargs) -> Tuple[List[bytes], bytes]:
        content = "<br>".join([f"{key}: {value}" for key, value in self.env.items()])
        return (BytesIO(content.encode("utf-8")), MIME_TYPES[".html"])


class ParametersView(ViewBase):
    def get(self, *args, **kwargs) -> Tuple[List[bytes], bytes]:
        qs = self.env["QUERY_STRING"].split("&")
        content = BytesIO("<br>".join(qs).encode("utf-8"))
        content_type = MIME_TYPES[".html"]
        return (content, content_type)

    def post(self, *args, **kwargs) -> Tuple[List[bytes], bytes]:
        headers = {
            "content-type": self.env["CONTENT_TYPE"],
            "content-length": self.env["CONTENT_LENGTH"],
        }
        fs = FieldStorage(
            fp=self.env["wsgi.input"],
            headers=headers,
            environ={"REQUEST_METHOD": "POST"},
        )
        res = "<br>".join([f"{f.name}: {f.value}" for f in fs.list])
        return (BytesIO(res.encode("utf-8")), MIME_TYPES[".html"])
