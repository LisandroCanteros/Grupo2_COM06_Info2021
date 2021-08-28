from django.db import models
from cuestionario.models import Cuestionario
# Create your models here.

class Pregunta(models.Model):
    texto = models.CharField(max_length=300)
    quiz = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.texto)

    def obtener_respuestas(self):
        return self.respuesta_set.all() #self.nombredelmodelo_set.all -- reverse relation -- trae todas las respuestas de una pregunta

class Respuesta(models.Model):
    texto = models.CharField(max_length=300)
    es_correcta = models.BooleanField(default=False)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

    def __str__(self):
        return f"pregunta: {self.pregunta.texto}, respuesta: {self.texto}, es correcta: {self.es_correcta}"
