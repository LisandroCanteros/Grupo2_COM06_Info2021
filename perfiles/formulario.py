from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    usuario = forms.CharField()
    contraseña = forms.CharField(widget = forms.PasswordInput)

class Registro(UserCreationForm):
    # UserCreationForm predeterminado proporciona username, password1 y password2.
    # Incluyendo from django.contrib.auth import User se pueden agregar más campos.
    email = forms.EmailField(required=True)
    nombre = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [    # especifica los campos a renderizar (registro.html) y su orden
            'nombre',
            'username',
            'email',
            'password1',
            'password2',
        ]
