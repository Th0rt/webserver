from typing import Type

from . import settings, views


class Route:
    def __init__(self, path: str):
        self.path = path
        self.route = {
            "/": views.IndexView,
            "/now": views.NowView,
            "/header": views.HeaderView,
            "/parameters": views.ParametersView
        }
        print(f"requested resource is {settings.DOCUMENT_ROOT} {self.path}")

    def get_view(self) -> Type[views.ViewBase]:
      try:
        return self.route[self.path]
      except KeyError:
        raise ValueError("path is unknown.")
