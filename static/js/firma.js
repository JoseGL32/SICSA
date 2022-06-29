var canvas1 = document.getElementById("signature");
var w = window.innerWidth;
var h = window.innerHeight;

// Como el lienzo no tiene ningún tamaño, lo especificaremos con JS
// El ancho del canvas será el ancho del dispositivo.
canvas1.width = w - 900;
// La altura del lienzo será (casi) la tercera parte de la altura de la pantalla.
canvas1.height = h / 2.5;

var signaturePad = new SignaturePad(canvas1, {
    dotSize: 0.5

});

document.getElementById("reset").addEventListener("click", function (e) {
    // Limpia el lienzo
    signaturePad.clear();
}, false);

const saveReport = (event) => {
    event.preventDefault();
    const formData = new FormData(document.getElementById('addReport'));
    /*CREAR EL INPUT CON LA IMAGEN*/
    var imageURI = signaturePad.toDataURL();
    const image = document.createElement('input');
    image.setAttribute('type', 'image');
    image.src = imageURI;
    image.value = imageURI;
    formData.append('signature', image.value);
    let request = new XMLHttpRequest();
    request.open('POST', '/firma');
    
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        if (data.status == 200) {
            alert('Firma Guardada');
            window.location = ('home');
        }
        else {
            alert('Error al crear el reporte, revise los datos');
        }
    }
    request.send(formData);
}