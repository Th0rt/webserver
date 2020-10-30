from typing import List, Dict
from io import BytesIO


class HttpRequest:
    def __init__(self, recv: bytes):
        self.recv = recv

        r = recv.split(b"\r\n\r\n", 1)
        header = r[0].decode("utf-8").split("\r\n")
        body = r[1]
        self._data = {}

        method, path, _ = header[0].split(" ")
        self._data["REQUEST_METHOD"] = method
        self._data["PATH_INFO"] = path
        self._data["wsgi.input"] = BytesIO(body)

        for item in header[1:]:
            key, value = item.split(": ", 1)

            if key == "Content-type":
                self._data["CONTENT_TYPE"] = value
            if key == "Content-length":
                self._data["CONTENT_LENGTH"] = value
            else:
                self._data[f"HTTP_{key}"] = value

        self._data["SCRIPT_NAME"] = ""
        self._data["QUERY_STRING"] = ""
        self._data["SERVER_NAME"] = ""
        self._data["SERVER_PORT"] = ""
        self._data["SERVER_PROTOCOL"] = ""

    def __str__(self) -> str:
        return self.recv.decode("utf-8")

    def get_data(self) -> Dict[str, str]:
        return self._data

    def as_bytes(self) -> bytes:
        return self.recv

    @property
    def path(self):
        if self.request_line.path == "/":
            return "/index.html"
        return self.request_line.path
