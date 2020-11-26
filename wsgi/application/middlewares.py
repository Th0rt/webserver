from abc import ABC, abstractmethod
from typing import Union
from uuid import uuid4

from .request import HttpRequest
from .response import HttpResponseBase
from .sessions import SESSION_STORAGE
from .views import ViewBase


class MiddlewareBase(ABC):
    def __init__(self, next: Union["MiddlewareBase", ViewBase]) -> None:
        self.next = next

    @abstractmethod
    def get_response(self, request: HttpRequest) -> HttpResponseBase:
        raise NotImplementedError


class SessionMiddleware(MiddlewareBase):
    def __init__(self, next: Union["MiddlewareBase", ViewBase]) -> None:
        super().__init__(next=next)

    def get_response(self, request: HttpRequest) -> HttpResponseBase:
        if "session_id" in request.cookie:
            session_id = request.cookie["session_id"]
            request.session = SESSION_STORAGE[session_id]
        else:
            session_id, session = str(uuid4()), {}
            SESSION_STORAGE[session_id] = session
            request.session = session

        response: HttpResponseBase = self.next.get_response(request)
        response.cookie["session_id"] = session_id

        return response
