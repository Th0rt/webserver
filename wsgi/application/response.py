from typing import Iterable, Tuple, Dict, List

from .settings import MIME_TYPES


class HttpResponseBase:
    def __init__(
        self, content: Iterable[bytes], status_code: str, content_type: str, header: Dict[str, str] = {}
    ) -> None:
        self.content = content
        self.status_code = status_code
        self.content_type = content_type
        self.header = header

    def header_as_bytes(self) -> List[Tuple[bytes, bytes]]:
        h = []
        h.append((b"Content-type", self.content_type.encode("utf-8")))
        for key, value in self.header.items():
            h.append((key.encode("utf-8"), value.encode("utf-8")))
        return h

    def output(self) -> Tuple[bytes, List[Tuple[bytes, bytes]], Iterable[bytes]]:
        return (
            self.status_code.encode("utf-8"),
            self.header_as_bytes(),
            self.content
        )


class HttpResponse(HttpResponseBase):
    def __init__(
        self, content: Iterable[bytes], content_type: str, status_code: str = "200 OK", header: Dict[str, str]= {}
    ) -> None:
        super().__init__(content, status_code, content_type, header)


class HttpResponse404(HttpResponseBase):
    def __init__(self) -> None:
        super().__init__([b"404 Not Found"], "404", MIME_TYPES[".html"])


class HttpResponse405(HttpResponseBase):
    def __init__(self) -> None:
        super().__init__([b"405 Not Allowed"], "405", MIME_TYPES[".html"])
