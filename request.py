import json
import unittest
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


class TestHttpRequest(unittest.TestCase):
    recv = "\n".join([
        "GET /favicon.ico HTTP/1.1",
        "Host: localhost:8090",
        "Connection: keep-alive",
        "Pragma: no-cache",
        "Cache-Control: no-cache",
        "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Accept: image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        "Sec-Fetch-Site: same-origin",
        "Sec-Fetch-Mode: no-cors",
        "Sec-Fetch-Dest: image",
        "Referer: http://localhost:8090/",
        "Accept-Encoding: gzip, deflate, br",
        "Accept-Language: ja,en-US;q=0.9,en;q=0.8",
        "\n",
    ]).encode("utf-8")

    def test_init(self):
        req = HttpRequest(self.recv)
        assert req.request_line.method == "GET"
        assert req.header.host == "localhost:8090"


class TestHttpRequestLine(unittest.TestCase):
    def test_main(self):
        line = HttpRequestLine("GET /favicon.ico HTTP/1.1")
        assert line.method == "GET"
        assert line.path == "/favicon.ico"
        assert line.protocol == "HTTP/1.1"


class TestHttpRequestHeader(unittest.TestCase):
    def test_main(self):
        header = HttpRequestHeader([
            "Host: localhost:8090",
            "Connection: keep-alive",
            "Pragma: no-cache",
            "Cache-Control: no-cache",
            "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            "Accept: image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Sec-Fetch-Site: same-origin",
            "Sec-Fetch-Mode: no-cors",
            "Sec-Fetch-Dest: image",
            "Referer: http://localhost:8090/",
            "Accept-Encoding: gzip, deflate, br",
            "Accept-Language: ja,en-US;q=0.9,en;q=0.8",
        ])
        assert header.host == "localhost:8090"


if __name__ == '__main__':
    unittest.main()

