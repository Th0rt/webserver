from typing import List


class HttpRequestLine:
    def __init__(self, raw: bytes):
        r = raw.split(b" ")
        self.method = r[0]
        self.path = r[1]
        self.protocol = r[2]


class HttpRequestHeader:
    def __init__(self, raw: List[bytes]):
        self._data = {}
        for item in raw:
            key, value = item.split(b": ")
            self._data[key] = value

    @property
    def host(self):
        return self._data[b"Host"]

    def as_dict(self) -> dict:
        return self._data


class HttpRequest:
    def __init__(self, recv: bytes):
        self.recv = recv

        r = recv.split(b"\r\n\r\n")
        header = r[0]
        if len(r) == 1:
            body = None
        elif len(r) == 2:
            body = r[1]
        else:
            raise Exception("Invalid Request.")

        h = header.splitlines()
        self.request_line = HttpRequestLine(h[0])
        self.header = HttpRequestHeader(h[1:])
        self.body = body

    def __str__(self) -> str:
        return self.recv.decode("utf-8")

    def as_bytes(self) -> bytes:
        return self.recv


    @property
    def path(self):
        if self.request_line.path == "/":
            return "/index.html"
        return self.request_line.path

