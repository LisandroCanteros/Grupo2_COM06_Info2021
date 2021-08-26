from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from preguntas.models import Pregunta, Respuesta
from resultados.models import Resultado

from .models import Cuestionario, Categoria
# Create your views here.

def pagina_principal(request):
    return render(request, "pagina_principal.html")


class CategoriasListView(ListView):
    model = Cuestionario
    template_name = "categorias.html"


def categorias_vista(request, categoria):
    cuestionario = Cuestionario.objects.all().values('categoria')
    return render(request, "categorias.html", {'obj': cuestionario})


class CuestionarioListView(ListView):
    model = Cuestionario
    template_name = "cuestionarios.html"


def cuestionario_vista(request, categoria, pk):
    # se obtiene la pk desde el navegador (urls.py) y con ella, se busca el cuestionario a la cual hace referencia (Cuestionario.objects.get())
    cuestionario = Cuestionario.objects.get(pk=pk) #esto devuelve un objeto cuestionario que tenga la pk especificada
    context = {
        'obj': cuestionario
    }
    print("---------", cuestionario)
    return render(request, "jugar.html", context)


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


def guardar_resultados(request, categoria, pk):
    if request.is_ajax():
        data = request.POST
        data_ = dict(data.lists())  # de los datos recibidos por ajax, los convierto en dict
        data_.pop('csrfmiddlewaretoken') # elimino el token dejando las preguntas y respuestas

        lista_preguntas = []
        for preg, rta in data_.items():
            pregunta = Pregunta.objects.get(texto=preg)
            lista_preguntas.append(pregunta)

        usuario = request.user
        cuest = Cuestionario.objects.get(pk=pk)

        puntaje = 0
        multiplicador = 100 / len(lista_preguntas)
        resultados = []
        respuesta_correcta = None
        for pregunta in lista_preguntas:                  #loop sobre todas las preguntas
            rta_elegida = request.POST.get(pregunta.texto)

            if rta_elegida != "":
                #loop respuestas contestadas
                respuestas = Respuesta.objects.filter(pregunta=pregunta)

                for rta in respuestas:
                    if rta.texto == rta_elegida:
                        if rta.es_correcta:
                            puntaje += 1
                            rta_correcta = rta.texto
                    else:
                        if rta.es_correcta:
                            rta_correcta = rta.texto

                resultados.append({str(pregunta): {'rta_correcta': rta_correcta, "rta_elegida": rta_elegida}})
            else:
                # respuesta sin contestar
                respuestas= Respuesta.objects.filter(pregunta=pregunta)
                for rta in respuestas:
                    if rta.es_correcta:
                        rta_correcta = rta.texto

                resultados.append({str(pregunta): {'rta_correcta': rta_correcta, "rta_elegida": "Sin responder"}})

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
        preguntas[pregunta] = preguntas[pregunta][0].replace("[", "").replace("]", "")

    print(preguntas)
    print(respuestas_correctas)
    print(respuestas_elegidas)

    context = {
        "resultado": resultado,
        "zip": zip(preguntas, respuestas_correctas, respuestas_elegidas)
    }
    return render(request, "resultado.html", context)
