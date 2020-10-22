from datetime import datetime
from abc import ABC, abstractmethod


class HttpRequestHeader:
    def __init__(self, raw: str):
        self.raw = raw
        self.method, self._path, self.protocol = self.raw.split(" ")

    @property
    def path(self) -> str:
        return self._path

    def __str__(self):
        return self.raw


class HttpResponseBase(ABC):
    def as_bytes(self) -> bytes:
        return self.header.encode("utf-8")

    @property
    def server_name(self) -> str:
        return "Modoki"

    @property
    def server_version(self) -> str:
        return "1"

    @property
    def http_method(self) -> str:
        return "HTTP/1.1"

    @property
    def status_code(self) -> str:
        raise NotImplementedError()

    @property
    def connection(self) -> str:
        return "Close"

    @property
    def response_datetime(self) -> str:
        return datetime.now().strftime("%a, %d %b %Y %H:%M:%S")

    @property
    def header(self) -> str:
        return "\n".join(
            [
                f"{self.http_method} {self.status_code}",
                f"Server: {self.server_name}",
                f"Date: {self.response_datetime} GMT",
                f"Connection: {self.connection}",
            ]
        )


class HttpResponse(HttpResponseBase):
    def __init__(self, content: bytes, content_type: str):
        super().__init__()
        self.content = content
        self.content_type = content_type

    @property
    def status_code(self) -> str:
        return "200 OK"

    @property
    def header(self) -> str:
        base = super().header
        return "\n".join([base, f"Content-Type: {self.content_type}"])

    def as_bytes(self) -> bytes:
        return b"\n\n".join([self.header.encode("utf-8"), self.content])


class HttpResponse404(HttpResponseBase):
    def __init__(self):
        super().__init__()

    @property
    def status_code(self) -> str:
        return "404 Not Found"
