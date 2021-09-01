console.log("jugar.js ejecutándose...");

const url = window.location.href

const cuestionarioCuadro = document.getElementById('formulario-caja')
const cuadroPuntaje = document.getElementById('cuadro-puntaje')
const cuadroResultados = document.getElementById('cuadro-resultados')
const cuadroTimer = document.getElementById('timer')

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const startTimer = (tiempo_limite)=> {
  if(tiempo_limite.toString().length < 2){
    cuadroTimer.innerHTML = `Tiempo restante: <b>0${tiempo_limite}:00 </b> `
  }else{
    cuadroTimer.innerHTML = `Tiempo restante: <b>${tiempo_limite}:00 </b> `
  }

  let minutos = tiempo_limite - 1
  let segundos = 60
  let displaySegundos
  let displayMinutos
  const Timer = setInterval(()=>{  // set interval ejecuta algo cada cierto tiempo, en este caso cada 1000 ms o 1 seg.
    segundos = segundos - 1
    if (segundos < 0){
      segundos = 59
      minutos = minutos - 1
    }

    if (minutos.toString().length < 2){
      displayMinutos = '0' + minutos
    }else{
      displayMinutos = minutos
    }

    if (segundos.toString().length < 2){
      displaySegundos = '0' + segundos
    }else{
      displaySegundos = segundos
    }

    if (minutos === 0 && segundos === 0){ //si el cronómetro es 0 entonces enviar las respuestas.
      cuadroTimer.innerHTML = "<b>00:00</b>"
      setTimeout(()=>{
        clearInterval(Timer)
        alert("TIME OVER")
        enviarDatos()

      })
    }

    cuestForm.addEventListener('submit', e=>{  //si el jugador envía antes del tiempo limite
      e.preventDefault()
      clearInterval(Timer)

      let minutos_empleados = tiempo_limite - displayMinutos - 1
      let segundos_empleados = 60 - segundos

      cuadroTimer.innerHTML = `Tiempo empleado: <b>${minutos_empleados} minutos ${segundos_empleados} segundos</b> <br>`
    })

    cuadroTimer.innerHTML = `Tiempo restante: <b>${displayMinutos}:${displaySegundos}</b>`

  }, 1000)
}

$.ajax({
  type: 'GET', // tomar datos
  url: `${url}jugar`, // de donde tomar los datos. Sé qué url contiene la direccion actual y a eso necesito agregarle /jugar(porque así lo definí en urls.py)
  success: function(response) {
    const data = response.data
    data.forEach(elto => { //cada elemento tiene una clave (pregunta) y valores (respuestas)
      for (const[pregunta, respuestas] of Object.entries(elto)) {  //separar preguntas y sus respuestas
        cuestionarioCuadro.innerHTML += `
          <div class="mb-2">
            <b> ${pregunta} </b>
          </div>
        `
        respuestas.forEach(respuesta => {
          cuestionarioCuadro.innerHTML += `
            <div class="form-check">
              <input type="checkbox" class="form-check-input respuesta" id="${pregunta}-${respuesta}" name="${pregunta}" value="${respuesta}">
              <label for="${pregunta}"> ${respuesta} </label>
            </div>
          `
        });

      }
    });
    startTimer(response.tiempo)
  },
  error: function(error) {
    console.log(error)
  }
})


const cuestForm = document.getElementById("formulario-cuestionario")
const csrf = getCookie('csrftoken')

const enviarDatos = () => {
  const rtas = [...document.getElementsByClassName('respuesta')] //convierte lista a arreglo
  const datos = {}
  datos['csrfmiddlewaretoken'] = csrf

  rtas.forEach(rta =>{
    if (rta.checked){   //si esta respuesta está seleccionada

      if (datos[rta.name] == null){
        datos[rta.name] = [rta.value] // name(pregunta) y value(respuesta) están definidos más arriba en el segundo bloque html. Entonces básicamente se tiene la pregunta con la respuesta marcada.
      }else{
        datos[rta.name].push(rta.value)
      }

    }else{
      if (!datos[rta.name]){ //si una determinada pregunta no tiene respuesta seleccionada
        datos[rta.name] = null  // asignarle null
      }
    }
  }
)

  $.ajax({
    type: 'POST',
    url: `${url}guardar/`, //url definida arriba
    data: datos, //diccionario a retornar a la vista (guardar_resultados) mediante JsonResponse
    success: function(response){
      const resultados = response.resultado //haciendo uso de response se pueden acceder a los valores pasados como diccionario desde la vista (guardar_resultados)
      cuestForm.classList.add('not-visible') //escondo el formulario (las opciones)
      cuadroPuntaje.innerHTML =`${response.aprobado? 'Aprobado. ' : 'Desaprobado. '} Tu puntaje es: ${response.puntaje.toFixed(2)}% <br>`


      resultados.forEach(result => {
          const resDiv = document.createElement("div")
          for (const [pregunta, rta] of Object.entries(result)){ //para cada resultado separo pregunta y respuesta
            resDiv.innerHTML += pregunta
            const cls = ['container', 'p-3', 'text-light', 'h3'] //estilos a aplicar a los resultados mostrados
            resDiv.classList.add(...cls)

            // cómo mostrar respuestas de acuerdo a si son corrrectas o no

            if (rta == 'Sin responder'){
              const correcta = rta['rta_correcta']
              resDiv.innerHTML += ` <br> Sin contestar`
              resDiv.innerHTML += ` <br> Respuesta correcta: ${correcta}`
              resDiv.classList.add('bg-danger') //clase de bootstrap para mostrar texto rojo

            }else{
              const respuesta = rta['rta_elegida']
              const correcta = rta['rta_correcta']

              if (respuesta == correcta){
                resDiv.classList.add('bg-success')
                resDiv.innerHTML += ` <br> Respuesta elegida: ${respuesta}`
              }else{
                resDiv.classList.add('bg-danger') //clase de bootstrap para mostrar texto rojo
                resDiv.innerHTML += ` <br> Respuesta correcta: ${correcta}`
                resDiv.innerHTML += ` <br> Respuesta elegida: ${respuesta}`
              }

            }
            cuadroResultados.append(resDiv)
          }
      });
    },
    error: function(error){
      console.log(error)
    }
  })
}





cuestForm.addEventListener('submit', e=>{
  e.preventDefault()
  enviarDatos()
})
