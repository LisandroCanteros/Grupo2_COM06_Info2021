console.log("main js ejecutándose...");
const modalBtns = [...document.getElementsByClassName('modal-button')]; //botones en la pantalla
const modalBody = document.getElementById('modal-body-confirm'); //información al clickear el boton del cuest
const startBtn = document.getElementById('start-button'); //obtener el boton de "comenzar"

const url = window.location.href // obtiene url actual y redirecciona a otra

// tomar todos los modalBtns (se los conoce por su nombre de clase, definidos en const linea 2) y por cada uno, mostrar su información (definida en el html)
modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', ()=>{

  //obtener todos los atributos del cuestionario pasados desde el html
  const pk = modalBtn.getAttribute('data-pk')
  const nombre = modalBtn.getAttribute('data-nombre')
  const categoria = modalBtn.getAttribute('data-categoria')
  const max_preguntas = modalBtn.getAttribute('data-max_preguntas')
  const dificultad = modalBtn.getAttribute('data-dificultad')
  const tiempo_limite = modalBtn.getAttribute('data-tiempo_limite')
  const puntaje_aprobacion = modalBtn.getAttribute('data-puntaje_aprobacion')


  // imprimir los atributos por pantalla, ver backtick
  modalBody.innerHTML = `
    <div class="h5 mb-3"> Comenzar <b>${nombre}</b> </div>

    <div class="text-muted">
      <ul>
        <li>Categoría: <b>${categoria}</b> </li>
        <li>Dificultad: <b>${dificultad}</b> </li>
        <li>Número de preguntas: <b>${max_preguntas}</b> </li>
        <li>Puntaje necesario para aprobar: <b>${puntaje_aprobacion}%</b> </li>
        <li>Tiempo límite: <b>${tiempo_limite} min</b> </li>
      </ul>
    </div>
    `
    startBtn.addEventListener('click', ()=>{
      window.location.href = url + pk //concatena direccion url actual con la pk del cuestionario
    })
}));
