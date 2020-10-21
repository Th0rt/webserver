
from ..request import HttpRequest, HttpRequestLine, HttpRequestHeader

class TestHttpRequest:
    recv = b"\n".join([
        b"GET /favicon.ico HTTP/1.1",
        b"Host: localhost:8090",
        b"Connection: keep-alive",
        b"Pragma: no-cache",
        b"Cache-Control: no-cache",
        b"User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        b"Accept: image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        b"Sec-Fetch-Site: same-origin",
        b"Sec-Fetch-Mode: no-cors",
        b"Sec-Fetch-Dest: image",
        b"Referer: http://localhost:8090/",
        b"Accept-Encoding: gzip, deflate, br",
        b"Accept-Language: ja,en-US;q=0.9,en;q=0.8",
        b"",
    ])

    def test_init(self):
        req = HttpRequest(self.recv)
        assert req.request_line.method == b"GET"
        assert req.header.host == b"localhost:8090"


class TestHttpRequestLine:
    def test_main(self):
        line = HttpRequestLine(b"GET /favicon.ico HTTP/1.1")
        assert line.method == b"GET"
        assert line.path == b"/favicon.ico"
        assert line.protocol == b"HTTP/1.1"


class TestHttpRequestHeader:
    def test_main(self):
        header = HttpRequestHeader([
            b"Host: localhost:8090",
            b"Connection: keep-alive",
            b"Pragma: no-cache",
            b"Cache-Control: no-cache",
            b"User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            b"Accept: image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            b"Sec-Fetch-Site: same-origin",
            b"Sec-Fetch-Mode: no-cors",
            b"Sec-Fetch-Dest: image",
            b"Referer: http://localhost:8090/",
            b"Accept-Encoding: gzip, deflate, br",
            b"Accept-Language: ja,en-US;q=0.9,en;q=0.8",
        ])
        assert header.host == b"localhost:8090"
