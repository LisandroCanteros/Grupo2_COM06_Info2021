from django.urls import path
from .views import (
                    UserSignUp, UserLogin, UserLogout,
                    )

urlpatterns = [
    path("registro/", UserSignUp, name ="registro"),
    path("login/", UserLogin, name="login"),
    path("logout/", UserLogout, name="logout"),
]
