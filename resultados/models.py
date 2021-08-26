from django.db import models
from django.contrib.auth.models import User
from cuestionario.models import Cuestionario
from preguntas.models import Pregunta, Respuesta

# Create your models here.

class Resultado(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete = models.CASCADE)
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    preguntas = models.TextField(null=True)
    respuestas = models.TextField(null=True)
    puntaje = models.DecimalField(max_digits = 5, decimal_places = 2)
    fecha = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"cuestionario: {self.cuestionario}, usuario: {self.usuario}, puntaje: {self.puntaje}, fecha: {self.fecha}, pk: {self.pk} "
