from typing import Callable, Iterable


class WSGIApplication:
    def application(env: dict, start_response: Callable) -> Iterable[bytes]:
        start_response(b'200 OK', [(b'Content-type', b'text/plain; charset=utf-8')])
        return [b'Hello World']
