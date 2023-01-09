from asyncio.windows_events import NULL
import os
from os.path import join, dirname
import MySQLdb 
from dotenv import load_dotenv
import pandas as pd
from proyect.colors import bcolors
from .balancesBD import Balance, EntradaDetalle, SalidaDetalle, ContenedorMovimiento, Contenedor
from datetime import datetime, timedelta

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

HOST_SERVER = os.environ.get('HOST_SERVER')
FILE_ESFERAS = os.environ.get('FILE_ESFERAS')
FILE_DUCTO = os.environ.get('FILE_DUCTO')

# Mes
FOLDER_MES_ESFERAS = os.environ.get('FOLDER_MES_ESFERAS')
FOLDER_MES_DUCTO = os.environ.get('FOLDER_MES_DUCTO')

#DBducto
DATABASE_DB = os.environ.get('DATABASE_DB_DUCA')
USER_DB = os.environ.get('USER_DB_DUCA')
PASSWORD_DB = os.environ.get('PASSWORD_DB_DUCA')
HOST_DB = os.environ.get('HOST_DB_DUCA')
PORT_DB = os.environ.get('PORT_DB_DUCA')

class ExcelService():
    fileEsferas = FILE_ESFERAS
    fileDucto = FILE_DUCTO
    folderMesEsferas = FOLDER_MES_ESFERAS
    folderMesDucto = FOLDER_MES_DUCTO

    host = HOST_DB
    db = DATABASE_DB
    user = USER_DB
    password = PASSWORD_DB
    port = PORT_DB
    conexion=''
    
    @classmethod
    def ductoServiceDB(self):
        try:
            datos = [self.host, self.user, self.password, self.db]
            self.conexion = MySQLdb.connect(*datos)
            return True
        except MySQLdb.MySQLError as e:
            print("Error", e)
            return False

    @classmethod
    def lecturaValoresDiarios(self, balance_id):
        cursor = self.conexion.cursor()
        querie = "SELECT MIN(valor) as primer, MAX(valor) as ultimo, (MAX(valor) - MIN(valor)) totalSalidaDucto FROM salidasDetalle WHERE tipo = 'd' AND balance_id = '%s'" % balance_id
        cursor.execute(querie)
        entradas = cursor.fetchall()

        for fila in entradas:
            try: 
                entradaDetalle = EntradaDetalle.create(
                    balance = balance_id,
                    valor = fila[2],
                )
                print(f"Registrada Entrada a ducto")
            except MySQLdb.MySQLError as e:
                print(e) 