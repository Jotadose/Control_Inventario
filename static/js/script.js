async function agregarProducto() {
    const id = document.getElementById('agregar_id').value;
    const nombre = document.getElementById('agregar_nombre').value;
    const cantidad = document.getElementById('agregar_cantidad').value;
    const precio = document.getElementById('agregar_precio').value;

    const response = await fetch('/agregar_producto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id, nombre, cantidad, precio }),
    });

    const result = await response.json();
    alert(result.message);
}

async function actualizarStock() {
    const id = document.getElementById('actualizar_id').value;
    const nueva_cantidad = document.getElementById('actualizar_cantidad').value;

    const response = await fetch('/actualizar_stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id, nueva_cantidad }),
    });

    const result = await response.json();
    alert(result.message);
}

async function mostrarInventario() {
    const response = await fetch('/mostrar_inventario');
    const result = await response.json();

    const inventarioDiv = document.getElementById('inventario');
    inventarioDiv.innerHTML = '';

    result.inventario.forEach(producto => {
        const productoDiv = document.createElement('div');
        productoDiv.classList.add('card', 'mt-2');
        productoDiv.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">ID: ${producto.id}</h5>
                <p class="card-text">Nombre: ${producto.nombre}</p>
                <p class="card-text">Cantidad: ${producto.cantidad}</p>
                <p class="card-text">Precio: ${producto.precio}</p>
            </div>
        `;
        inventarioDiv.appendChild(productoDiv);
    });
}

async function predecirDemanda() {
    const inputs = document.querySelectorAll('#prediccion_inputs input');
    const datos = Array.from(inputs).map(input => input.value);

    const response = await fetch('/predecir_demanda', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ datos }),
    });

    const result = await response.json();
    if (result.error) {
        alert(result.error);
    } else {
        document.getElementById('resultado_prediccion').innerText = `Demanda Predicha: ${result.demanda}`;
    }
}
