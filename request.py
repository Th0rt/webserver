from typing import List


class HttpRequest:
    def __init__(self, recv: bytes):
        self.recv = recv
        raw_header, raw_body = recv.decode("utf-8").split("\n\n")

        meta = raw_header.split("\n")
        self.request_line = HttpRequestLine(meta[0])
        self.header = HttpRequestHeader(meta[1:])
        self.body = raw_body

    def __str__(self) -> str:
        return self.recv.decode("utf-8")

    def as_bytes(self) -> bytes:
        return self.recv


class HttpRequestLine:
    def __init__(self, raw: str):
        self.method, self.path, self.protocol = raw.split(" ")


class HttpRequestHeader:
    def __init__(self, raw: List[str]):
        self._data = {}
        for item in raw:
            key, value = item.split(": ")
            self._data[key] = value

    @property
    def host(self):
        return self._data["Host"]



