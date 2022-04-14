from unicodedata import name
from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings/<int:auction_id>/", views.listings, name="listings"),
    path("addwatch/<int:auction_id>/", views.addWatch, name="addwatch"),
    path("watchlist", views.watchList, name="watchlist")
]
