const formulario = document.getElementById('formulario-registro');
const listaRegistros = document.getElementById('lista-registros');
const alertaContainer = document.getElementById('alerta-container');
const spinner = document.getElementById('spinner-carga');

function mostrarAlerta(mensaje, tipo) {
    alertaContainer.innerHTML = `
        <div class="alert alert-${tipo} alert-dismissible fade show" role="alert">
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>`;
}

function verDetalle(nombre, categoria, desc) {
    document.getElementById('modal-contenido').innerHTML = `
        <p><strong>Proyecto:</strong> ${nombre}</p>
        <p><strong>Categoría:</strong> ${categoria}</p>
        <p><strong>Descripción:</strong> ${desc}</p>`;
    new bootstrap.Modal(document.getElementById('modalDetalle')).show();
}

function crearElementoLista(nombre, categoria, desc) {
    const columna = document.createElement('div');
    columna.className = 'col-md-6';
    columna.innerHTML = `
        <div class="card h-100 shadow-sm">
            <div class="card-body">
                <span class="badge bg-primary mb-2">${categoria}</span>
                <h6 class="card-title fw-bold">${nombre}</h6>
                <div class="d-grid gap-2">
                    <button class="btn btn-info btn-sm text-white" onclick="verDetalle('${nombre}', '${categoria}', '${desc}')">Ver Detalle</button>
                    <button class="btn btn-outline-danger btn-sm">Eliminar</button>
                </div>
            </div>
        </div>
    `;
    columna.querySelector('.btn-outline-danger').addEventListener('click', () => columna.remove());
    listaRegistros.appendChild(columna);
}

formulario.addEventListener('submit', (e) => {
    e.preventDefault();
    spinner.classList.remove('d-none'); // Mostrar spinner
    
    setTimeout(() => { // Simular tiempo de procesamiento
        const nombre = document.getElementById('nombre').value;
        const categoria = document.getElementById('categoria').value;
        const desc = document.getElementById('descripcion').value;

        if (nombre.length >= 3 && categoria && desc.length >= 10) {
            crearElementoLista(nombre, categoria, desc);
            mostrarAlerta("Proyecto guardado con éxito", "success");
            formulario.reset();
        } else {
            mostrarAlerta("Error: Verifica que el nombre tenga al menos 3 caracteres y la descripción al menos 10.", "danger");
        }
        spinner.classList.add('d-none'); // Ocultar spinner
    }, 600);
});