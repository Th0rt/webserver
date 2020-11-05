import os
from typing import Callable, Iterable, List, Tuple
from .settings import DOCUMENT_ROOT, MIME_TYPES
from .route import Route
from .request import HttpRequest


class WSGIApplication:
    def application(self, env: dict, start_response: Callable) -> Iterable[bytes]:
        self.request = HttpRequest(env)
        content, content_type = self.get_content()
        start_response(b"200 OK", [(b"Content-type", content_type)])
        return content

    def get_content(self):
        filename, ext = os.path.splitext(self.request.path)
        print(filename, ext)

        if ext in ("", "html"):
            return self.get_html()
        else:
            return self.get_static(filename + ext)

    def get_static(self, filename: str) -> Tuple[Iterable[bytes], bytes]:
        with open(DOCUMENT_ROOT + filename, "rb") as f:
            content = f.readlines()
            content_type = MIME_TYPES[os.path.splitext(f.name)[-1]]

        return (content, content_type)

    def get_html(self) -> Tuple[Iterable[bytes], bytes]:
        view_cls = Route(self.request.path).get_view()
        return view_cls(self.request).get_response()
