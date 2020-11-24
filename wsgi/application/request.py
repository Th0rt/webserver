from cgi import FieldStorage
from typing import Any, Dict, Optional


class HttpRequest:
    def __init__(self, env: Dict[str, Any]) -> None:
        self.env = env

    @property
    def path(self) -> str:
        return self.env["PATH_INFO"]

    @property
    def request_method(self) -> str:
        return self.env["REQUEST_METHOD"]

    @property
    def query_string(self) -> Dict[str, str]:
        qs = self.env["QUERY_STRING"].split("&")
        return {q[0]: q[2] for q in qs}

    @property
    def cookie(self) -> Optional[Dict[str, str]]:
        cookie = {}
        if "HTTP_Cookie" in self.env:
            for c in self.env["HTTP_Cookie"].split("; "):
                key, value = c.split("=")
                cookie[key] = value
        return cookie

    @property
    def request_body(self) -> Dict[str, str]:
        headers = {
            "content-type": self.env["CONTENT_TYPE"],
            "content-length": self.env["CONTENT_LENGTH"],
        }
        fs = FieldStorage(
            fp=self.env["wsgi.input"],
            headers=headers,
            environ={"REQUEST_METHOD": "POST"},
        )
        return {f.name: f.value for f in fs.list}

    def as_dict(self) -> Dict[str, Any]:
        return self.env
