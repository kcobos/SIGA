# -*- coding: utf-8 -*-

from .bd import BD

class Acreditacion():
    """
    Modelo para el objeto <acreditacion>.
    Necesita de conexión a la BBDD.
    """

    def __init__(self, BD_setting):
        """
        Constructor del objeto acreditacion.
        :param BD_setting: string de conexión a la BBDD.
        """
        self.BD_setting = BD_setting

        self.columnas = ('uid')

        self.uid = ""  # string

        self.datos = self.get()

    def get_columnas(self):
        """
        Devuelve una lista con las posibles columnas del objeto acreditacion.
        :return list columnas:
        """
        return self.columnas

    def get(self):
        """
        Devuelve en un diccionario los valores del objeto.
        :return dict uid:
        """
        return dict(zip(self.columnas, (self.uid)))

    def get_all(self):
        """
        Devuelve una lista de acreditaciones.
        :return list dict(acreditacion):
        """
        consulta = "SELECT * from acreditacion;"
        bd = BD(self.BD_setting)
        bd.ejecutar(consulta)
        acreditaciones = bd.filas()
        resultado = []
        for acreditacion in acreditaciones:
            resultado.append({self.columnas: acreditacion})
        return {"num_acreditaciones":len(resultado),"acreditaciones":resultado}

    def cargar(self,uid):
        """
        Carga el objeto acreditacion
        :param uid: uid de la acreditacion a cargar
        :return None:
        """
        bd = BD(self.BD_setting)
        bd.ejecutar("SELECT * from acreditacion WHERE uid = '{:s}';".format(str(uid)))
        datos = bd.fila()
        if datos != None:
            self.uid = datos[0]
        else:
            self.uid = ""

    def existe(self):
        """
        Comprueba si la acreditacion existe en el sistema
        :param uid: uid de la acreditacion a comprobar
        :return None:
        """
        # bd = BD(self.BD_setting)
        # bd.ejecutar("SELECT * from acreditacion WHERE uid = '{:s}';".format(str(uid)))
        # datos = bd.fila()
        # if datos != None:
        #     return True
        # return False
        if self.uid == "":
            return False
        return True

    def alta(self, uid):
        """
        Crea una nueva acreditación en el sistema.
        :param uid: string uid de la nueva tarjeta
        :return boolean:
        """
        bd = BD(self.BD_setting)
        estado = bd.ejecutar("INSERT INTO acreditacion (uid) " \
                           "VALUES ('{:s}');".format(str(uid)))
        if estado == "INSERT 0 1":
            return True
        return False

    def baja(self):
        """
        Elimina la acreditacion
        :return boolean:
        """
        bd = BD(self.BD_setting)
        estado = bd.ejecutar("DELETE FROM acreditacion WHERE uid = '{:s}';".format(str(self.uid)))
        if estado == "DELETE 1":
            return True
        return False
