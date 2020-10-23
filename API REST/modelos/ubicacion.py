# -*- coding: utf-8 -*-
from symbol import lambdef

from .bd import BD
from .destino_usuarios import Destino_usuarios

class Ubicacion():
    """
    Modelo para el objeto <ubicacion>.
    Necesita de conexión a la BBDD.
    """

    def __init__(self, BD_setting):
        """
        Constructor del objeto ubicacion.
        :param BD_setting: string de conexión a la BBDD.
        """
        self.BD_setting = BD_setting

        self.columnas = ('id', 'direccion', 'latitud', 'longitud', 'plazas_totales', 'plazas_ocupadas', 'observaciones')

        self.id = -1  # int auto
        self.direccion = ""  # string
        self.latitud = 0 # float
        self.longitud = 0 # float
        self.plazas_totales = -1 # int
        self.plazas_ocupadas = -1 # int
        self.observaciones = "" # string

        self.datos = self.get()

    def get_columnas(self):
        """
        Devuelve una lista con las posibles columnas del objeto ubicacion.
        :return list columnas:
        """
        return self.columnas

    def get(self):
        """
        Devuelve en un diccionario los valores del objeto.
        :return dict id, direccion, lalitud, longitud, plazas_totales, plazas_ocupadas, observaciones:
        """
        return dict(zip(self.columnas,
            (
                self.id,
                self.direccion,
                self.latitud,
                self.longitud,
                self.plazas_totales,
                self.plazas_ocupadas,
                self.observaciones
            )))

    def get_all(self, lat_min=None, lat_max=None, long_min=None, long_max=None):
        """
        Devuelve una lista de ubicaciones.
        Si no se pasan parámetros, son todas.
        Si se pasan parámetros, las que estén en el interior de la ventana.
        :param lat_min: latitud esquina inferior derecha.
        :param lat_max: latitud esquina superior izquierda.
        :param long_min: longitud esquina superior izquierda.
        :param long_max: longitud esquina inferion derecha.
        :return list dict(plaza):
        """
        if lat_min is None or lat_max is None or long_min is None or long_max is None:
            consulta = "SELECT id,direccion,latitud,longitud,plazas_totales,plazas_ocupadas,observaciones "\
                       "from ubicacion ORDER BY id ASC;"
        else:
            consulta = "SELECT id,direccion,latitud,longitud,plazas_totales,plazas_ocupadas,observaciones "\
                       "FROM ubicacion WHERE (latitud BETWEEN {:f} AND {:f}) " \
                       "AND (longitud BETWEEN {:f} AND {:f}) ORDER BY id ASC;".\
                           format(float(lat_min), float(lat_max), float(long_min), float(long_max))
        # print(consulta)
        bd = BD(self.BD_setting)
        bd.ejecutar(consulta)
        ubicaciones = bd.filas()
        resultado = []
        ubicaciones = [tuple("" if v is None else v for v in f) for f in ubicaciones]
        # print(ubicaciones)
        for ubicacion in ubicaciones:
            resultado.append(dict(zip(self.columnas, ubicacion)))
        return {"num_ubicaciones":len(resultado),"ubicaciones":resultado}

    def get_cercanas(self, lat, long, grano=0):
        """
        Devuelve una lista de ubicaciones cercanas a una posicion ordenadas por distancia.
        :param lat: latitud posicion.
        :param long: longitud posicion.
        :param grano: distancia cluster
        :return list dict(plaza):
        """

        # desti = Destino_usuarios(self.BD_setting)
        # desti.nuevo(lat, long)

        consulta = "SELECT id,direccion,latitud,longitud,plazas_totales,plazas_ocupadas,observaciones, "\
                       "ST_Distance_Sphere(ST_GeomFromText('POINT({:f} {:f})',4326),geom) as distancia " \
                       "FROM ubicacion " \
                       "WHERE plazas_totales > 0 " \
                       "ORDER BY distancia ASC".\
                       format(float(long), float(lat))
        print(consulta)
        bd = BD(self.BD_setting)
        bd.ejecutar(consulta)
        ubicaciones = bd.filas()
        resultado = []
        ubicaciones = [tuple("" if v is None else v for v in f) for f in ubicaciones]
        # print(ubicaciones)
        grano = int(grano)
        print(grano)
        if grano == 0:
            for ubicacion in ubicaciones:
                resultado.append(dict(zip(self.columnas+("distancia",), ubicacion)))
        else:
            d = {}
            for ubicacion in ubicaciones:
                i = int(ubicacion[7]//grano)
                # print(ubicacion[7],i)
                if i in d:
                    d[i].append(ubicacion)
                else:
                    d[i] = [ubicacion,]
            rs = []
            for cluster in sorted(d.keys()):
                d[cluster] = sorted(d[cluster], key=lambda x: x[4] - x[5], reverse=True)
                # print(cluster)
                # print(d[cluster])
                # print("-----------")
                rs = rs + d[cluster]
            for r in rs:
                resultado.append(dict(zip(self.columnas+("distancia",), r)))
            # print(resultado)
        return {"num_ubicaciones":len(resultado),"ubicaciones":resultado}

    # def get_libres(self, lat_min=None, lat_max=None, long_min=None, long_max=None):
    #     """
    #     Devuelve una lista de plazas con estado libre.
    #     Si no se pasan parámetros, son todas.
    #     Si se pasan parámetros, las que estén en el interior de la ventana.
    #     :param lat_min: latitud esquina inferior derecha
    #     :param lat_max: latitud esquina superior izquierda
    #     :param long_min: longitud esquina superior izquierda
    #     :param long_max: longitud esquina inferion derecha
    #     :return list dict(plaza):
    #     """
    #     if lat_min is None or lat_max is None or long_min is None or long_max is None:
    #         consulta = "SELECT * from plaza WHERE estado=0 ORDER BY id ASC;"
    #     else:
    #         consulta = "SELECT * FROM plaza WHERE (latitud BETWEEN {:f} AND {:f}) " \
    #                    "AND (longitud BETWEEN {:f} AND {:f}) AND estado=0 ORDER BY id ASC;".\
    #                        format(float(lat_min), float(lat_max), float(long_min), float(long_max))
    #     print(consulta)
    #     bd = BD(self.BD_setting)
    #     bd.ejecutar(consulta)
    #     plazas = bd.filas()
    #     resultado = []
    #     for plaza in plazas:
    #         resultado.append(dict(zip(self.columnas, plaza)))
    #     return {"num_plazas": len(resultado), "plazas": resultado}

    def cargar(self,id):
        """
        Carga el objeto ubicacion
        :param id: id de la ubicacion a cargar
        :return None:
        """
        bd = BD(self.BD_setting)
        bd.ejecutar("SELECT id,direccion,latitud,longitud,plazas_totales,plazas_ocupadas,observaciones "\
                    "FROM ubicacion WHERE id = {:d};".format(int(id)))
        datos = bd.fila()
        # print(datos)
        if datos != None:
            self.id = datos[0]
            self.direccion = datos[1]
            self.latitud = datos[2]
            self.longitud = datos[3]
            self.plazas_totales = datos[4]
            self.plazas_ocupadas = datos[5]
            if datos[6] == None:
                self.observaciones = ""
            else:
                self.observaciones = datos[6]
        else:
            self.id=-1

    def existe(self):
        """
        Comprueba si la ubicacion cargada existe en el sistema
        :return boolean:
        """
        if self.id > 0:
            return True
        return False

    def alta(self, direccion, latitud, longitud, observaciones):
        """
        Crea una nueva ubicacion en el sistema.
        :param direccion: string dirección de la nueva ubicacion
        :param latitud: float latitud de la nueva ubicacion
        :param longitud: float longitud de la nueva ubicacion
        :param observaciones string observaciones de la nueva ubicacion
        :return boolean:
        """
        bd = BD(self.BD_setting)
        direccion = direccion.replace("\"", "\\\"")
        direccion = direccion.replace("\'", "\\\'")
        direccion = direccion[0:300]
        estado = bd.ejecutar("INSERT INTO ubicacion (direccion, latitud, longitud, plazas_totales, plazas_ocupadas, observaciones, geom) " \
                           "VALUES ('{:s}', {:f}, {:f}, 0, 0, '{:s}', st_SetSrid(st_MakePoint({:f}, {:f}), 4326));".\
                           format(direccion, float(latitud), float(longitud), observaciones, float(longitud), float(latitud)))
        # print("INSERT INTO ubicacion (direccion, latitud, longitud, plazas_totales, plazas_ocupadas, observaciones, geom) " \
        #                    "VALUES ('{:s}', {:f}, {:f}, 0, 0, '{:s}', st_SetSrid(st_MakePoint({:f}, {:f}), 4326));".\
        #                    format(direccion, float(latitud), float(longitud), observaciones, float(longitud), float(latitud)))
        # print(estado)
        estado_devolver = False
        id = -1
        if estado == "INSERT 0 1":
            estado_devolver = True
            bd.ejecutar("SELECT currval('ubicacion_id_seq');")
            datos = bd.fila()
            if datos != None:
                id = datos[0]
        return {"estado": estado_devolver, "id":id}

    def eliminar(self, id):
        """
        Elimina la ubicacion
        :param id: id ubicacion a eliminar
        :return boolean:
        """
        bd = BD(self.BD_setting)
        estado = bd.ejecutar("DELETE FROM ubicacion WHERE id = {:d};".format(int(id)))
        if estado == "DELETE 1":
            return True
        return False

    def modificar(self, direccion, observaciones):
        """
        Modifica una ubicacion existente en el sistema
        :param id: identificador de la ubicacion a modificar
        :param direccion: string dirección modificada
        :param observaciones string observaciones modificada
        :return boolean:
        """
        bd = BD(self.BD_setting)
        direccion = direccion.replace("\"", "\\\"")
        direccion = direccion.replace("\'", "\\\'")
        direccion = direccion[0:300]
        estado = bd.ejecutar("UPDATE ubicacion SET direccion = '{:s}', observaciones = '{:s}' "\
                             "WHERE id = {:d};".\
                           format(direccion, observaciones, int(self.id)))

        if estado == "UPDATE 1":
            return True
        return False

    def add_plaza(self):
        """
        Añade una plaza a las plazas totales de la ubicacion
        :return boolean
        """
        bd = BD(self.BD_setting)
        estado = bd.ejecutar("UPDATE ubicacion SET plazas_totales = plazas_totales + 1 WHERE id = {:d};"\
                                    .format(self.id))
        if estado == "UPDATE 1":
            self.plazas_totales += 1
            return True
        return False

    def elimina_plaza(self):
        """
        Elimina una plaza a las plazas totales de la ubicacion
        :return boolean
        """
        bd = BD(self.BD_setting)
        estado = bd.ejecutar("UPDATE ubicacion SET plazas_totales = plazas_totales - 1 WHERE id = {:d};"\
                                    .format(self.id))
        if estado == "UPDATE 1":
            self.plazas_totales -= 1
            return True
        return False

    def add_ocupada(self):
        """
        Añade una plaza a las plazas ocupadas de la ubicacion
        :return boolean
        """
        bd = BD(self.BD_setting)
        estado = bd.ejecutar("UPDATE ubicacion SET plazas_ocupadas = plazas_ocupadas + 1 WHERE id = {:d};"\
                                    .format(self.id))
        if estado == "UPDATE 1":
            self.plazas_ocupadas += 1
            return True
        return False

    def elimina_ocupada(self):
        """
        Elimina una plaza a las plazas ocupadas de la ubicacion
        :return boolean
        """
        bd = BD(self.BD_setting)
        estado = bd.ejecutar("UPDATE ubicacion SET plazas_ocupadas = plazas_ocupadas - 1 WHERE id = {:d};"\
                                    .format(self.id))
        if estado == "UPDATE 1":
            self.plazas_ocupadas -= 1
            return True
        return False
