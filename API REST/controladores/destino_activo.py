# -*- coding: utf-8 -*-

import json # Para leer o sacar datos en JSON
import cherrypy # Framework servidor
from modelos.destino_activo import Destino_activo

class DestinoActivoController(object):
    """Controlador para destino activos -notificaciones-"""

    def __init__(self, conexionBD):
        self.modelo = Destino_activo(conexionBD)

    @cherrypy.tools.json_out()
    def get_all(self):
        """
        Devolucion del listado de todos los destinos activos
        /destinos_activos
        """
        return self.modelo.get_all()

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def alta(self):
        """
        Da de alta un destino activo
        /destino_activo/nueva
        """
        print("alta nueva destino activo")
        input_json = cherrypy.request.json
        id_ubicacion = input_json["id_ubicacion"]
        token = input_json["token"]
        print("alta destino activo id_ubicacion",id_ubicacion)
        if token == "" or not isinstance(id_ubicacion, int):
            raise cherrypy.HTTPError(404, 'Error en parametros.')
        estado = self.modelo.alta(id_ubicacion, token)
        return {"estado": estado}

    def cors_alta(self):
        cherrypy.response.headers["Access-Control-Allow-Headers"] = (
            "content-type, Authorization, X-Requested-With"
        )
        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.headers["Access-Control-Allow-Methods"] = (
            'POST, OPTIONS'
        )
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

    @cherrypy.tools.json_out()
    def eliminar(self, token):
        """
        Elimina un destino activo
        /destino_activo/{uid}
        """
        estado = self.modelo.baja(token)
        return {"token": token, "eliminado": estado}


    def cors_eliminar(self, token):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        cherrypy.response.headers["Access-Control-Allow-Headers"] = (
            "content-type, Authorization, X-Requested-With"
        )
        cherrypy.response.headers["Access-Control-Allow-Methods"] = (
            'DELETE, OPTIONS'
        )

def add_controlador_destino_activo(dispatcher, conexionBD):
    """
    Añade direcciones URL relacionadas con las acreditaciones en el servidor.
    :param dispatcher: Dispacher del servidor para añadir nuevas direcciones.
    :param conexionBD: Cadena de parámetros de la conexión a la BBDD
    :return: None
    """

    # /destinos_activos (GET)  ->  DestinoActivoController.get_all()
    # dispatcher.connect(name='dectinos activos',
    #                    route='/destinos_activos',
    #                    action='get_all',
    #                    controller=DestinoActivoController(conexionBD),
    #                    conditions={'method': ['GET']})

    # /destino_activo/nueva (POST)  ->  DestinoActivoController.alta() recibe JSON
    dispatcher.connect(name='alta destino activo',
                       route='/destino_activo/nueva',
                       action='alta',
                       controller=DestinoActivoController(conexionBD),
                       conditions={'method': ['POST']})
    dispatcher.connect(name='cors alta destino activo',
                       route='/destino_activo/nueva',
                       action='cors_alta',
                       controller=DestinoActivoController(conexionBD),
                       conditions={'method': ['OPTIONS']})

    # /destino_activo/{token} (DELETE)  ->  DestinoActivoController.eliminar(token):
    dispatcher.connect(name='eliminar destino activo',
                       route='/destino_activo/{token}',
                       action='eliminar',
                       controller=DestinoActivoController(conexionBD),
                       conditions={'method': ['DELETE']})
    dispatcher.connect(name='cors eliminar destino activo',
                       route='/destino_activo/{token}',
                       action='cors_eliminar',
                       controller=DestinoActivoController(conexionBD),
                       conditions={'method': ['OPTIONS']})
