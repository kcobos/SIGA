function get_alertas() {
  $.get("http://192.168.1.x:8080/plazas/mal_ocupadas").then(function(data) {
    for (var i = 0; i < data.num_registros; i++) {
      var fecha = data.registros[i].tiempo.split(" ")[0].split("-")[2] + "/" +
        data.registros[i].tiempo.split(" ")[0].split("-")[1] + "/" +
        data.registros[i].tiempo.split(" ")[0].split("-")[0];
      var hora = data.registros[i].tiempo.split(" ")[1].substring(0, 5);
      muestra_alerta("Plaza #" + data.registros[i].id_plaza + " mal ocupada desde las " + hora + " horas del " + fecha)
    }
  });
}

function muestra_alerta(msg) {
  $.notify({
    // options
    message: msg,
    url: 'plazas.html',
    target: '_self'
  }, {
    // settings
    element: 'body',
    newest_on_top: true,
    type: 'warning'
  });
}

$(function() {
  get_alertas();
  setInterval(get_alertas, 15000);
});
