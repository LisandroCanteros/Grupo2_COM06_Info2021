from django.db import models
import random
# Create your models here.

CATEGORIAS = (
    ("Ciencia y Arte", "CIENCIA Y ARTE"),
    ("Historia", "HISTORIA"),
    ("Deportes", "DEPORTES"),
    ("Geografia", "GEOGRAFÍA"),
    ("Economia", "ECONOMÍA"),
    ("Ciencia y Educacion", "CIENCIA Y EDUCACIÓN"),
    ("Entretenimiento", "ENTRETENIMIENTO"),
)

class Categoria(models.Model):
    categoria = models.CharField(max_length=150, choices = CATEGORIAS)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return str(self.categoria)


DIFICULTADES = (
    ("fácil", "FÁCIL"),
    ("intermedio", "INTERMEDIO"),
    ("difícil", "DIFÍCIL")
)

class Cuestionario(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    max_preguntas = models.IntegerField()
    tiempo_limite = models.IntegerField(help_text="duración del cuestionario")   #quizas no es necesario
    puntaje_para_aprobar = models.IntegerField(help_text="puntaje requerido") # no es necesario
    dificultad = models.CharField(max_length=20, choices=DIFICULTADES) # no es necesario

    def __str__(self):
        return f"{self.nombre} - {self.pk}"

    def obtener_preguntas(self):
        preguntas = list(self.pregunta_set.all()) # reverse relation - trae todas las preguntas de un cuestionario y las convierte en formato lista
        random.shuffle(preguntas) # mezcla las preguntas de la lista
        return preguntas[:self.max_preguntas] #solo muestra las cantidad de preguntas definidas
