from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.main, name = "main"),
    path("login", views.userAuth, name = "login"),
    path("home", views.home, name = "home" ),
    path("logout", views.user_logout, name = "logout"),
    path("pao/", include("pao.urls")),
    path("oopk/", include("oopk.urls"))
    
] 