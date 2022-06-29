addEventListener("DOMContentLoaded", () => {
  const btn_menu = document.querySelector(".btn_menu");
  if (btn_menu) {
    btn_menu.addEventListener("click", () => {
      const menu_items = document.querySelector(".menu_items");
      menu_items.classList.toggle("show");
    });
  }
});

function reportes() {
  var reportes = document.querySelector(".div-reportes");
  if (reportes.style.display === "none") {
    reportes.style.display = "block";
  } else {
    reportes.style.display = "none";
  }
}
function perfil() {
  var reportes = document.querySelector(".perfil");
  if (reportes.style.display === "none") {
    reportes.style.display = "block";
  } else {
    reportes.style.display = "none";
  }
}

function notificacion() {
  var solicitud = document.querySelector(".div-notificacion");
  if (solicitud.style.display === "none") {
    solicitud.style.display = "block";
  } else {
    solicitud.style.display = "none";
  }
}
function notificacion1() {
  var solicitud = document.querySelector(".div-notificacion1");
  if (solicitud.style.display === "none") {
    solicitud.style.display = "block";
  } else {
    solicitud.style.display = "none";
  }
}
function notificacion1emp() {
  var solicitud = document.querySelector(".div-notificacion1emp");
  if (solicitud.style.display === "none") {
    solicitud.style.display = "block";
  } else {
    solicitud.style.display = "none";
  }
}
function solicitud() {
  var solicitud = document.querySelector(".div-solicitud");
  if (solicitud.style.display === "none") {
    solicitud.style.display = "block";
  } else {
    solicitud.style.display = "none";
  }
}
function reporte() {
  var solicitud = document.querySelector(".div-reportes");
  if (solicitud.style.display === "none") {
    solicitud.style.display = "block";
  } else {
    solicitud.style.display = "none";
    window.location = '../home'
  }
}
function acta() {
  var solicitud = document.querySelector(".div-acta");
  if (solicitud.style.display === "none") {
    solicitud.style.display = "block";
  } else {
    solicitud.style.display = "none";
  }
}
function acta_historial() {
  var solicitud = document.querySelector(".div-acta-print");
  if (solicitud.style.display === "none") {
    solicitud.style.display = "block";
  } else {
    solicitud.style.display = "none";
    window.location = '../home'
  }
}
function reportellen() {
  var solicitud = document.querySelector(".div-reportes-llenar");
  if (solicitud.style.display === "none") {
    solicitud.style.display = "block";
  } else {
    solicitud.style.display = "none";
  }
}
function reportellen1() {
  var solicitud = document.querySelector(".div-reportes-llenar1");
  if (solicitud.style.display === "none") {
    solicitud.style.display = "block";
  } else {
    solicitud.style.display = "none";
  }
}

function tareas() {
  var tareas = document.querySelector(".div-tareas");
  if (tareas.style.display === "none") {
    tareas.style.display = "block";
  } else {
    tareas.style.display = "none";
  }
}

function not() {
  var solicitud = document.querySelector(".div-not");
  if (solicitud.style.display === "none") {
    solicitud.style.display = "block";
  } else {
    solicitud.style.display = "none";
  }
}
function añadiremp() {
  var solicitud = document.querySelector(".div-añadiremp");
  if (solicitud.style.display === "none") {
    solicitud.style.display = "block";
  } else {
    solicitud.style.display = "none";
    
  }
}
function añadircli() {
  var solicitud = document.querySelector(".div-añadircli");
  if (solicitud.style.display === "none") {
    solicitud.style.display = "block";
  } else {
    solicitud.style.display = "none";
  }
}

// Grafico
var1 = document.getElementById("completado").innerHTML;
var2 = document.getElementById("incompleto").innerHTML;
var3 = document.getElementById("progreso").innerHTML;
const ctx = document.getElementById("myChart");
const myChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: ["Incompletos", "Completados", "En Progreso"],
    datasets: [
      {
        label: "Estadi",
        data: [var2, var1, var3],
        backgroundColor: ["#c63637", "#006c0f", "yellow"],
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  },
});
var $window = $(window);

function run() {
  var fName = arguments[0],
    aArgs = Array.prototype.slice.call(arguments, 0);
  try {
    fName.apply(window, aArgs);
  } catch (err) {
    alert("error");
  }
}

/* chart
            ================================================== */
function _chart() {
  $(".b-skills").appear(function () {
    setTimeout(function () {
      $(".chart").easyPieChart({
        easing: "easeOutElastic",
        delay: 3000,
        barColor: "#369670",
        trackColor: "#fff",
        scaleColor: false,
        lineWidth: 21,
        trackWidth: 21,
        size: 250,
        lineCap: "round",
        onStep: function (from, to, percent) {
          this.el.children[1].innerHTML = Math.round(percent);
        },
      });
    }, 150);
  });
}

$(document).ready(function () {
  run(_chart);
});
// var canvas1 = document.getElementById("signature");
// var w = window.innerWidth;
// var h = window.innerHeight;

// // Como el lienzo no tiene ningún tamaño, lo especificaremos con JS
// // El ancho del canvas será el ancho del dispositivo.
// canvas1.width = w - 900;
// // La altura del lienzo será (casi) la tercera parte de la altura de la pantalla.
// canvas1.height = h / 2.5;

// var signaturePad = new SignaturePad(canvas1, {
//     dotSize: 0.5

// });

// document.getElementById("reset").addEventListener("click", function (e) {
//     // Limpia el lienzo
//     signaturePad.clear();
// }, false);

// function pdf() {
//     alert('dentro')

// }

document.onreadystatechange = function () {
  if (document.readyState === "complete") {
  }
};

const saveReport = (event) => {
  event.preventDefault();
  const formData = new FormData(document.getElementById("addReport"));
  /*CREAR EL INPUT CON LA IMAGEN*/
  // var imageURI = signaturePad.toDataURL();
  // const image = document.createElement('input');
  // image.setAttribute('type', 'image');
  // image.src = imageURI;
  // image.value = imageURI;
  // formData.append('signature', image.value);
  let request = new XMLHttpRequest();
  request.open("POST", "/reporte");

  request.onload = () => {
    const data = JSON.parse(request.responseText);
    if (data.status == 200) {
      alert("Reporte creado");
      window.location = "home";
    } else {
      alert("Error al crear el reporte, revise los datos");
    }
  };
  request.send(formData);
};

/*empleados*/
