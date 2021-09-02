from django.forms import ModelForm
from .models import Cuestionario, Categoria
from preguntas.models import Pregunta, Respuesta

class CuestionarioForm(ModelForm):
    class Meta:
        model = Cuestionario
        fields = '__all__'


class PreguntaForm(ModelForm):
    class Meta:
        model = Pregunta
        fields = '__all__'


class RespuestaForm(ModelForm):
    class Meta:
        model = Respuesta
        fields = '__all__'

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
