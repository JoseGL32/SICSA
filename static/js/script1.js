document.getElementById("file").onchange = function(e){
    let reader = new FileReader();
    reader.readAsDataURL(e.target.files[0]);
    reader.onload = function(){
        let preview = document.getElementById("preview");
        imagen = document.createElement('img');
        imagen.src = reader.result;
        imagen.style.width = "400px";
        preview.innerHTML =  "";
        preview.append(imagen);
        document.getElementById("file").style.display= "none";
    }
}