import os
from typing import Callable, Iterable

from .request import HttpRequest
from .response import HttpResponse, HttpResponse404, HttpResponseBase
from .route import ROUTE
from .settings import DOCUMENT_ROOT, MIME_TYPES
from .middlewares import SessionMiddleware


class WSGIApplication:
    MIDDLEWARES = [SessionMiddleware]

    def application(self, env: dict, start_response: Callable) -> Iterable[bytes]:
        self.request = HttpRequest(env)
        status_code, header, content = self.get_content().output()
        start_response(status_code, header)
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
            view = ROUTE[self.request.path](self.request)
        except KeyError:
            return HttpResponse404()

        for middleware in self.MIDDLEWARES:
            view = middleware(view)

        return view.get_response(self.request)
