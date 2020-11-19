from . import views

ROUTE = {
    "/": views.IndexView,
    "/now": views.NowView,
    "/header": views.HeaderView,
    "/parameters": views.ParametersView,
    "/setcookie": views.SetCookieView
}
