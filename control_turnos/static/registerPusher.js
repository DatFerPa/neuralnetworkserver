var pusher = new Pusher('33da5fe2d909596436d5', {
     cluster: 'eu'
   });

   var channel = pusher.subscribe('my-channel');
   channel.bind('my-event', function(data) {
    //Crear el Toast de bootstrap
    //data.maquinista
    //data.turno
     alert(JSON.stringify(data));
   });
