from django.urls import path
from .views import (
                    UserSignUp, UserLogin, UserLogout,
                    )
from cuestionario import views as cuestionario_views

urlpatterns = [
    path("registro/", UserSignUp, name ="registro"),
    path("login/", UserLogin, name="login"),
    path("logout/", UserLogout, name="logout"),
    path("categorias/", cuestionario_views.CategoriasListView.as_view(), name="categorias"),
]
