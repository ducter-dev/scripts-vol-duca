from email.errors import InvalidMultipartContentTransferEncodingDefect
from turtle import bgcolor
from .datosServices import DatosService
from datetime import datetime, timedelta
from .balancesBD import cnx as conection
from .balancesBD import Balance, Contenedor, EntradaDetalle, BalanceMovimiento, ContenedorMovimiento, ContenedorBalance, SalidaDetalle, Empresa
from .documentacionBD import DocumentacionService

now = datetime.now()
fecha_base = datetime(now.year, now.month, now.day, 5, 0, 0)
fechaJornada = (fecha_base - timedelta(days=1)).strftime("%Y-%m-%d")

def iniciarApp():
    if conection.is_closed():
        conection.connect()
        print('Conexión Exitosa')
        fetchLlenaderasDocumentacion()
        fetchDataDucto()
            
        #conection.create_tables([
        #    Empresa,
        #    Contenedor,
        #    Balance,
        #    EntradaDetalle,
        #    SalidaDetalle,
        #    ContenedorMovimiento,
        #    BalanceMovimiento,
        #    ContenedorBalance,
        #])

def crearBalance():
    fechaBalance = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    # obtener el balance 
    balance = Balance.select().where(Balance.fecha == fechaBalance).first()
    if balance is None:
        balance = Balance.create(
            fecha = fechaBalance,
            entradas = 0,
            salidas = 0,
            almacenamiento = 0,
            inventarioInicial = 0,
            empresa_id = 1,
        )
        print(f"Se creó balance: id -> {balance.id_balance}, fecha -> {balance.fecha}")
    
    print(f"Se encontró balance: id -> {balance.id_balance}, fecha -> {balance.fecha}")

def fetchLlenaderasDocumentacion():
    if (DocumentacionService.conectarBD()):
        DocumentacionService.fetchLlenaderas(fechaJornada)
    else:
        print('No conectado')

def fetchDataDucto():
    if(DatosService.ductoServiceDB()):
        DatosService.lecturaValoresDiarios(fechaJornada)  
    else:
        print('No hay conexión')

iniciarApp()