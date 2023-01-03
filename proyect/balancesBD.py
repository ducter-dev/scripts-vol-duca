from asyncio.windows_events import NULL
import os
from os.path import join, dirname
from peewee import *
from dotenv import load_dotenv
from datetime import datetime

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

DATABASE_DB = os.environ.get('DATABASE_DB')
USER_DB = os.environ.get('USER_DB')
PASSWORD_DB = os.environ.get('PASSWORD_DB')
HOST_DB = os.environ.get('HOST_DB')
PORT_DB = os.environ.get('PORT_DB')

try:
    cnx = MySQLDatabase(
                DATABASE_DB,
                user=USER_DB,
                password=PASSWORD_DB,
                host=HOST_DB,
                port=int(PORT_DB),
    )
    
except Exception as ex:
    print(f"Error durante la database {ex}")
    
class UnsignedBigAutoField(BigAutoField):
    field_type = 'BIGINT UNSIGNED AUTO_INCREMENT'
    
class UnsignedForeignField(ForeignKeyField):
    field_type = 'BIGINT UNSIGNED'

class Empresa(Model):
    id_empresa = UnsignedBigAutoField()
    descripcion = CharField(255)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    
    class Meta:
        database = cnx
        table_name = 'empresas'        
        
class Balance(Model):
    id_balance = UnsignedBigAutoField()
    fecha = DateField(default=datetime.now, formats='%Y-%m-%d')
    entradas = DoubleField(null=True)
    salidas = DoubleField(null=True)
    almacenamiento = DoubleField(null=True)
    inventarioInicial = DoubleField(null=True)
    empresa = UnsignedForeignField(Empresa, backref='empresa')
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    
    class Meta:
        database = cnx
        table_name = 'balances'
        

class Contenedor(Model):
    id_contenedor = UnsignedBigAutoField()
    descripcion = CharField(255)
    localizacion_descripcion = CharField(255)
    vigencia_calibracion = DateField(default=datetime.now, formats='%Y-%m-%d')
    capacidad_total = DoubleField(null=True)
    capacidad_operativa = DoubleField(null=True)
    capacidad_util = DoubleField(null=True)
    capacidad_fondaje = DoubleField(null=True)
    volumen_minimo_operacion = DoubleField(null=True)
    estado = CharField(1)
    sistema_medicion = CharField(255)
    localizacion_sistema_medicion = CharField(255)
    vigencia_calibracion_sistema_medicion = DateField(default=datetime.now, formats='%Y-%m-%d')
    incertidumbre_sistema_medicion = DoubleField(null=True)
    empresa = UnsignedForeignField(Empresa, backref='empresa')
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    
    class Meta:
        database = cnx
        table_name = 'contenedores'
        

class EntradaDetalle(Model):
    id_entradaDetalle = UnsignedBigAutoField()
    balance = UnsignedForeignField(Balance, backref='balance')
    fecha_hora = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    valor = DoubleField(null=True)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        database = cnx
        table_name = 'entradasDetalle'


class SalidaDetalle(Model):
    id_salidaDetalle = UnsignedBigAutoField()
    balance = UnsignedForeignField(Balance, backref='balance')
    fecha_hora_inicio = DateTimeField(null=True)
    fecha_hora_fin = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    valor = DoubleField(null=True)
    tipo = CharField(1, null=True)
    pg = CharField(10, null=True)
    llenadera = CharField(10, null=True)
    cliente = IntegerField(null=True)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    
    class Meta:
        database = cnx
        table_name = 'salidasDetalle'
        

class ContenedorBalance(Model):
    id_contenedorBalance = UnsignedBigAutoField()
    balance = UnsignedForeignField(Balance, backref='balance')
    contenedor = UnsignedForeignField(Contenedor, backref='contenedor')
    valor = DoubleField(null=True)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    
    class Meta:
        database = cnx
        table_name = 'contenedorBalance'
        

class BalanceMovimiento(Model):
    id_balanceMovimiento = UnsignedBigAutoField()
    balance = UnsignedForeignField(Balance, backref='balance')
    contenedor = UnsignedForeignField(Contenedor, backref='contenedor')
    tipo = CharField(1, null=True)
    valor = DoubleField(null=True)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        database = cnx
        table_name = 'balanceMovimientos'


class ContenedorMovimiento(Model):
    id_contenedorMovimiento = UnsignedBigAutoField()
    balance = UnsignedForeignField(Balance, backref='balance')
    contenedor = UnsignedForeignField(Contenedor, backref='contenedor')
    fecha_hora = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')
    valor = DoubleField(null=True)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    
    class Meta:
        database = cnx
        table_name = 'contenedorMovimientos'