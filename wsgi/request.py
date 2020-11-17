from typing import List, Dict
from io import BytesIO


class HttpRequest:
    def __init__(self, recv: bytes):
        self.recv = recv
        self._data = {}

        r = recv.split(b"\r\n\r\n", 1)
        header = r[0].decode("utf-8").split("\r\n")
        body = r[1]

        # get request body
        self._data["wsgi.input"] = BytesIO(body)

        # get request line
        method, path, _ = header[0].split(" ")

        self._data["REQUEST_METHOD"] = method

        if "?" in path:
            p = path.split("?", 1)
            self._data["PATH_INFO"] = p[0]
            self._data["QUERY_STRING"] = p[1]
        else:
            self._data["PATH_INFO"] = path
            self._data["QUERY_STRING"] = ""

        # get request header
        for item in header[1:]:
            key, value = item.split(": ", 1)

            if key == "Content-Type":
                self._data["CONTENT_TYPE"] = value
            if key == "Content-Length":
                self._data["CONTENT_LENGTH"] = value
            else:
                self._data[f"HTTP_{key}"] = value

        self._data["SCRIPT_NAME"] = ""
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
