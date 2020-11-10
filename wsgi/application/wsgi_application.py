import os
from typing import Callable, Iterable

from .request import HttpRequest
from .response import HttpResponse, HttpResponse404, HttpResponseBase
from .route import Route
from .settings import DOCUMENT_ROOT, MIME_TYPES


class WSGIApplication:
    def application(self, env: dict, start_response: Callable) -> Iterable[bytes]:
        self.request = HttpRequest(env)
        status_code, content, content_type = self.get_content().output()
        start_response(status_code, [(b"Content-type", content_type)])
        return content

    def get_content(self) -> HttpResponseBase:
        filename, ext = os.path.splitext(self.request.path)
        print(filename, ext)

        if ext in ("", "html"):
            return self.get_html()
        else:
            return self.get_static(filename + ext)

    def get_static(self, filename: str) -> HttpResponseBase:
        if not os.path.exists(DOCUMENT_ROOT + filename):
            return HttpResponse404()

        with open(DOCUMENT_ROOT + filename, "rb") as f:
            content = f.readlines()
            content_type = MIME_TYPES[os.path.splitext(f.name)[-1]]
            return HttpResponse(content, content_type)

    def get_html(self) -> HttpResponseBase:
        try:
            view_cls = Route(self.request.path).get_view()
            return view_cls(self.request).get_response()
        except ValueError:
            return HttpResponse404()
