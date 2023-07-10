// Función para incrementar la cantidad de un plato
function incrementarCantidad(platoId) {
    const cantidadElement = document.getElementById(`cantidad-${platoId}`);
    let cantidad = parseInt(cantidadElement.textContent);
    cantidad++;
    cantidadElement.textContent = cantidad.toString();
    actualizarCantidadEnCart(platoId, cantidad);
  }
  
  // Función para decrementar la cantidad de un plato
  function decrementarCantidad(platoId) {
    const cantidadElement = document.getElementById(`cantidad-${platoId}`);
    let cantidad = parseInt(cantidadElement.textContent);
    if (cantidad > 1) {
      cantidad--;
      cantidadElement.textContent = cantidad.toString();
      actualizarCantidadEnCart(platoId, cantidad);
    }
  }
  
  // Función para actualizar la cantidad de un plato en cart_items
  function actualizarCantidadEnCart(platoId, cantidad) {
    const plato = cart_items.find(item => item.plato_id === platoId);
    if (plato) {
      plato.cantidad = cantidad;
    }
  }
  
  // Función para eliminar un plato de la carta
  function eliminarPlato(platoId) {
    const platoElement = document.getElementById(`plato-${platoId}`);
    platoElement.remove();
    eliminarPlatoDeCart(platoId);
  }
  
  // Función para eliminar un plato de cart_items
  function eliminarPlatoDeCart(platoId) {
    cart_items = cart_items.filter(item => item.plato_id !== platoId);
  }
  
  // Evento para aplicar el código de promoción
  const aplicarBtn = document.getElementById("aplicar-btn");
  aplicarBtn.addEventListener("click", () => {
    const codigoInput = document.getElementById("codigo-input");
    const codigoPromocion = codigoInput.value;
    // Lógica para aplicar el código de promoción
    // ...
  });
  