from typing import List


class HttpRequest:
    def __init__(self, recv: bytes):
        self.recv = recv
        meta = recv.decode("utf-8").split("\n")
        self.request_line = HttpRequestLine(meta[0])
        self.header = HttpRequestHeader(meta[1:])

    def __str__(self) -> str:
        return self.recv.decode("utf-8")

    def as_bytes(self) -> bytes:
        return self.recv

    @property
    def path(self):
        if self.request_line.path == "/":
            return "/index.html"
        return self.request_line.path


class HttpRequestLine:
    def __init__(self, raw: str):
        self.method, self.path, self.protocol = raw.split(" ")


class HttpRequestHeader:
    def __init__(self, raw: List[str]):
        self._data = {}
        for item in raw:
            try:
                key, value = item.split(": ")
                self._data[key] = value
            except Exception:
                print(item)

    @property
    def host(self):
        return self._data["Host"]
