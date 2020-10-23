# -*- coding: utf-8 -*-

from .bd import BD


class Historico_Plaza():
    """
    Modelo para el objeto <historico_plaza>.
    Necesita de conexión a la BBDD.
    """

    def __init__(self, BD_setting):
        """
        Constructor del objeto historico_plaza.
        :param BD_setting: string de conexión a la BBDD.
        """
        self.BD_setting = BD_setting

        self.columnas = ('tiempo', 'id_plaza', 'estado')

    def get_columnas(self):
        """
        Devuelve una lista con las posibles columnas del objeto historico_plaza.
        :return list columnas:
        """
        return self.columnas

    def nuevo(self, id_plaza, estado):
        """
        Crea un nuevo registro en el historico de plaza en el sistema.
        :param id_plaza: int id de la plaza asociada
        :param estado: int estado nuevo de la plaza
        :return boolean:
        """
        bd = BD(self.BD_setting)
        estado = bd.ejecutar("INSERT INTO historico_plaza (tiempo, id_plaza, estado) " \
                             "VALUES (now(),{:d},{:d});".format(int(id_plaza), int(estado)))
        if estado == "INSERT 0 1":
            return True
        return False

    def get_ultimo_estado(self, estado=None):
        """
        Devuelve una lista (id_plaza, tiempo, estado) con el último estado en el historico.
        :param estado: int estado específico a buscar
        :return list dict(historico_plaza):
        """
        bd = BD(self.BD_setting)
        resultado = []
        if estado == None:
            bd.ejecutar("SELECT DISTINCT ON (id_plaza) tiempo, id_plaza, estado " \
                        "FROM historico_plaza " \
                        "ORDER BY id_plaza, tiempo DESC")
            registros = bd.filas()
            for r in registros:
                resultado.append(dict(zip(self.columnas, r)))
            return {"num_registros": len(resultado), "registros": resultado}
        else:
            bd.ejecutar("SELECT * FROM ( " \
                        "SELECT DISTINCT ON (id_plaza) tiempo, id_plaza, estado " \
                        "FROM historico_plaza " \
                        "ORDER BY id_plaza, tiempo DESC " \
                        ") ultimo_estado " \
                        "WHERE estado = {:d};".format(int(estado)))
            registros = bd.filas()
            for r in registros:
                resultado.append(dict(zip(self.columnas, (r[0].__str__(), r[1], r[2]))))
            return {"num_registros": len(resultado), "registros": resultado}
