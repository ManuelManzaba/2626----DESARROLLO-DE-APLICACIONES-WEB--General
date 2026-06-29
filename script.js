// 1. Obtener los elementos del HTML mediante sus identificadores únicos (ID)
const formulario = document.getElementById('formulario-registro');
const inputNombre = document.getElementById('nombre');
const selectCategoria = document.getElementById('categoria');
const txtDescripcion = document.getElementById('descripcion');
const mensajeValidacion = document.getElementById('mensaje-validacion');
const listaRegistros = document.getElementById('lista-registros');
const contadorRegistros = document.getElementById('contador-registros');

// Variable global para llevar el conteo de los registros
let totalRegistros = 0;

// 2. Escuchar el evento de envío (submit) del formulario
formulario.addEventListener('submit', function (event) {
    // Evita que la página web se recargue por defecto
    event.preventDefault();

    // Capturar los valores ingresados por el usuario eliminando espacios extras
    const nombre = inputNombre.value.trim();
    const categoria = selectCategoria.value;
    const descripcion = txtDescripcion.value.trim();

    // 3. Validación: Comprobar que ningún campo esté vacío
    if (nombre === '' || categoria === '' || descripcion === '') {
        mostrarAlerta('Por favor, complete todos los campos del formulario antes de guardar.', 'danger');
        return; // Detiene la ejecución del código
    }

    // Si los datos son válidos, mostrar alerta de éxito
    mostrarAlerta('¡Proyecto registrado correctamente!', 'success');

    // 4. Crear de forma dinámica la tarjeta con los datos ingresados
    crearElementoLista(nombre, categoria, descripcion);

    // 5. Incrementar el contador global y actualizarlo en pantalla
    totalRegistros++;
    actualizarContador();

    // Limpiar todos los campos del formulario para un nuevo ingreso
    formulario.reset();
});

// Función para generar alertas visuales usando clases de Bootstrap
function mostrarAlerta(mensaje, estilo) {
    mensajeValidacion.innerHTML = `
        <div class="alert alert-${estilo} alert-dismissible fade show m-0" role="alert">
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}

// Función para crear las tarjetas HTML usando los métodos createElement y appendChild
function crearElementoLista(nombreVal, categoriaVal, descripcionVal) {
    // Crear el contenedor de la columna responsiva
    const columna = document.createElement('div');
    columna.className = 'col-12';

    // Crear la tarjeta contenedora principal
    const tarjeta = document.createElement('div');
    tarjeta.className = 'card shadow-sm border-start border-primary border-4';

    // Crear el cuerpo interno de la tarjeta
    const cuerpo = document.createElement('div');
    cuerpo.className = 'card-body d-flex justify-content-between align-items-center';

    // Crear la caja contenedora de los textos
    const contenidoTexto = document.createElement('div');

    // Crear el título con el nombre del proyecto
    const titulo = document.createElement('h6');
    titulo.className = 'card-title mb-1 fw-bold';
    titulo.textContent = nombreVal;

    // Crear la etiqueta de la categoría
    const etiqueta = document.createElement('span');
    etiqueta.className = 'badge bg-secondary mb-2 d-inline-block';
    etiqueta.textContent = categoriaVal;

    // Crear el párrafo con la descripción
    const parrafoDesc = document.createElement('p');
    parrafoDesc.className = 'card-text text-muted small mb-0';
    parrafoDesc.textContent = descripcionVal;

    // Unir los elementos de texto en su respectivo contenedor
    contenidoTexto.appendChild(titulo);
    contenidoTexto.appendChild(etiqueta);
    contenidoTexto.appendChild(parrafoDesc);

    // Crear el botón de eliminación
    const botonEliminar = document.createElement('button');
    botonEliminar.className = 'btn btn-danger btn-sm';
    botonEliminar.textContent = 'Eliminar';

    // Asignar el evento de clic al botón eliminar
    botonEliminar.addEventListener('click', function () {
        columna.remove(); // Remueve la tarjeta del DOM
        totalRegistros--; // Disminuye el contador en uno
        actualizarContador(); // Actualiza la interfaz de usuario
    });

    // Unir todas las partes estructurales mediante appendChild
    cuerpo.appendChild(contenidoTexto);
    cuerpo.appendChild(botonEliminar);
    tarjeta.appendChild(cuerpo);
    columna.appendChild(tarjeta);

    // Insertar el nuevo registro al listado visible en la página
    listaRegistros.appendChild(columna);
}

// Función encargada de actualizar el valor del contador en pantalla
function actualizarContador() {
    contadorRegistros.textContent = totalRegistros;
}