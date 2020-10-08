
from ..request import HttpRequest, HttpRequestLine, HttpRequestHeader

class TestHttpRequest:
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
    ]).encode("utf-8")

    def test_init(self):
        req = HttpRequest(self.recv)
        assert req.request_line.method == "GET"
        assert req.header.host == "localhost:8090"


class TestHttpRequestLine:
    def test_main(self):
        line = HttpRequestLine("GET /favicon.ico HTTP/1.1")
        assert line.method == "GET"
        assert line.path == "/favicon.ico"
        assert line.protocol == "HTTP/1.1"


class TestHttpRequestHeader:
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
