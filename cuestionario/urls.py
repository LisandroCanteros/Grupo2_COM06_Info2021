from django.urls import path
from .views import (
    CategoriasListView, pagina_principal,
    CuestionarioListView, cuestionario_vista, cuestionario_datos,
    guardar_resultados, resultado
    )


urlpatterns =[
    path("", pagina_principal, name="pagina_principal"),
    path("categorias/", CategoriasListView.as_view(), name="categorias"),


    path("categorias/<str:categoria>/", CuestionarioListView.as_view(), name="categoria-actual"),
    path("categorias/<str:categoria>/<int:pk>/", cuestionario_vista, name="cuestionarios"),
    path("categorias/<str:categoria>/<int:pk>/jugar", cuestionario_datos, name="jugar"),

    path("categorias/<str:categoria>/<int:pk>/guardar/", guardar_resultados, name="guardar_cuestionarios"),

    path("resultado/<int:pk>/", resultado, name='resultado'),

]
