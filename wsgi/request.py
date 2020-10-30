from typing import List, Dict
from io import BytesIO
from ast import literal_eval


class HttpRequestLine:
    def __init__(self, raw: bytes):
        r = raw.split(b" ")
        self.method = r[0]
        self.path = r[1]
        self.protocol = r[2]


class HttpRequestHeader:
    def __init__(self, raw: List[str]):
        self._data = {}

        x, y, _ = raw[0].split(" ")
        self._data["REQUEST_METHOD"] = x
        self._data["PATH_INFO"] = y
        self._data["SCRIPT_NAME"] = ""
        self._data["QUERY_STRING"] = ""
        self._data["SERVER_NAME"] = ""
        self._data["SERVER_PORT"] = ""
        self._data["SERVER_PROTOCOL"] = ""

        for item in raw[1:]:
            i = item.split(": ", 1)
            print(i)
            key = i[0]
            value = i[1]


            if key == "Content-type":
                self._data["CONTENT_TYPE"] = value
            if key == "Content-length":
                self._data["CONTENT_LENGTH"] = value
            else:
                self._data[f"HTTP_{key}"] = value

    @property
    def host(self):
        return self._data["Host"]

    def as_dict(self):
        return self._data


class HttpRequest:
    def __init__(self, recv: bytes):
        self.recv = recv

        header, body = recv.split(b"\r\n\r\n", 1)

        self.header = HttpRequestHeader(header.decode("utf-8").split("\r\n"))
        self.body = BytesIO(body)

    def __str__(self) -> str:
        return self.recv.decode("utf-8")

    def as_bytes(self) -> bytes:
        return self.recv


    @property
    def path(self):
        if self.request_line.path == "/":
            return "/index.html"
        return self.request_line.path

