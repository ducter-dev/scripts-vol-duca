import os
from os.path import join, dirname
import MySQLdb
from dotenv import load_dotenv
from peewee import *
from datetime import datetime, timedelta
from .balancesBD import SalidaDetalle, Balance

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

DATABASE_DB = os.environ.get('DATABASE_DB_DOC')
USER_DB = os.environ.get('USER_DB_DOC')
PASSWORD_DB = os.environ.get('PASSWORD_DB_DOC')
HOST_DB = os.environ.get('HOST_DB_DOC')
PORT_DB = os.environ.get('PORT_DB')

class DocumentacionService():
    host = HOST_DB
    db = DATABASE_DB
    user = USER_DB
    password = PASSWORD_DB
    port = PORT_DB
    conexion=''
    
    @classmethod
    def conectarBD(self):
        try:
            datos = [self.host, self.user, self.password, self.db]
            self.conexion = MySQLdb.connect(*datos)
            return True
        except MySQLdb.MySQLError as e:
            # Catch Error
            print("Error", e)
            return False


    @classmethod
    def fetchLlenaderas(self, fechaBalance):
        #print(fechaBalance)
        cursor = self.conexion.cursor()
        querie = "SELECT e.id, e.noEmbarque, e.fecha, e.compania, e.grupo,e.subgrupo, emb.llenadera_llenado as llenadera,  e.valorCarga, e.pg, e.masa, e.masa / 1000 as masaTon, e.fechaSalida, e.fechaJornada, emb.inicioCarga_llenado as inicioCarga, emb.finCarga_llenado as finCarga FROM entrada e INNER JOIN embarques emb ON e.noEmbarque = emb.embarque WHERE e.fechaJornada = '%s'" % fechaBalance
        #print(querie)
        cursor.execute(querie)
        # obtener el balance balance
        balance = Balance.select().where(Balance.fecha == fechaBalance).first()
        if balance is None:
            print('No se encontro el balance')
        embarques = cursor.fetchall()

        for fila in embarques:
            try:
                
                salidaDetalle = SalidaDetalle.create(
                    balance_id = balance.id_balance,
                    fecha_hora_inicio = fila[13],
                    fecha_hora_fin = fila[14],
                    valor = fila[10],
                    tipo = "l",
                    pg = fila[8],
                    llenadera = fila[6],
                    cliente = fila[3],
                )
                print(f"Registrada Salida de Llenadera: {salidaDetalle.id_salidaDetalle} | Hora Inicio: {salidaDetalle.fecha_hora_inicio} | Hora Fin: {salidaDetalle.fecha_hora_fin} Valor: {salidaDetalle.valor}")
            except MySQLdb.MySQLError as e:
                print(e) 