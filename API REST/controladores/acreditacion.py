# -*- coding: utf-8 -*-

import json # Para leer o sacar datos en JSON
import cherrypy # Framework servidor
from modelos.acreditacion import Acreditacion

class AcreditacionesController(object):
    """Controlador para acreditaciones"""

    def __init__(self, conexionBD):
        self.modelo = Acreditacion(conexionBD)

    @cherrypy.tools.json_out()
    def get_all(self):
        """
        Devolucion del listado de todas las acreditaciones
        /plazas
        """
        return self.modelo.get_all()

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def alta(self):
        """
        Da de alta una acreditacion
        /acreditacion/nueva
        """
        input_json = cherrypy.request.json
        uid = input_json["uid"].replace(".", " ")
        if uid == "":
            raise cherrypy.HTTPError(404, 'Se necesita uid.')
        estado = self.modelo.alta(uid)
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
    def existe(self, uid):
        """
        Existe acreditacion
        /acreditacion/{uid}
        """
        self.modelo.cargar(uid)
        if self.modelo.existe():
            return {"existe": True}

        raise cherrypy.HTTPError(404, 'Acreditacion {} no existe'.format(uid))

    @cherrypy.tools.json_out()
    def eliminar(self, uid):
        """
        Elimina una acreditacion
        /acreditacion/{uid}
        """
        self.modelo.cargar(uid)
        if self.modelo.existe():
            estado = self.modelo.baja()
            return {"id": uid, "eliminado": estado}

        raise cherrypy.HTTPError(404, 'Acreditación {} no existe'.format(uid))

    def cors_eliminar(self, uid):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        cherrypy.response.headers["Access-Control-Allow-Headers"] = (
            "content-type, Authorization, X-Requested-With"
        )
        cherrypy.response.headers["Access-Control-Allow-Methods"] = (
            'DELETE, OPTIONS'
        )

def add_controlador_acreditacion(dispatcher, conexionBD):
    """
    Añade direcciones URL relacionadas con las acreditaciones en el servidor.
    :param dispatcher: Dispacher del servidor para añadir nuevas direcciones.
    :param conexionBD: Cadena de parámetros de la conexión a la BBDD
    :return: None
    """

    # /acreditacioness (GET)  ->  AcreditacionesController.get_all()
    dispatcher.connect(name='acreditaciones',
                       route='/acreditaciones',
                       action='get_all',
                       controller=AcreditacionesController(conexionBD),
                       conditions={'method': ['GET']})

    # /acreditacion/nueva (POST)  ->  AcreditacionesController.alta() recibe JSON
    dispatcher.connect(name='alta acreditacion',
                       route='/acreditacion/nueva',
                       action='alta',
                       controller=AcreditacionesController(conexionBD),
                       conditions={'method': ['POST']})
    dispatcher.connect(name='cors alta acreditacion',
                       route='/acreditacion/nueva',
                       action='cors_alta',
                       controller=AcreditacionesController(conexionBD),
                       conditions={'method': ['OPTIONS']})

    # /acreditacion/{uid} (GET)  ->  AcreditacionesController.existe(uid)
    dispatcher.connect(name='existe acreditacion',
                       route='/acreditacion/{uid}',
                       action='existe',
                       controller=AcreditacionesController(conexionBD),
                       conditions={'method': ['GET']})

    # /acreditacion/{id} (DELETE)  ->  AcreditacionesController.eliminar(uid):
    dispatcher.connect(name='eliminar acreditacion',
                       route='/acreditacion/{uid}',
                       action='eliminar',
                       controller=AcreditacionesController(conexionBD),
                       conditions={'method': ['DELETE']})
    dispatcher.connect(name='cors eliminar acreditacion',
                       route='/acreditacion/{uid}',
                       action='cors_eliminar',
                       controller=AcreditacionesController(conexionBD),
                       conditions={'method': ['OPTIONS']})
