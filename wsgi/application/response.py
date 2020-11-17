from typing import Iterable, Tuple

from .settings import MIME_TYPES


class HttpResponseBase:
    def __init__(
        self, content: Iterable[bytes], status_code: str, content_type: str
    ) -> None:
        self.content = content
        self.status_code = status_code
        self.content_type = content_type

    def output(self) -> Tuple[bytes, Iterable[bytes], bytes]:
        return (
            self.status_code.encode("utf-8"),
            self.content,
            self.content_type.encode("utf-8"),
        )


class HttpResponse(HttpResponseBase):
    def __init__(
        self, content: Iterable[bytes], content_type: str, status_code: str = "200 OK"
    ) -> None:
        super().__init__(content, status_code, content_type)


class HttpResponse404(HttpResponseBase):
    def __init__(self) -> None:
        super().__init__([b"404 Not Found"], "404", MIME_TYPES[".html"])
