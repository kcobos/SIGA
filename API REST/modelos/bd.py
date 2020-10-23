# -*- coding: utf-8 -*-

import psycopg2 # Conector con PostgreSQL


class BD():
    def __init__(self, BD_setting):
        self.conector = psycopg2.connect(BD_setting)
        self.cursor = self.conector.cursor()

    def __del__(self):
        self.cursor.close()
        self.conector.close()
        # print("close BD")

    def ejecutar(self, consulta):
        self.cursor.execute(consulta)
        self.conector.commit()
        return self.cursor.statusmessage

    def n_filas(self):
        return self.cursor.rowcount()

    def fila(self):
        return self.cursor.fetchone()

    def filas(self, numero=0):
        assert isinstance(numero, int) and numero>-1
        if numero==0:
            return self.cursor.fetchall()
        return self.cursor.fetchmany(numero)

    def cursor(self):
        return self.cursor

    def conector(self):
        return self.conector
