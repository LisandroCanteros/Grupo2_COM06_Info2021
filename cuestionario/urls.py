from django.urls import path
from .views import (
    CategoriasListView, pagina_principal,
    CuestionarioListView, cuestionario_vista, cuestionario_datos,
    guardar_resultados, resultado, nuevo_cuestionario, editar_cuestionario, eliminar_cuestionario, nueva_pregunta, nueva_respuesta, agregar_categoria,
    )


urlpatterns =[
    path("", pagina_principal, name="pagina_principal"),

    path("nuevo_cuestionario/", nuevo_cuestionario, name="nuevo_cuestionario"),
    path("editar_cuestionario/<str:pk>", editar_cuestionario, name="editar_cuestionario"),
    path("eliminar_cuestionario/<str:pk>", eliminar_cuestionario, name="eliminar_cuestionario"),

    path("agregar_categoria", agregar_categoria, name="agregar_categoria"),

    path("agregar_pregunta/", nueva_pregunta, name="agregar_pregunta"),
    path("agregar_respuesta/", nueva_respuesta, name="agregar_respuesta"),

    path("categorias/", CategoriasListView.as_view(), name="categorias"),
    path("categorias/<str:categoria>/", CuestionarioListView.as_view(), name="categoria-actual"),
    path("categorias/<str:categoria>/<int:pk>/", cuestionario_vista, name="cuestionarios"),
    path("categorias/<str:categoria>/<int:pk>/jugar", cuestionario_datos, name="jugar"),

    path("categorias/<str:categoria>/<int:pk>/guardar/", guardar_resultados, name="guardar_cuestionarios"),

    path("resultado/<int:pk>/", resultado, name='resultado'),

]
