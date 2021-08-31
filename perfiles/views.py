from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from resultados.models import Resultado
from cuestionario.models import Cuestionario
from preguntas.models import Pregunta

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

def UserProfile(request, nombre):
    usuario = User.objects.get(username=nombre)
    if usuario.is_authenticated:
        resultados = Resultado.objects.filter(usuario=usuario).values().order_by('-fecha')
        lista_resultados = []

        for resultado in resultados:
            puntaje = int(resultado['puntaje'])
            cuest_id = (resultado['cuestionario_id'])
            fecha = resultado['fecha']
            cuestionario = Cuestionario.objects.filter(pk=cuest_id).values()
            cuest_nombre = cuestionario[0]['nombre']
            id = resultado['id']
            lista_resultados.append((id, cuest_nombre, puntaje, fecha))

        cuest_mas_jugado = cuestionario_mas_jugado(usuario)
        categ_mas_jugada = categoria_mas_jugada(usuario)

        context = {
            'usuario': usuario,
            'resultados': lista_resultados,
            'cuestionario_mas_jugado': cuest_mas_jugado,
            'categoria_mas_jugada': categ_mas_jugada,
        }
        return render(request, "perfil.html", context)
    else:
        return redirect('login')


def cuestionario_mas_jugado(usuario):
    resultados = Resultado.objects.filter(usuario=usuario)
    cuestionarios_jugados = {}
    for resultado in resultados:
        if resultado.cuestionario not in cuestionarios_jugados.keys():
            cuestionarios_jugados[resultado.cuestionario] = 1
        else:
            cuestionarios_jugados[resultado.cuestionario] += 1

    if len(cuestionarios_jugados) == 0:
        cuestionario_mas_jugado = None
    else:
        cuestionario_mas_jugado = max(cuestionarios_jugados, key=cuestionarios_jugados.get)

    return cuestionario_mas_jugado

def categoria_mas_jugada(usuario):
    resultados = Resultado.objects.filter(usuario=usuario)
    categorias_jugadas = {}
    for resultado in resultados:
        if resultado.cuestionario.categoria not in categorias_jugadas.keys():
            categorias_jugadas[resultado.cuestionario.categoria] = 1
        else:
            categorias_jugadas[resultado.cuestionario.categoria] += 1

    if len(categorias_jugadas) == 0:
        categoria_mas_jugada = None
    else:
        categoria_mas_jugada = max(categorias_jugadas, key=categorias_jugadas.get)

    return categoria_mas_jugada
