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

// =========================================================================
// INTEGRACIÓN SEMANA 6: FUNCIONES DE VALIDACIÓN DINÁMICA
// =========================================================================

// Función auxiliar para aplicar clases de Bootstrap según una condición
function aplicarEstiloValidacion(inputElement, condicion) {
    if (condicion) {
        inputElement.classList.remove('is-invalid');
        inputElement.classList.add('is-valid');
        return true;
    } else {
        inputElement.classList.remove('is-valid');
        inputElement.classList.add('is-invalid');
        return false;
    }
}

// Validar nombre: obligatorio y longitud mínima de 3 caracteres
function validarNombre() {
    const valor = inputNombre.value.trim();
    return aplicarEstiloValidacion(inputNombre, valor !== '' && valor.length >= 3);
}

// Validar categoría: selección obligatoria de una opción válida
function validarCategoria() {
    return aplicarEstiloValidacion(selectCategoria, selectCategoria.value !== '' && selectCategoria.value !== null);
}

// Validar descripción: obligatoria y con información suficiente (mínimo 10 caracteres)
function validarDescripcion() {
    const valor = txtDescripcion.value.trim();
    return aplicarEstiloValidacion(txtDescripcion, valor !== '' && valor.length >= 10);
}

// =========================================================================
// ESCUCHADORES DE EVENTOS EN TIEMPO REAL (input, blur, change)
// =========================================================================
inputNombre.addEventListener('input', validarNombre);
inputNombre.addEventListener('blur', validarNombre);

selectCategoria.addEventListener('change', validarCategoria);
selectCategoria.addEventListener('blur', validarCategoria);

txtDescripcion.addEventListener('input', validarDescripcion);
txtDescripcion.addEventListener('blur', validarDescripcion);


// 2. Escuchar el evento de envío (submit) del formulario
formulario.addEventListener('submit', function (event) {
    // Evita que la página web se recargue por defecto
    event.preventDefault();

    // Forzar la ejecución de validaciones al intentar enviar el formulario
    const esNombreValido = validarNombre();
    const esCategoriaValida = validarCategoria();
    const esDescripcionValida = validarDescripcion();

    // Capturar los valores ingresados por el usuario eliminando espacios extras
    const nombre = inputNombre.value.trim();
    const categoria = selectCategoria.value;
    const descripcion = txtDescripcion.value.trim();

    // Comprobar que todas las validaciones pasen antes de proceder a la lógica de la semana 5
    if (!esNombreValido || !esCategoriaValida || !esDescripcionValida) {
        mostrarAlerta('Por favor, complete correctamente todos los campos obligatorios antes de guardar.', 'danger');
        return; // Detiene la ejecución del código
    }

    // Si los datos son válidos, mostrar alerta de éxito
    mostrarAlerta('¡Proyecto registrado correctamente!', 'success');

    // 4. Crear de forma dinámica la tarjeta con los datos ingresados (Lógica nativa Semana 5)
    crearElementoLista(nombre, categoria, descripcion);

    // 5. Incrementar el contador global y actualizarlo en pantalla
    totalRegistros++;
    actualizarContador();

    // Limpiar todos los campos del formulario para un nuevo ingreso
    formulario.reset();

    // Remover los estilos verdes de validación correcta tras la limpieza del formulario
    inputNombre.classList.remove('is-valid');
    selectCategoria.classList.remove('is-valid');
    txtDescripcion.classList.remove('is-valid');
});

// Función para generar alertas visuales usando clases de Bootstrap
function mostrarAlerta(mensaje, estilo) {
    mensajeValidacion.innerHTML = `
        <div class="alert alert-${estilo} alert-dismissible fade show m-0 small fw-bold" role="alert">
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}

// Función para crear las tarjetas HTML usando los métodos createElement y appendChild
function crearElementoLista(nombreVal, categoriaVal, descripcionVal) {
    // Crear el contenedor de la columna responsiva (Cambiado a col-md-6 para visualización en cuadrícula)
    const columna = document.createElement('div');
    columna.className = 'col-md-6';

    // Crear la tarjeta contenedora principal
    const tarjeta = document.createElement('div');
    tarjeta.className = 'card h-100 shadow-sm border-start border-primary border-4';

    // Crear el cuerpo interno de la tarjeta
    const cuerpo = document.createElement('div');
    cuerpo.className = 'card-body d-flex flex-column justify-content-between';

    // Crear la caja contenedora de los textos
    const contenidoTexto = document.createElement('div');

    // Crear la etiqueta de la categoría
    const etiqueta = document.createElement('span');
    etiqueta.className = 'badge bg-primary mb-2 d-inline-block';
    etiqueta.textContent = categoriaVal;

    // Crear el título con el nombre del proyecto
    const titulo = document.createElement('h6');
    titulo.className = 'card-title mb-1 fw-bold text-dark';
    titulo.textContent = nombreVal;

    // Crear el párrafo con la descripción
    const parrafoDesc = document.createElement('p');
    parrafoDesc.className = 'card-text text-muted small mb-0';
    parrafoDesc.textContent = descripcionVal;

    // Unir los elementos de texto en su respectivo contenedor
    contenidoTexto.appendChild(etiqueta);
    contenidoTexto.appendChild(titulo);
    contenidoTexto.appendChild(parrafoDesc);

    // Crear contenedor para alinear el botón de borrado de forma organizada
    const contenedorBoton = document.createElement('div');
    contenedorBoton.className = 'text-end mt-3';

    // Crear el botón de eliminación
    const botonEliminar = document.createElement('button');
    botonEliminar.className = 'btn btn-outline-danger btn-sm';
    botonEliminar.textContent = 'Eliminar';

    // Asignar el evento de clic al botón eliminar
    botonEliminar.addEventListener('click', function () {
        columna.remove(); // Remueve la tarjeta del DOM
        totalRegistros--; // Disminuye el contador en uno
        actualizarContador(); // Actualiza la interfaz de usuario
        mostrarAlerta('Proyecto eliminado correctamente.', 'warning');
    });

    // Unir todas las partes estructurales mediante appendChild
    contenedorBoton.appendChild(botonEliminar);
    cuerpo.appendChild(contenidoTexto);
    cuerpo.appendChild(contenedorBoton);
    tarjeta.appendChild(cuerpo);
    columna.appendChild(tarjeta);

    // Insertar el nuevo registro al listado visible en la página
    listaRegistros.appendChild(columna);
}

// Función encargada de actualizar el valor del contador en pantalla
function actualizarContador() {
    contadorRegistros.textContent = totalRegistros;
}