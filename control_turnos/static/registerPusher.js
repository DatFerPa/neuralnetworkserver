var pusher = new Pusher('33da5fe2d909596436d5', {
     cluster: 'eu'
   });

   var channel = pusher.subscribe('my-channel');
   channel.bind('my-event', function(data) {
    //Crear el Toast de bootstrap
    //data.maquinista
    //data.turno
     //alert(JSON.stringify(data));
     identificador = toast + Date.now();
     $("#toastContainer").append("<div id=\" "+ identificador +" \" class=\"toast\" data-autohide=\"false\" role=\"alert\" aria-live=\"assertive\" aria-atomic=\"true\"><div class=\"toast-header\"><strong class=\"mr-auto\">Alarma de hombre muerto</strong><small class=\"text-muted\">just now</small><button type=\"button\" class=\"ml-2 mb-1 close\" data-dismiss=\"toast\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div><div class=\"toast-body\">See? Just like this.</  div></div>");
     $("#"+identificador).toast('show')
   });
