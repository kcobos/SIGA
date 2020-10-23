# -*- coding: utf-8 -*-

import cherrypy # Framework servidor

from modelos.plaza import Plaza

class PlazasController(object):
    """Controlador para plazas"""

    def __init__(self, conexionBD):
        self.modelo = Plaza(conexionBD)

    @cherrypy.tools.json_out()
    def get_all(self):
        """
        Devolucion del listado de todas las plazas
        /plazas
        """
        return self.modelo.get_all()

    @cherrypy.tools.json_out()
    def get(self, id):
        """
        Devolucion de una plaza
        /plaza/{id}
        """
        self.modelo.cargar(id)
        if self.modelo.existe():
            return self.modelo.get()

        raise cherrypy.HTTPError(404, 'Plaza {} no existe'.format(id))

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def alta(self):
        """
        Da de alta una plaza
        /plaza/nueva
        """
        input_json = cherrypy.request.json
        # print(input_json)
        if input_json["id_ubicacion"] == "" or input_json["id_ubicacion"] == -1:
            raise cherrypy.HTTPError(404, 'No existe la ubicacion')
        return self.modelo.alta(input_json["id_ubicacion"])

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
    def actualizarEstado(self, id, estado):
        """
        Actualiza campo estado de una plaza
        /plaza/{id}/estado/{estado}
        """
        if not estado.isdigit():
            raise cherrypy.HTTPError(406, 'Estado {} no valido'.format(estado))
        estado = int(estado)
        if estado < 0 or estado > self.modelo.get_max_estado():
            raise cherrypy.HTTPError(406, 'Estado {} no valido'.format(estado))

        self.modelo.cargar(id)
        if not self.modelo.existe():
            raise cherrypy.HTTPError(404, 'Plaza {} no existe'.format(id))

        estado = self.modelo.actualiza_estado(estado)

        return {"id":id, "actualizado":estado}

    @cherrypy.tools.json_out()
    def eliminar(self, id):
        """
        Elimina una plaza
        /plaza/{id}
        """
        self.modelo.cargar(id)
        if self.modelo.existe():
            estado = self.modelo.baja()
            return {"id":id, "eliminado":estado}

        raise cherrypy.HTTPError(404, 'Plaza {} no existe'.format(id))

    def cors_eliminar(self, id):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        cherrypy.response.headers["Access-Control-Allow-Headers"] = (
            "content-type, Authorization, X-Requested-With"
        )
        cherrypy.response.headers["Access-Control-Allow-Methods"] = (
            'DELETE, OPTIONS'
        )

    @cherrypy.tools.json_out()
    def get_historico_mal_ocupada(self):
        """
        Devolucion del listado del ultimo estado mal ocupada
        /plazas/mal_ocupadas
        """
        return self.modelo.get_historico_mal_ocupada()


def add_controlador_plaza(dispatcher, conexionBD):
    """
    Añade direcciones URL relacionadas con las plazas en el servidor.
    :param dispatcher: Dispacher del servidor para añadir nuevas direcciones.
    :param conexionBD: Cadena de parámetros de la conexión a la BBDD
    :return: None
    """

    # /plazas (GET)  ->  PlazasController.get_all()
    dispatcher.connect(name='plazas',
                       route='/plazas',
                       action='get_all',
                       controller=PlazasController(conexionBD),
                       conditions={'method': ['GET']})

    # /plaza/{id} (GET)  ->  PlazasController.get(id)
    dispatcher.connect(name='plaza',
                       route='/plaza/{id}',
                       action='get',
                       controller=PlazasController(conexionBD),
                       conditions={'method': ['GET']})

    # /plaza/nueva (POST)  ->  PlazasController.alta() recibe JSON
    dispatcher.connect(name='alta plaza',
                       route='/plaza/nueva',
                       action='alta',
                       controller=PlazasController(conexionBD),
                       conditions={'method': ['POST']})
    dispatcher.connect(name='cors alta plaza',
                       route='/plaza/nueva',
                       action='cors_alta',
                       controller=PlazasController(conexionBD),
                       conditions={'method': ['OPTIONS']})

    # /plaza/{id}/estado/{estado} (PUT)  ->  PlazasController.actualizarEstado(id, estado):
    dispatcher.connect(name='actualizar estado plaza',
                       route='/plaza/{id}/estado/{estado}',
                       action='actualizarEstado',
                       controller=PlazasController(conexionBD),
                       conditions={'method': ['PUT']})

    # /plaza/{id} (DELETE)  ->  PlazasController.eliminar(id):
    dispatcher.connect(name='eliminar plaza',
                       route='/plaza/{id}',
                       action='eliminar',
                       controller=PlazasController(conexionBD),
                       conditions={'method': ['DELETE']})
    dispatcher.connect(name='cors eliminar plaza',
                       route='/plaza/{id}',
                       action='cors_eliminar',
                       controller=PlazasController(conexionBD),
                       conditions={'method': ['OPTIONS']})

    # /plazas/mal_ocupadas (GET)  ->  PlazasController.get_all()
    dispatcher.connect(name='plazas mal ocupadas',
                       route='/plazas/mal_ocupadas',
                       action='get_historico_mal_ocupada',
                       controller=PlazasController(conexionBD),
                       conditions={'method': ['GET']})