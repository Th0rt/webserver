import os
import random
import string
from abc import ABC
from datetime import datetime
from io import BytesIO

from .request import HttpRequest
from .response import HttpResponse, HttpResponse405, HttpResponseBase
from .settings import DOCUMENT_ROOT, MIME_TYPES


class ViewBase(ABC):
    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def get_response(self, *args, **kwargs) -> HttpResponseBase:
        if self.request.request_method == "GET":
            return self.get(args, kwargs)
        elif self.request.request_method == "POST":
            return self.post(args, kwargs)
        else:
            return HttpResponse405()

    def get(self, *args, **kwargs) -> HttpResponseBase:
        return HttpResponse405()

    def post(self, *args, **kwargs) -> HttpResponseBase:
        return HttpResponse405()


class IndexView(ViewBase):
    def get(self, *args, **kwargs) -> HttpResponseBase:
        with open(os.path.join(DOCUMENT_ROOT + "/index.html"), "rb") as f:
            content = f.readlines()
            content_type = MIME_TYPES[".html"]

        return HttpResponse(content, content_type)


class NowView(ViewBase):
    def get(self, *args, **kwargs) -> HttpResponseBase:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode("utf-8")
        return HttpResponse(BytesIO(now), MIME_TYPES[".html"])


class HeaderView(ViewBase):
    def get(self, *args, **kwargs) -> HttpResponseBase:
        content = BytesIO(str(self.request.as_dict()).encode("utf-8"))
        return HttpResponse(content, MIME_TYPES[".html"])


class ParametersView(ViewBase):
    def get(self, *args, **kwargs) -> HttpResponseBase:
        content = BytesIO(str(self.request.query_string).encode("utf-8"))
        content_type = MIME_TYPES[".html"]
        return HttpResponse(content, content_type)

    def post(self, *args, **kwargs) -> HttpResponseBase:
        content = BytesIO(str(self.request.request_body).encode("utf-8"))
        return HttpResponse(content, MIME_TYPES[".html"])

class SetCookieView(ViewBase):
    cookie_value = {}
    content = """
<html>
  <head>
    <meta httpequiv="ContentType" content="text/html;charset=utf-8" />
    <title>テストフォーム</title>
  </head>
  <body>
    こんにちは、{username}さん。
    <form action="http://localhost:8090/setcookie" method="post" enctype="multipart/form-data">
      テキストボックス：<input type="text" name="username" /><br />
      <input type="submit" name="submit_name" value="送るよ!" />
    </form>
  </body>
</html>
"""

    def get_content(self, username: str) -> str:
        return self.content.replace("{username}", username)

    def get(self, *args, **kwargs) -> HttpResponseBase:
        try:
            user_id = self.request.cookie["user_id"]
            username = self.cookie_value[user_id]
        except KeyError:
            username = "名無し"

        content = BytesIO(self.get_content(username).encode("utf-8"))
        return HttpResponse(content, MIME_TYPES[".html"])

    def post(self, *args, **kwargs) -> HttpResponseBase:
        key = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(12)])
        username = self.request.request_body.get("username", "名無し")
        self.cookie_value[key] = username

        content = BytesIO(self.get_content(username).encode("utf-8"))
        return HttpResponse(content, MIME_TYPES[".html"], cookie={"user_id": key})
