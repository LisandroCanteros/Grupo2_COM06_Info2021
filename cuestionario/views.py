from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from preguntas.models import Pregunta, Respuesta
from resultados.models import Resultado
from .models import Cuestionario, Categoria
from .formularios import CuestionarioForm, RespuestaForm, PreguntaForm
# Create your views here.

def pagina_principal(request):
    return render(request, "pagina_principal.html")

@staff_member_required
def nuevo_cuestionario(request):
    form = CuestionarioForm()

    if request.method == "POST":
        form = CuestionarioForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, "nuevo_cuestionario.html", context)

@staff_member_required
def editar_cuestionario(request, pk):
    cuestionario = Cuestionario.objects.get(pk=pk)
    form = CuestionarioForm(instance=cuestionario)

    if request.method == "POST":
        form = CuestionarioForm(request.POST, instance=cuestionario)
        if form.is_valid():
            form.save()
            return redirect("/categorias/")


    context = {'form': form}
    return render(request, "editar_cuestionario.html", context)

@staff_member_required
def eliminar_cuestionario(request, pk):
    cuestionario = Cuestionario.objects.get(pk=pk)
    if request.method == "POST":
        cuestionario.delete()
        return redirect("/categorias")
    context = {'cuestionario': cuestionario}
    return render(request, "eliminar_cuestionario.html", context)


@staff_member_required
def nueva_pregunta(request):
    form = PreguntaForm()

    if request.method == "POST":
        form = PreguntaForm(request.POST)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
    }
    return render(request, "nueva_pregunta.html", context)


@staff_member_required
def nueva_respuesta(request):
    form = RespuestaForm()

    if request.method == "POST":
        form = RespuestaForm(request.POST)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
    }
    return render(request, "nueva_respuesta.html", context)

class CategoriasListView(ListView):
    model = Categoria
    template_name = "categorias.html"

def categorias_vista(request, categoria):
    cuestionario = Cuestionario.objects.all().values('categoria')
    return render(request, "categorias.html", {'obj': cuestionario})

class CuestionarioListView(ListView):
    model = Cuestionario
    template_name = "cuestionarios.html"

@login_required(login_url='/login/')
def cuestionario_vista(request, categoria, pk):
    # se obtiene la pk desde el navegador (urls.py) y con ella, se busca el cuestionario a la cual hace referencia (Cuestionario.objects.get())
    cuestionario = Cuestionario.objects.get(pk=pk) #esto devuelve un objeto cuestionario que tenga la pk especificada
    context = {
        'obj': cuestionario
    }
    return render(request, "jugar.html", context)

@login_required(login_url='/login/')
def cuestionario_datos(request, categoria, pk):
    cuestionario = Cuestionario.objects.get(pk=pk)
    preguntas = []
    for pregunta in cuestionario.obtener_preguntas():
        respuestas = []                                 # la lista de respuestas se vacía para cada pregunta
        for respuesta in pregunta.obtener_respuestas():
            respuestas.append(respuesta.texto)
        preguntas.append({str(pregunta): respuestas}) # a cada pregunta, le asigno todas las respuestas

    return JsonResponse(
        {
            'data': preguntas,
            'tiempo': cuestionario.tiempo_limite
        }
    )

@login_required(login_url='/login/')
def guardar_resultados(request, categoria, pk):
    if request.is_ajax():
        data = request.POST
        data_ = dict(data.lists())  # de los datos recibidos por ajax, los convierto en dict
        data_.pop('csrfmiddlewaretoken')

        lista_preguntas = []

        for preg, rta in data_.items():
            preg = preg.replace("[]", "")
            pregunta = Pregunta.objects.get(texto=preg)
            lista_preguntas.append(pregunta)


        usuario = request.user
        cuest = Cuestionario.objects.get(pk=pk)

        puntaje = 0
        multiplicador = 100 / len(lista_preguntas)
        resultados = []
        respuesta_correcta = None

        for pregunta in lista_preguntas:
            cont = 0
            for preg in data_.keys():
                rta_elegidas = ""
                rta_correctas = ""
                pregunta_actual = preg.replace("[]", "")
                respuestas = Respuesta.objects.filter(pregunta=pregunta)
                for rta in data_[preg]:
                    rta_elegidas += rta + " "

                for respuesta in respuestas:
                    if respuesta.es_correcta:
                        rta_correctas += respuesta.texto + " "

                if pregunta_actual == str(respuestas[cont].pregunta):
                    if rta_elegidas == " ":
                        rta_elegidas = "Sin contestar"
                    elif rta_correctas == rta_elegidas:
                        puntaje += 1
                    resultados.append({str(pregunta): {'rta_correcta': rta_correctas, "rta_elegida": rta_elegidas}})
            cont += 1

        puntaje_ = puntaje * multiplicador
        lista_preguntas_ = []

        for pregunta in lista_preguntas:
            lista_preguntas_.append(pregunta.texto)

        resultado = Resultado.objects.create(cuestionario=cuest, usuario=usuario, preguntas=lista_preguntas_, respuestas=resultados, puntaje=puntaje_)
        if puntaje_ >= cuest.puntaje_para_aprobar:
            return JsonResponse({'aprobado': True, 'puntaje':puntaje_, 'resultado': resultados})
        else:
            return JsonResponse({'aprobado': False, 'puntaje':puntaje_, 'resultado': resultados})

def resultado(request, pk):
    resultado = Resultado.objects.get(pk=pk)
    usuario = resultado.usuario
    preg_y_resp_lista = resultado.respuestas.split('}},')
    preguntas_respuestas = []
    preguntas = []
    respuestas = []
    respuestas_elegidas = []
    respuestas_correctas = []
    aux = []

    for preg_resp in preg_y_resp_lista:
         preguntas_respuestas.append(preg_resp.replace("{", "").replace("}","").replace("'","").replace("rta_correcta", "Respuesta correcta").replace("rta_elegida", "Respuesta elegida").replace("[", "").replace("]", ""))

    for elemento in preguntas_respuestas:
        preguntas.append(elemento.split("Respuesta correcta")[0].split("Respuesta elegida"))

    for pregunta in preguntas:
        for elto in pregunta:
            elto.replace("[", "").replace("]", "")
            for el in range(len(preguntas_respuestas)):
                preguntas_respuestas[el] = preguntas_respuestas[el].replace(elto, "")

    for elemento in preguntas_respuestas:
        aux = (elemento.split(','))
        respuestas_elegidas.append(aux[1])

    aux *= 0

    for elemento in preguntas_respuestas:
        aux = (elemento.split(','))
        respuestas_correctas.append(aux[0])

    for pregunta in range(len(preguntas)):
        preguntas[pregunta] = preguntas[pregunta][0].replace("[", "").replace("]", "").replace(":", "")


    context = {
        "usuario": usuario,
        "resultado": resultado,
        "zip": zip(preguntas, respuestas_correctas, respuestas_elegidas)
    }
    return render(request, "resultado.html", context)
