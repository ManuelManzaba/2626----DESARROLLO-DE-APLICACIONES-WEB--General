const formulario = document.getElementById('formulario-registro');
const listaRegistros = document.getElementById('lista-registros');
const contadorRegistros = document.getElementById('contador-registros');
let totalRegistros = 0;

// Arreglo de objetos (Datos iniciales)
const proyectosIniciales = [
    { nombre: "Proyecto Integrador U1", categoria: "Desarrollo Web", desc: "Base del portafolio" }
];

// Función para renderizar tarjetas
function crearElementoLista(nombre, categoria, desc) {
    const columna = document.createElement('div');
    columna.className = 'col-md-6';
    columna.innerHTML = `
        <div class="card h-100 shadow-sm border-start border-primary border-4">
            <div class="card-body">
                <span class="badge bg-primary mb-2">${categoria}</span>
                <h6 class="card-title fw-bold">${nombre}</h6>
                <p class="card-text text-muted small">${desc}</p>
                <button class="btn btn-outline-danger btn-sm w-100">Eliminar</button>
            </div>
        </div>
    `;
    // Evento para eliminar
    columna.querySelector('button').addEventListener('click', () => {
        columna.remove();
        totalRegistros--;
    });
    listaRegistros.appendChild(columna);
}

// Cargar datos al iniciar
document.addEventListener('DOMContentLoaded', () => {
    proyectosIniciales.forEach(p => {
        crearElementoLista(p.nombre, p.categoria, p.desc);
        totalRegistros++;
    });
});

// Manejo del formulario
formulario.addEventListener('submit', (e) => {
    e.preventDefault();
    const nombre = document.getElementById('nombre').value;
    const categoria = document.getElementById('categoria').value;
    const desc = document.getElementById('descripcion').value;

    if (nombre.length >= 3 && categoria && desc.length >= 10) {
        crearElementoLista(nombre, categoria, desc);
        totalRegistros++;
        formulario.reset();
    } else {
        alert("Por favor, verifica los campos.");
    }
});