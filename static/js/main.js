/**
 * main.js
 * JavaScript personalizado para la Escuela de Fútbol WEB_TOHALLY
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log("Scripts de TOHALLY cargados correctamente. ⚽");
    
    // ---------------------------------------------
    // 1. Cierre Automático de Mensajes Flash (Alertas de Bootstrap)
    // ---------------------------------------------
    
    // Selecciona todos los mensajes de alerta de Bootstrap
    var alerts = document.querySelectorAll('.alert');

    alerts.forEach(function(alert) {
        // Si el elemento es un mensaje flash (de éxito o info)
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            // Cierra la alerta después de 5 segundos (5000 milisegundos)
            setTimeout(function() {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // ---------------------------------------------
    // 2. Inicialización de Componentes (Opcional, si no funciona el data-bs-ride="carousel")
    // ---------------------------------------------
    
    // Inicializar carrusel (asegúrate de que el ID coincida con tu home.html)
    var myCarousel = document.getElementById('heroCarouselPublic');
    if (myCarousel) {
        new bootstrap.Carousel(myCarousel, {
            interval: 4000 // Cambia de slide cada 4 segundos
        });
    }

    // Nota: El carrusel en el dashboard (index.html) se llama heroCarousel
    var adminCarousel = document.getElementById('heroCarousel');
    if (adminCarousel) {
        new bootstrap.Carousel(adminCarousel, {
            interval: 5000
        });
    }

});

// Función de prueba para verificar la conexión JS
function logTest() {
    console.log("¡JavaScript está vivo!");
}