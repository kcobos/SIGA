# -*- coding: utf-8 -*-

import json # Para leer o sacar datos en JSON
import cherrypy # Framework servidor
from modelos.ubicacion import Ubicacion

class UbicacionesController(object):
    """Controlador para ubicaciones"""

    def __init__(self, conexionBD):
        self.modelo = Ubicacion(conexionBD)

    @cherrypy.tools.json_out()
    def get_all(self):
        """
        Devolucion del listado de todas las ubicaciones
        /ubicaciones
        """
        return self.modelo.get_all()

    @cherrypy.tools.json_out()
    def get_ventana(self, lat_min, lat_max, long_min, long_max):
        """
        Devolucion del listado de todas las ubicaciones dentro de una ventana
        /ubicaciones/{lat_min}&{lat_max}/{long_min}&{long_max}
        """
        try:
            latmin = lat_min = float(lat_min)
            latmax = lat_max = float(lat_max)
            longmin = long_min = float(long_min)
            longmax = long_max = float(long_max)
        except:
            raise cherrypy.HTTPError(406, 'Parámetros incorrectos')
        if lat_min > lat_max:
            latmin = lat_max
            latmax = lat_min
        if long_min > long_max:
            longmin = long_max
            longmax = long_min

        return self.modelo.get_all(latmin, latmax, longmin, longmax)

    @cherrypy.tools.json_out()
    def get_cercanas(self, lat, long, grano=0):
        """
        Devolucion del listado de todas las ubicaciones cercanas a una posicion
        /ubicaciones/{lat}&{long}
        """
        try:
            lat = float(lat)
            long = float(long)
        except:
            raise cherrypy.HTTPError(406, 'Parámetros incorrectos')

        return self.modelo.get_cercanas(lat, long, grano)

    @cherrypy.tools.json_out()
    def get(self, id):
        """
        Devolucion de una ubicacion
        /ubicacion/{id}
        """
        self.modelo.cargar(id)
        if self.modelo.existe():
            return self.modelo.get()

        raise cherrypy.HTTPError(404, 'Ubicacion {} no existe'.format(id))

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    # def alta(self, **kwargs):
    def alta(self):
        """
        Da de alta una ubicacion
        /ubicacion/nueva
        """
        input_json = cherrypy.request.json
        if input_json["direccion"] == "" or input_json["latitud"] == "" or input_json["longitud"] == "":
            raise cherrypy.HTTPError(404, 'Faltan parámetros')

        estado = self.modelo.alta(
                                    input_json["direccion"],
                                    input_json["latitud"],
                                    input_json["longitud"],
                                    input_json["observaciones"]
                                    )

        return estado

    def cors_alta(self):
        cherrypy.response.headers["Access-Control-Allow-Headers"] = (
            "content-type, Authorization, X-Requested-With"
        )
        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.headers["Access-Control-Allow-Methods"] = (
            'POST, OPTIONS'
        )
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def modificar(self, id):
        """
        Modifica una ubicacion
        /ubicacion/{id}
        """
        print(id,cherrypy.request.json)
        if cherrypy.request.json["direccion"] == "":
            raise cherrypy.HTTPError(404, 'Faltan parámetros')

        self.modelo.cargar(id)
        if self.modelo.existe():
            estado = self.modelo.modificar(
                                        cherrypy.request.json["direccion"],
                                        cherrypy.request.json["observaciones"]
                                        )

            return {"id": id, "actualizado": estado}
        raise cherrypy.HTTPError(404, 'Ubicación {} no existe'.format(id))

    def cors_modificar(self):
        cherrypy.response.headers["Access-Control-Allow-Headers"] = (
            "content-type, Authorization, X-Requested-With"
        )
        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.headers["Access-Control-Allow-Methods"] = (
            'POST, OPTIONS'
        )
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

    @cherrypy.tools.json_out()
    def eliminar(self, id):
        """
        Elimina una ubicacion
        /ubicacion/{id}
        """
        self.modelo.cargar(id)
        if self.modelo.existe():
            estado = self.modelo.eliminar(id)
            return {"id": id, "eliminado": estado}

        raise cherrypy.HTTPError(404, 'Ubicación {} no existe'.format(id))

    def cors_eliminar(self, id):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        cherrypy.response.headers["Access-Control-Allow-Headers"] = (
            "content-type, Authorization, X-Requested-With"
        )
        cherrypy.response.headers["Access-Control-Allow-Methods"] = (
            'DELETE, OPTIONS'
        )

def add_controlador_ubicacion(dispatcher, conexionBD):
    """
    Añade direcciones URL relacionadas con las ubicaciones en el servidor.
    :param dispatcher: Dispacher del servidor para añadir nuevas direcciones.
    :param conexionBD: Cadena de parámetros de la conexión a la BBDD
    :return: None
    """

    # /ubicaciones (GET)  ->  UbicacionesController.get_all()
    dispatcher.connect(name='ubicaciones',
                       route='/ubicaciones',
                       action='get_all',
                       controller=UbicacionesController(conexionBD),
                       conditions={'method': ['GET']})

    # /ubicaciones/{lat_min}&{lat_max}/{long_min}&{long_max} (GET)  ->  UbicacionesController.get_ventana(lat_min, lat_max, long_min, long_max)
    dispatcher.connect(name='ubicaciones ventana',
                       route='/ubicaciones/{lat_min}&{lat_max}/{long_min}&{long_max}',
                       action='get_ventana',
                       controller=UbicacionesController(conexionBD),
                       conditions={'method': ['GET']})

    # /ubicaciones/{lat}&{long} (GET)  ->  UbicacionesController.get_cercanas(lat, long)
    dispatcher.connect(name='ubicaciones cercanas',
                       route='/ubicaciones/{lat}&{long}',
                       action='get_cercanas',
                       controller=UbicacionesController(conexionBD),
                       conditions={'method': ['GET']})
    # /ubicaciones/{lat}&{long}/{grano} (GET)  ->  UbicacionesController.get_cercanas(lat, long, grano)
    dispatcher.connect(name='ubicaciones cercanas',
                       route='/ubicaciones/{lat}&{long}/{grano}',
                       action='get_cercanas',
                       controller=UbicacionesController(conexionBD),
                       conditions={'method': ['GET']})

    # /ubicacion/{id} (GET)  ->  UbicacionesController.get(id)
    dispatcher.connect(name='ubicacion',
                       route='/ubicacion/{id}',
                       action='get',
                       controller=UbicacionesController(conexionBD),
                       conditions={'method': ['GET']})

    # /ubicacion/nueva (POST)  ->  UbicacionesController.alta() recibe JSON
    dispatcher.connect(name='alta ubicacion',
                       route='/ubicacion/nueva',
                       action='alta',
                       controller=UbicacionesController(conexionBD),
                       conditions={'method': ['POST']})
    dispatcher.connect(name='cors alta ubicacion',
                       route='/ubicacion/nueva',
                       action='cors_alta',
                       controller=UbicacionesController(conexionBD),
                       conditions={'method': ['OPTIONS']})

    # /ubicacion/{id} (DELETE)  ->  UbicacionesController.eliminar(id):
    dispatcher.connect(name='eliminar ubicacion',
                       route='/ubicacion/{id}',
                       action='eliminar',
                       controller=UbicacionesController(conexionBD),
                       conditions={'method': ['DELETE']})
    dispatcher.connect(name='cors eliminar ubicacion',
                       route='/ubicacion/{id}',
                       action='cors_eliminar',
                       controller=UbicacionesController(conexionBD),
                       conditions={'method': ['OPTIONS']})

    # /ubicacion/{id} (POST)  ->  UbicacionesController.modificar() recibe JSON
    dispatcher.connect(name='modificar ubicacion',
                       route='/ubicacion/{id}',
                       action='modificar',
                       controller=UbicacionesController(conexionBD),
                       conditions={'method': ['POST']})
    dispatcher.connect(name='cors alta modificar',
                       route='/ubicacion/{id}',
                       action='cors_modificar',
                       controller=UbicacionesController(conexionBD),
                       conditions={'method': ['OPTIONS']})
