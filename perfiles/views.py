from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages

from .formulario import Registro, LoginForm
# Create your views here.
def UserSignUp(request):
    if request.method == "POST":
        form = Registro(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') #redirecciona a pagina de inicio despues de apretar enviar en el formulario
    else:
        form = Registro()

    context = {
        'form': form,
    }

    return render(request, 'registro.html', context)


def UserLogout(request):
    logout(request)
    return redirect("/")


def UserLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        usuario = request.POST['username']
        contraseña = request.POST['password']
        usuario = authenticate(username=usuario, password=contraseña)

        if usuario is not None:
            if usuario.is_active:
                login(request, usuario)
                return redirect("/")
        else:
            messages.error(request,'Usuario o contraseña incorrectos.')
            return redirect('/login')

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
