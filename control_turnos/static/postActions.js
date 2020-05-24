function nuevoMaquinista(){
  $.ajax({
    method:"POST",
    url:"https://servidorhombremuerto.herokuapp.com/nuevoMaquinista/",
    data: {"nombre": $("#inputNombre").val()}
  }).done(function(msg){
    if("ok_maquinsita".equals(msg)){
      $(".container").prepend("<div class=\"alert alert-success alert-dismissible fade show\" role=\"alert\">El maquinista <strong>se ha ñadido</strong><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>");
    }else{
      $(".container").prepend("<div class=\"alert alert-danger alert-dismissible fade show\" role=\"alert\">El maquinista <strong>ya se encuentra</strong>en el sistema<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>");
    }
  });
}

function quitarMaquinista(){
  $.ajax({
    method:"POST",
    url:"https://servidorhombremuerto.herokuapp.com/quitarMaquinista/",
    data: {"nombre": $("#inputNombre").val()}
  }).done(function(msg){
    if("ok_maquinsita".equals(msg)){
      $(".container").prepend("<div class=\"alert alert-success alert-dismissible fade show\" role=\"alert\">El maquinista <strong>se ha eliminado</strong><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>");
    }else{
      $(".container").prepend("<div class=\"alert alert-danger alert-dismissible fade show\" role=\"alert\">El maquinista <strong>no se encuentra</strong>en el sistema<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>");
    }
  });
}

function nuevoTurno(){
  $.ajax({
    method:"POST",
    url:"https://servidorhombremuerto.herokuapp.com/nuevoTurno/",
    data: {"nombreTurno" : $("#nombreTurno").val() , "nombreMaquina" : $("#nombreMaquina").val()}
  }).done(function(msg){
    if("ok_turno".equals(msg)){
      $(".container").prepend("<div class=\"alert alert-success alert-dismissible fade show\" role=\"alert\">El turno <strong>se ha añadido</strong><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>");
    }else{
      $(".container").prepend("<div class=\"alert alert-danger alert-dismissible fade show\" role=\"alert\">El turno <strong>ya se encuentra</strong>en el sistema<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>");
    }
  });
}

function quitarTurno(){
  $.ajax({
    method:"POST",
    url:"https://servidorhombremuerto.herokuapp.com/quitarTurno/",
    data: {"nombreTurno" : $("#inputNombre").val() , "nombreMaquina" : $("#nombreMaquina").val()}
  }).done(function(msg){
    if("ok_turno".equals(msg)){
      $(".container").prepend("<div class=\"alert alert-success alert-dismissible fade show\" role=\"alert\">El turno <strong>se ha eliminado</strong><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>");
    }else{
      $(".container").prepend("<div class=\"alert alert-danger alert-dismissible fade show\" role=\"alert\">El turno <strong>no se encuentra</strong>en el sistema<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>");
    }
  });
}
