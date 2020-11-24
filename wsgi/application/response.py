from typing import Dict, Iterable, List, Tuple

from .settings import MIME_TYPES


class HttpResponseBase:
    def __init__(
        self,
        content: Iterable[bytes],
        status_code: str,
        content_type: str,
        header: Dict[str, str] = {},
        cookie: Dict[str, str] = {},
    ) -> None:
        self.content = content
        self.status_code = status_code
        self.content_type = content_type
        self.header = header
        self.cookie = cookie

    def header_as_bytes(self) -> List[Tuple[bytes, bytes]]:
        h = [
            HttpContentType(self.content_type).to_http(),
        ]
        cookies = [
            HttpCookie(f"{key}={value}").to_http() for key, value in self.cookie.items()
        ]
        h.extend(cookies)
        extra_header = [
            HttpHeader(key, value).to_http() for key, value in self.header.items()
        ]
        h.extend(extra_header)
        return h

    def output(self) -> Tuple[bytes, List[Tuple[bytes, bytes]], Iterable[bytes]]:
        return (self.status_code.encode("utf-8"), self.header_as_bytes(), self.content)


class HttpResponse(HttpResponseBase):
    def __init__(
        self,
        content: Iterable[bytes],
        content_type: str,
        status_code: str = "200 OK",
        header: Dict[str, str] = {},
        cookie: Dict[str, str] = {},
    ) -> None:
        super().__init__(content, status_code, content_type, header, cookie)


class HttpResponse404(HttpResponseBase):
    def __init__(self) -> None:
        super().__init__([b"404 Not Found"], "404", MIME_TYPES[".html"])


class HttpResponse405(HttpResponseBase):
    def __init__(self) -> None:
        super().__init__([b"405 Not Allowed"], "405", MIME_TYPES[".html"])


class HttpHeaderBase:
    def __init__(self, key: str, value: str) -> None:
        self.key = key
        self.value = value

    def to_http(self) -> Tuple[bytes, bytes]:
        return (self.key.encode("utf-8"), self.value.encode("utf-8"))


class HttpHeader(HttpHeaderBase):
    def __init__(self, key: str, value: str) -> None:
        self.key = key
        self.value = value


class HttpContentType(HttpHeaderBase):
    def __init__(self, value: str) -> None:
        self.key = "Content-Type"
        self.value = value


class HttpCookie(HttpHeaderBase):
    def __init__(self, value: str):
        self.key = "Set-Cookie"
        self.value = value
