# -*- coding: utf-8 -*-

from .bd import BD
from .ubicacion import Ubicacion
from .historico_plaza import Historico_Plaza
from .destino_activo import Destino_activo
from funciones.notificacion import Notificacion


class Plaza():
    """
    Modelo para el objeto <plaza>.
    Necesita de conexión a la BBDD.
    """

    def __init__(self, BD_setting):
        """
        Constructor del objeto plaza.
        :param BD_setting: string de conexión a la BBDD.
        """
        self.BD_setting = BD_setting

        self.columnas = ('id', 'estado', 'id_ubicacion')

        self.id = -1  # int auto
        self.estado = -1  # int -1 no definido, 0 disponible, 1 ocupada, 2 mal ocupada
        self.id_ubicacion = -1  # int FK ubicacion.id

        self.datos = self.get()

    def get_max_estado(self):
        """
        Función que devuelve el valor máximo a poder tomar el campo estado.
        :return int max_estado:
        """
        return 2

    def get_columnas(self):
        """
        Devuelve una lista con las posibles columnas del objeto plaza.
        :return list columnas:
        """
        return self.columnas

    def get(self):
        """
        Devuelve en un diccionario los valores del objeto.
        :return dict id, direccion, lalitud, longitud, estado:
        """
        return dict(zip(self.columnas, (self.id, self.estado, self.id_ubicacion)))

    def get_all(self):
        """
        Devuelve una lista de plazas.
        :return list dict(plaza):
        """
        consulta = "SELECT * from plaza ORDER BY id ASC;"
        bd = BD(self.BD_setting)
        bd.ejecutar(consulta)
        plazas = bd.filas()
        resultado = []
        for plaza in plazas:
            resultado.append(dict(zip(self.columnas, plaza)))
        return {"num_plazas": len(resultado), "plazas": resultado}

    def get_mal_ocupada(self):
        """
        Devuelve una lista de plazas mal ocupadas.
        :return list dict(plaza):
        """
        consulta = "SELECT * from plaza WHERE estado = 2 ORDER BY id ASC;"
        bd = BD(self.BD_setting)
        bd.ejecutar(consulta)
        plazas = bd.filas()
        resultado = []
        for plaza in plazas:
            resultado.append(dict(zip(self.columnas, plaza)))
        return {"num_plazas": len(resultado), "plazas": resultado}

    def get_historico_mal_ocupada(self):
        """
        Devuelve una lista de historico plazas mal ocupadas.
        :return list dict(historico plaza):
        """
        historico = Historico_Plaza(self.BD_setting)
        return historico.get_ultimo_estado(2)

    def cargar(self, id):
        """
        Carga el objeto plaza
        :param id: id de la plaza a cargar
        :return None:
        """
        bd = BD(self.BD_setting)
        bd.ejecutar("SELECT * from plaza WHERE id = {:d};".format(int(id)))
        datos = bd.fila()
        if datos != None:
            self.id = datos[0]
            self.estado = datos[1]
            self.id_ubicacion = datos[2]

    def existe(self):
        """
        Comprueba si la plaza cargada existe en el sistema
        :return boolean:
        """
        if self.id > 0:
            return True
        return False

    def alta(self, id_ubicacion):
        """
        Crea una nueva plaza en el sistema.
        :param id_ubicacion: int ubicacion
        :return boolean:
        """
        bd = BD(self.BD_setting)
        ubicacion = Ubicacion(self.BD_setting)
        ubicacion.cargar(int(id_ubicacion))
        if not ubicacion.existe():
            return {"estado":False, "id":-1}

        estado = bd.ejecutar("INSERT INTO plaza (estado, id_ubicacion) " \
                             "VALUES (-1, {:d});".format(int(id_ubicacion)))

        estado_devolver = False
        id = -1
        if estado == "INSERT 0 1":
            if ubicacion.add_plaza():
                if ubicacion.add_ocupada():
                    estado_devolver = True
                    bd.ejecutar("SELECT currval('plaza_id_seq');")
                    datos = bd.fila()
                    if datos != None:
                        id = datos[0]

        return {"estado": estado_devolver, "id": id}

    def actualiza_estado(self, nuevo_estado):
        """
        Actualiza el campo estado de la plaza cargada
        :param estado: int menor que get_max_estado()
        :return boolean:
        """
        if self.estado == nuevo_estado:
            return True

        bd = BD(self.BD_setting)
        ubicacion = Ubicacion(self.BD_setting)
        historico = Historico_Plaza(self.BD_setting)

        ubicacion.cargar(self.id_ubicacion)

        # print("actualizar plaza",self.id,"estado",self.estado,"nuevo estado",nuevo_estado)

        estado_consulta = bd.ejecutar(
            "UPDATE plaza SET estado = {:d} WHERE id = {:d};".format(nuevo_estado, int(self.id)))
        # print("estado consulta",estado_consulta)
        if estado_consulta == "UPDATE 1":
            if historico.nuevo(self.id, nuevo_estado):
                if self.estado != 0 and nuevo_estado == 0:
                    # print("elimina ocupada")
                    return ubicacion.elimina_ocupada()
                if self.estado == 0 and nuevo_estado != 0:
                    if ubicacion.add_ocupada():
                        # print("añade ocupada")
                        # print("id_ubicacion",self.id_ubicacion)
                        des_act = Destino_activo(self.BD_setting)
                        tokens = des_act.buscar_id_ubicacion(self.id_ubicacion)
                        # print("tokens", tokens)
                        if len(tokens) != 0:
                            Notific = Notificacion()
                            Notific.notificar(tokens)
                return True

        return False

    def baja(self):
        """
        Elimina la plaza
        :return boolean:
        """
        bd = BD(self.BD_setting)
        estado = bd.ejecutar("DELETE FROM plaza WHERE id = {:d};".format(int(self.id)))
        if estado == "DELETE 1":
            ubicacion = Ubicacion(self.BD_setting)
            ubicacion.cargar(self.id_ubicacion)
            if ubicacion.elimina_plaza():
                if self.estado != 0:
                    return ubicacion.elimina_ocupada()
        return False
