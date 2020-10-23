#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API REST Gestor de aparcamientos para personas con movilidad reducida
"""

import json # Para leer o sacar datos en JSON
import cherrypy # Framework servidor
# import cherrypy_cors

global conexionBD
conexionBD = "dbname='' user='' host='localhost' password=''"

from controladores.plaza import add_controlador_plaza
from controladores.acreditacion import add_controlador_acreditacion
from controladores.ubicacion import add_controlador_ubicacion
from controladores.destino_activo import add_controlador_destino_activo
from controladores.destino_usuario import add_controlador_destino_usuario

def jsonify_error(status, message, traceback, version):

    """
    Convierte el error en un JSON
    """

    cherrypy.response.headers['Content-Type'] = 'application/json'
    response_body = json.dumps(
        {
            'error': {
                'http_status': status,
                'message': message
                # 'traceback': traceback
            }
        })

    cherrypy.response.status = status

    return response_body

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Headers"] = (
        "content-type, Authorization, X-Requested-With"
    )

    cherrypy.response.headers["Access-Control-Allow-Methods"] = (
        'GET, POST, PUT, DELETE, OPTIONS'
    )


if __name__ == '__main__':
    # Gestor de rutas
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    # Aquí las llamadas para incluir controladores
    add_controlador_plaza(dispatcher, conexionBD)
    add_controlador_acreditacion(dispatcher, conexionBD)
    add_controlador_ubicacion(dispatcher, conexionBD)
    add_controlador_destino_activo(dispatcher, conexionBD)
    add_controlador_destino_usuario(dispatcher, conexionBD)

    # cherrypy_cors.install()

    config = {
        '/': {
            'request.dispatch': dispatcher,
            'error_page.default': jsonify_error,
            'tools.CORS.on': True,
            # 'tools.response_headers.on': True,
            # 'tools.response_headers.headers': [('Content-Type', 'application/json')],
            # 'cors.expose.on': True,
        },
    }

    cherrypy.tree.mount(root=None, config=config)
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        'server.thread_pool': 30,
                            })
    cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
    cherrypy.engine.start()
    cherrypy.engine.block()
