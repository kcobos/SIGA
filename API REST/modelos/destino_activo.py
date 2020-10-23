# -*- coding: utf-8 -*-

from .bd import BD
from .ubicacion import Ubicacion

class Destino_activo():
    """
    Modelo para el objeto <destino_activo>.
    Necesita de conexión a la BBDD.
    """

    def __init__(self, BD_setting):
        """
        Constructor del objeto destino_activo.
        :param BD_setting: string de conexión a la BBDD.
        """
        self.BD_setting = BD_setting

        self.columnas = ('id_ubicacion','token')


    def get_columnas(self):
        """
        Devuelve una lista con las posibles columnas del objeto destino_activo.
        :return list columnas:
        """
        return self.columnas

    def get_all(self):
        """
        Devuelve una lista de destinos activos.
        :return list dict(destino_activo):
        """
        consulta = "SELECT * from destino_activo;"
        bd = BD(self.BD_setting)
        bd.ejecutar(consulta)
        destino_activos = bd.filas()
        resultado = []
        for destino_activo in destino_activos:
            resultado.append(dict(zip(self.columnas, destino_activo)))
        return {"num_destino_activos":len(resultado),"destino_activo":resultado}

    def buscar_id_ubicacion(self,id_ubicacion):
        """
        Devuelve listado de tokens de APP que van a la ubicacion
        :param id_ubicacion: identificador de ubicacion a buscar en destinos activos
        :return list(tokens):
        """
        bd = BD(self.BD_setting)
        bd.ejecutar("SELECT * from destino_activo WHERE id_ubicacion = '{:d}';".format(int(id_ubicacion)))
        destino_activos = bd.filas()
        resultado = []
        for destino_activo in destino_activos:
            resultado.append(destino_activo[1].strip())
        return resultado


    def alta(self, id_ubicacion, token):
        """
        Crea un nuevo registro de destino activo
        :param id_ubicacion: int identificacion de ubicacion de destino
        :param token: string token de notificacion de la APP
        :return boolean:
        """
        bd = BD(self.BD_setting)
        ubicacion = Ubicacion(self.BD_setting)
        ubicacion.cargar(id_ubicacion)
        if not ubicacion.existe():
            return False

        estado = bd.ejecutar("INSERT INTO destino_activo (id_ubicacion, token) " \
                           "VALUES ({:d},'{:s}');".format(int(id_ubicacion),str(token)))
        if estado == "INSERT 0 1":
            return True
        return False

    def baja(self, token):
        """
        Elimina registro de destino activo
        :param token: string token de notificacion de la APP
        :return boolean:
        """
        bd = BD(self.BD_setting)
        estado = bd.ejecutar("DELETE FROM destino_activo WHERE token = '{:s}';".format(str(token)))
        if estado == "DELETE 1":
            return True
        return False
