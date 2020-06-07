var pusher = new Pusher('33da5fe2d909596436d5', {
     cluster: 'eu'
   });

   var channel = pusher.subscribe('my-channel');
   channel.bind('my-event', function(data) {
    //Crear el Toast de bootstrap
    //data.maquinista
    //data.turno
     //alert(JSON.stringify(data));
     let identificador = "alert" + Date.now();
     $(".container").prepend("<div class=\"alert alert-secondary alert-dismissible fade show\" role=\"alert\"> <h4 class=\"alert-heading\"> Un maquinista ha tenido un accidente </h4> El maquinista <a href=\" {{ url_for('webRoutes.logsTurno',"+data.nombreFichero+","+data.turno+","+data.fecha+") }} \" class=\"alert-link\">"+ data.nombre +"ha sufrido un accidente en el turno"+ data.turno+"</a>  <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>");


   });
