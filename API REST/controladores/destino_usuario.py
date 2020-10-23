# -*- coding: utf-8 -*-

import json # Para leer o sacar datos en JSON
import cherrypy # Framework servidor
from modelos.destino_usuarios import Destino_usuarios

class DestinoUsuarioController(object):
    """Controlador para destino usuario -notificaciones-"""

    def __init__(self, conexionBD):
        self.modelo = Destino_usuarios(conexionBD)

    @cherrypy.tools.json_out()
    def get_all(self):
        """
        Devolucion del listado de todos los destinos de los usuarios
        /destinos_usuario
        """
        return self.modelo.get_all()

    @cherrypy.tools.json_out()
    def alta(self, lat, long):
        """
        Da de alta un destino activo
        /destino_usuario/nueva
        """
        estado = self.modelo.nuevo(lat, long)

        return {"estado": estado}

def add_controlador_destino_usuario(dispatcher, conexionBD):
    """
    Añade direcciones URL relacionadas con las acreditaciones en el servidor.
    :param dispatcher: Dispacher del servidor para añadir nuevas direcciones.
    :param conexionBD: Cadena de parámetros de la conexión a la BBDD
    :return: None
    """

    # /destinos_usuarios (GET)  ->  DestinoUsuarioController.get_all()
    # dispatcher.connect(name='dectinos activos',
    #                    route='/destinos_usuarios',
    #                    action='get_all',
    #                    controller=DestinoUsuarioController(conexionBD),
    #                    conditions={'method': ['GET']})

    # /destinos_usuario/nueva{lat}&{long} (PUT)  ->  DestinoUsuarioController.alta()
    dispatcher.connect(name='alta destino usuario',
                       route='/destinos_usuario/{lat}&{long}',
                       action='alta',
                       controller=DestinoUsuarioController(conexionBD),
                       conditions={'method': ['PUT']})