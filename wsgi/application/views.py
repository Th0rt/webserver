import os
from abc import ABC
from datetime import datetime
from io import BytesIO
from typing import List, Tuple, Iterable

from .settings import DOCUMENT_ROOT, MIME_TYPES
from .request import HttpRequest


class ViewBase(ABC):
    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def get_response(self, *args, **kwargs) -> Tuple[Iterable[bytes], bytes]:
        if self.request.request_method == "GET":
            return self.get(args, kwargs)
        elif self.request.request_method == "POST":
            return self.post(args, kwargs)
        else:
            raise ValueError(f"{self.request.request_method} is not allowed.")

    def get(self, *args, **kwargs) -> Tuple[Iterable[bytes], bytes]:
        raise ValueError("GET is not allowed.")

    def post(self, *args, **kwargs) -> Tuple[Iterable[bytes], bytes]:
        raise ValueError("POST is not allowed.")


class IndexView(ViewBase):
    def get(self, *args, **kwargs) -> Tuple[List[bytes], bytes]:
        with open(os.path.join(DOCUMENT_ROOT + "/index.html"), "rb") as f:
            content = f.readlines()
            content_type = MIME_TYPES[".html"]

        return (content, content_type)


class NowView(ViewBase):
    def get(self, *args, **kwargs) -> Tuple[Iterable[bytes], bytes]:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode("utf-8")
        return (BytesIO(now), MIME_TYPES[".html"])


class HeaderView(ViewBase):
    def get(self, *args, **kwargs) -> Tuple[Iterable[bytes], bytes]:
        return (
            BytesIO(str(self.request.as_dict()).encode("utf-8")),
            MIME_TYPES[".html"],
        )


class ParametersView(ViewBase):
    def get(self, *args, **kwargs) -> Tuple[Iterable[bytes], bytes]:
        content = BytesIO(str(self.request.query_string).encode("utf-8"))
        content_type = MIME_TYPES[".html"]
        return (content, content_type)

    def post(self, *args, **kwargs) -> Tuple[Iterable[bytes], bytes]:
        return (
            BytesIO(str(self.request.request_body).encode("utf-8")),
            MIME_TYPES[".html"],
        )
