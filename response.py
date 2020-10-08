from datetime import datetime


class HttpRequestHeader:
    def __init__(self, raw: str):
        self.raw = raw
        self.method, self._path, self.protocol = self.raw.split(" ")

    @property
    def path(self) -> str:
        return self._path

    def __str__(self):
        return self.raw


class HttpResponse:
    server_name = "Modoki"
    server_version = "1"

    def __init__(self, body: bytes):
        self.header = HttpResponseHeader(self.server_name, self.server_version)
        self.body = body
    def __init__(self, content: bytes, content_type: str):
        self.header = HttpResponseHeader(content_type)
        self.content = content

    def as_bytes(self) -> bytes:
        return self.header.as_bytes() + b"\n\n" + self.content


class HttpResponseHeader:
    def __init__(self, server_name: str, server_version: str):
        self.server_name = f"{server_name}/{server_version}"

    @property
    def http_method(self) -> str:
        return "HTTP/1.1"

    @property
    def status_code(self) -> str:
        return "200 OK"

    @property
    def connection(self) -> str:
        return "Close"

    @property
    def response_datetime(self) -> str:
        return datetime.now().strftime("%a, %d %b %Y %H:%M:%S")

    def __str__(self) -> str:
        return "\n".join([
            f"{self.http_method} {self.status_code}",
            f"Server: {self.server_name}",
            f"Date: {self.response_datetime} GMT",
            f"Content-Type: {self.content_type}",
            f"Connection: {self.connection}",
        ])

    def as_bytes(self) -> bytes:
        return str(self).encode("utf-8")
