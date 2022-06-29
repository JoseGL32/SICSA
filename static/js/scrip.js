
document.addEventListener("DOMContentLoaded", () => {
    // Escuchamos el click del botón
    const $boton = document.querySelector("#print");
    $boton.addEventListener("click", () => {
 
        const $elementoParaConvertir = document.querySelector(".containers")

        // <-- Aquí puedes elegir cualquier elemento del DOM
        html2pdf()
            .set({
                margin: 1,
                filename: 'Cotizacion.pdf',
                html2canvas: {
                    scale: 3, // A mayor escala, mejores gráficos, pero más peso
                    letterRendering: true,
                   
                },
                jsPDF: {
                    margin: 10,
                    unit: "in",
                    format: "a3",
                    orientation: 'portrait', // landscape o portrait
                },
            })
            .from($elementoParaConvertir)
            .save()
            .catch(err => console.log(err));
    });
});

//segundo pdf
document.addEventListener("DOMContentLoaded", () => {
    // Escuchamos el click del botón
    const $boton = document.querySelector("#print");
    $boton.addEventListener("click", () => {
 
         $elementoParaConvertir = document.querySelector(".containers-fact")
         elementoParaConvertir += document.querySelector(".containers-fact")
        // <-- Aquí puedes elegir cualquier elemento del DOM
        html2pdf()
            .set({
                margin: 1,
                filename: 'facturacion.pdf',
                html2canvas: {
                    scale: 2, // A mayor escala, mejores gráficos, pero más peso
                   
                },
                jsPDF: {
                    width : doc.internal.pageSize.getWidth(),
                    height : doc.internal.pageSize.getHeight(),
                    margin: 10,
                    unit: "mm",
                    format: "a4",
                    orientation: 'portrait', // landscape o portrait
                
                }
            })
            .from($elementoParaConvertir)
            .from($elementoParaConvertir)
            .save()
            .catch(err => console.log(err));
    });
});


