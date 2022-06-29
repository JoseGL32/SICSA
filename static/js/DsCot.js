
function changemode() {
    document.getElementById("sectionCotizacion").style.display= '';
    document.getElementById("sectionMateriales").style.display= "none"; 
    document.getElementById("sectionMo").style.display= "none";
    document.getElementById("tablahistorial").style.display= "none";
    document.getElementById("secciondescripcion").style.display= 'none';
}

function changemodefinal() {
    document.getElementById("sectionCotizacion").style.display= '';
    document.getElementById("addRow").style.display= '';
    document.getElementById("btn_pass").style.display= "none"; 
    document.getElementById("sectionMateriales").style.display= "none"; 
    document.getElementById("sectionMo").style.display= "none";
    document.getElementById("tablahistorial").style.display= "none";
}


function changemodeMaterial() {
  document.getElementById("secciondescripcion").style.display= 'none';
    document.getElementById("sectionCotizacion").style.display= "none";
    document.getElementById("sectionMateriales").style.display= 'block';
    document.getElementById("sectionMo").style.display= "none";
    document.getElementById("tablahistorial").style.display= "none";
}

function changemodeMo() {
    document.getElementById("sectionCotizacion").style.display= "none";
    document.getElementById("sectionMateriales").style.display= 'none';
    document.getElementById("sectionMo").style.display= '';
    document.getElementById("tablahistorial").style.display= "none";
    document.getElementById("secciondescripcion").style.display= 'none';
}
function changemodehistorial() {
   
    document.getElementById("sectionCotizacion").style.display= "none";
    document.getElementById("sectionMateriales").style.display= 'none';
    document.getElementById("sectionMo").style.display= 'none';
    document.getElementById("tablahistorial").style.display= '';
    document.getElementById("secciondescripcion").style.display= 'none';
    
}
function changemodedesc(){
  document.getElementById("sectionCotizacion").style.display= "none";
  document.getElementById("sectionMateriales").style.display= 'none';
  document.getElementById("sectionMo").style.display= 'none';
  document.getElementById("tablahistorial").style.display= 'none';
  document.getElementById("secciondescripcion").style.display= '';
}


function changemodeMe(){

 document.getElementById('Elextrico').style.display = '';
 document.getElementById('auto').style.display = 'none';
 document.getElementById('mecanica').style.display = 'none';
 document.getElementById('Pintura').style.display = 'none';
 document.getElementById('consumibles').style.display = 'none';
 document.getElementById('H&S').style.display = 'none';
 document.getElementById("secciondescripcion").style.display= 'none';
}
function changemodeau(){

    document.getElementById('Elextrico').style.display = 'none';
    document.getElementById('auto').style.display = '';
    document.getElementById('mecanica').style.display = 'none';
    document.getElementById('Pintura').style.display = 'none';
    document.getElementById('consumibles').style.display = 'none';
    document.getElementById('H&S').style.display = 'none';
    document.getElementById("secciondescripcion").style.display= 'none';
   }
   function changemodemec(){

    document.getElementById('Elextrico').style.display = 'none';
    document.getElementById('auto').style.display = 'none';
    document.getElementById('mecanica').style.display = '';
    document.getElementById('Pintura').style.display = 'none';
    document.getElementById('consumibles').style.display = 'none';
    document.getElementById('H&S').style.display = 'none';
    document.getElementById("secciondescripcion").style.display= 'none';
   }
   function changemodepin(){

    document.getElementById('Elextrico').style.display = 'none';
    document.getElementById('auto').style.display = 'none';
    document.getElementById('mecanica').style.display = 'none';
    document.getElementById('Pintura').style.display = '';
    document.getElementById('consumibles').style.display = 'none';
    document.getElementById('H&S').style.display = 'none';
    document.getElementById("secciondescripcion").style.display= 'none';
   }
   function changemodehs(){

    document.getElementById('Elextrico').style.display = 'none';
    document.getElementById('auto').style.display = 'none';
    document.getElementById('mecanica').style.display = 'none';
    document.getElementById('Pintura').style.display = 'none';
    document.getElementById('consumibles').style.display = 'none';
    document.getElementById('H&S').style.display = '';
    document.getElementById("secciondescripcion").style.display= 'none';
   }
   function changemodecons(){

    document.getElementById('Elextrico').style.display = 'none';
    document.getElementById('auto').style.display = 'none';
    document.getElementById('mecanica').style.display = 'none';
    document.getElementById('Pintura').style.display = 'none';
    document.getElementById('consumibles').style.display = '';
    document.getElementById('H&S').style.display = 'none';
    document.getElementById("secciondescripcion").style.display= 'none';
   }

   function changemodeall(){

    document.getElementById('Elextrico').style.display = '';
    document.getElementById('auto').style.display = '';
    document.getElementById('mecanica').style.display = '';
    document.getElementById('Pintura').style.display = '';
    document.getElementById('consumibles').style.display = '';
    document.getElementById('H&S').style.display = '';
    document.getElementById("secciondescripcion").style.display= 'none';
   }

   function newRowTableAu() {

    var combo = document.getElementById("typeselect");
    var selected = combo.options[combo.selectedIndex].text;
    var numero = document.getElementById("Cantidadau").value;
    var costo = document.getElementById("Costoau").value;

    var name_table = document.getElementById("tabla_au");

    var row = name_table.insertRow(0 + 1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

    cell1.innerHTML = '<p name="numero_f[]" class="non-margin">' + selected + '</p>';
    cell2.innerHTML = '<p name="codigo_p[]" class="non-margin">' + numero + '</p>';
    cell3.innerHTML = '<p name="codigo_p[]" class="non-margin">' + costo + '</p>';
    typo = 1
  
    const dict_values = {
      selected,
      numero,
      costo,
       typo 
    }
    const dict_values1 = {
      numero
    } //Pass the javascript variables to a dictionary.
    const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
    document.getElementById("Cantidadau").value = "";
    document.getElementById("Costoau").value = "";
   
    $.ajax({
      type:"POST",
      url: "/Cotizacion",
      traditional:false,
      dataType:'json',
      contentType  : "application/json;charset=utf-8",
      data: JSON.stringify(s)
    });
  }


  function newRowTablemec() {

    var combo = document.getElementById("typeselectmec");
    var selected = combo.options[combo.selectedIndex].text;
    var numero = document.getElementById("Cantidadmec").value;
    var costo = document.getElementById("Costomec").value;

    var name_table = document.getElementById("tablamec");

    var row = name_table.insertRow(0 + 1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

    cell1.innerHTML = '<p name="numero_f[]" class="non-margin">' + selected + '</p>';
    cell2.innerHTML = '<p name="codigo_p[]" class="non-margin">' + numero + '</p>';
    cell3.innerHTML = '<p name="codigo_p[]" class="non-margin">' + costo + '</p>';
    typo = 1
  
    const dict_values = {
      selected,
      numero,
      costo,
       typo 
    }
    const dict_values1 = {
      numero
    } //Pass the javascript variables to a dictionary.
    const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
    document.getElementById("Cantidadmec").value = "";
    document.getElementById("Costomec").value = "";

   
    $.ajax({
      type:"POST",
      url: "/Cotizacion",
      traditional:false,
      dataType:'json',
      contentType  : "application/json;charset=utf-8",
      data: JSON.stringify(s)
    });
  }

  function newRowTablepin() {

    var combo = document.getElementById("typeselectpin");
    console.log('gh')
    var selected = combo.options[combo.selectedIndex].text;
    var numero = document.getElementById("Cantidadpin").value;
    var costo = document.getElementById("Costopin").value;

    var name_table = document.getElementById("tablapin");

    var row = name_table.insertRow(0 + 1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

    cell1.innerHTML = '<p name="numero_f[]" class="non-margin">' + selected + '</p>';
    cell2.innerHTML = '<p name="codigo_p[]" class="non-margin">' + numero + '</p>';
    cell3.innerHTML = '<p name="codigo_p[]" class="non-margin">' + costo + '</p>';
    typo = 1
  
    const dict_values = {
      selected,
      numero,
      costo,
       typo 
    }
    const dict_values1 = {
      numero
    } //Pass the javascript variables to a dictionary.
    const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
    document.getElementById("Cantidadpin").value = "";
    document.getElementById("Costopin").value = "";
   
    $.ajax({
      type:"POST",
      url: "/Cotizacion",
      traditional:false,
      dataType:'json',
      contentType  : "application/json;charset=utf-8",
      data: JSON.stringify(s)
    });
  }

  function newRowTablehs() {

    var combo = document.getElementById("typeselecths");
    var selected = combo.options[combo.selectedIndex].text;
    var numero = document.getElementById("Cantidadhs").value;
    var costo = document.getElementById("Costohs").value;

    var name_table = document.getElementById("tablahs");

    var row = name_table.insertRow(0 + 1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

    cell1.innerHTML = '<p name="numero_f[]" class="non-margin">' + selected + '</p>';
    cell2.innerHTML = '<p name="codigo_p[]" class="non-margin">' + numero + '</p>';
    cell3.innerHTML = '<p name="codigo_p[]" class="non-margin">' + costo + '</p>';
    typo = 1
  
    const dict_values = {
      selected,
      numero,
      costo,
       typo 
    }
    const dict_values1 = {
      numero
    } //Pass the javascript variables to a dictionary.
    const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
    var numero = document.getElementById("Cantidadhs").value = "";
    document.getElementById("Costohs").value = "";

    $.ajax({
      type:"POST",
      url: "/Cotizacion",
      traditional:false,
      dataType:'json',
      contentType  : "application/json;charset=utf-8",
      data: JSON.stringify(s)
    });
  }
 function newRowTablecom() {

    var combo = document.getElementById("typeselectcom");
    var selected = combo.options[combo.selectedIndex].text;
    var numero = document.getElementById("Cantidadcom").value;
    var costo = document.getElementById("Costocom").value;

    var name_table = document.getElementById("tablacom");

    var row = name_table.insertRow(0 + 1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

    cell1.innerHTML = '<p name="numero_f[]" class="non-margin">' + selected + '</p>';
    cell2.innerHTML = '<p name="codigo_p[]" class="non-margin">' + numero + '</p>';
    cell3.innerHTML = '<p name="codigo_p[]" class="non-margin">' + costo + '</p>';
    typo = 1
  
    const dict_values = {
      selected,
      numero,
      costo,
       typo 
    }
    const dict_values1 = {
      numero
    } //Pass the javascript variables to a dictionary.
    const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
    document.getElementById("Cantidadcom").value = "";
    document.getElementById("Costocom").value = "";
   
    $.ajax({
      type:"POST",
      url: "/Cotizacion",
      traditional:false,
      dataType:'json',
      contentType  : "application/json;charset=utf-8",
      data: JSON.stringify(s)
      
    });
  }

  function newRowTabledes() {

    
    var descripcion = document.getElementById("descripcionproc").value;
   
    var name_table = document.getElementById("tabladesc");

    var row = name_table.insertRow(0 + 1);
    var cell1 = row.insertCell(0);


    cell1.innerHTML = '<p name="numero_f[]" class="non-margin">' + descripcion + '</p>';
   
    typo = 5
    const dict_values = {
      descripcion,
      typo
    }
   //Pass the javascript variables to a dictionary.
    const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
    document.getElementById("descripcionproc").value = "";
   
    $.ajax({
      type:"POST",
      url: "/Cotizacion",
      traditional:false,
      dataType:'json',
      contentType  : "application/json;charset=utf-8",
      data: JSON.stringify(s)
      
    });
  }
 function aceptar(){
  var codigo = document.getElementById("codigo").value;
  var Ubicacion = document.getElementById("Ubicacion").value;
  var marca = 3
   console.log(codigo)
  const dict_values = {
    codigo,
    Ubicacion,
    marca 
  }
  var  URLactual = window.location.href
  const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
  console.log(s)
  $.ajax({
    type:"POST",
    url: URLactual,
    traditional:false,
    dataType:'json',
    contentType  : "application/json;charset=utf-8",
    data: JSON.stringify(s)
  });

 }

 function doSearch() {
  const tableReg = document.getElementById("table-history");

  const searchText = document.getElementById("searchTerm").value.toLowerCase();

  let total = 0;

  // Recorremos todas las filas con contenido de la tabla

  for (let i = 1; i < tableReg.rows.length; i++) {
    // Si el td tiene la clase "noSearch" no se busca en su cntenido

    if (tableReg.rows[i].classList.contains("noSearch")) {
      continue;
    }

    let found = false;

    const cellsOfRow = tableReg.rows[i].getElementsByTagName("td");

    // Recorremos todas las celdas

    for (let j = 0; j < cellsOfRow.length && !found; j++) {
      const compareWith = cellsOfRow[j].innerHTML.toLowerCase();

      // Buscamos el texto en el contenido de la celda

      if (searchText.length == 0 || compareWith.indexOf(searchText) > -1) {
        found = true;

        total++;
       

      }
    }

    if (found) {
      tableReg.rows[i].style.display = "";
    } else {
      // si no ha encontrado ninguna coincidencia, esconde la

      // fila de la tabla

      tableReg.rows[i].style.display = "none";
    }
  }

  // mostramos las coincidencias

  const lastTR = tableReg.rows[tableReg.rows.length - 1];

  const td = lastTR.querySelector("td");

  lastTR.classList.remove("hide", "red");

  if (searchText == "") {
    lastTR.classList.add("hide");
  } else if (total) {
    td.innerHTML =
      "Se ha encontrado " + total + " coincidencia" + (total > 1 ? "s" : "");
  } else {
    lastTR.classList.add("red");

    td.innerHTML = "No se han encontrado coincidencias";
  }
}


