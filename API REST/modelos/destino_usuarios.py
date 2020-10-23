# -*- coding: utf-8 -*-

from .bd import BD


class Destino_usuarios():
    """
    Modelo para el objeto <destino_usuarios>.
    Necesita de conexión a la BBDD.
    """

    def __init__(self, BD_setting):
        """
        Constructor del objeto destino_usuarios.
        :param BD_setting: string de conexión a la BBDD.
        """
        self.BD_setting = BD_setting

        self.columnas = ('latitud', 'longitud', 'tiempo')

    def get_columnas(self):
        """
        Devuelve una lista con las posibles columnas del objeto destino_usuarios.
        :return list columnas:
        """
        return self.columnas

    def nuevo(self, latitud, longitud):
        """
        Crea un nuevo registro de destino en el sistema.
        :param latitud: float latitud del destino
        :param longitud: float longitud del destino
        :return boolean:
        """
        bd = BD(self.BD_setting)
        estado = bd.ejecutar("INSERT INTO destino_usuarios (latitud, longitud, tiempo) " \
                             "VALUES ({:f},{:f},now());".format(float(latitud), float(longitud)))
        if estado == "INSERT 0 1":
            return True
        return False
