from django.contrib import admin
from .models import Cuestionario, Categoria
# Register your models here.

admin.site.register(Categoria)
admin.site.register(Cuestionario)