from email.errors import InvalidMultipartContentTransferEncodingDefect
from turtle import bgcolor
from .excelServices import ExcelService
from datetime import datetime, timedelta
from .balancesBD import cnx as conection
from .balancesBD import Balance, Contenedor, EntradaDetalle, BalanceMovimiento, ContenedorMovimiento, ContenedorBalance, SalidaDetalle, Empresa
from .documentacionBD import DocumentacionService

def iniciarApp():
    if conection.is_closed():
        
        conection.connect()
        print('Conexion Exitosa')
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
    # obtener la fecha 
    now = datetime.now()
    #fechaBalance = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    fechaBalance = '2022-02-28'
    # obtener el balance balance
    balance = Balance.select().where(Balance.fecha == fechaBalance).first()
    if balance is None:
        #print('No se encontro el balance')
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
        now = datetime.now()
        fecha_base = datetime(now.year, now.month, now.day, 5, 0, 0)
        #fechaJornada = (fecha_base - timedelta(days=1)).strftime("%Y-%m-%d")
        fechaJornada = '2022-02-28'
        DocumentacionService.fetchLlenaderas(fechaJornada)
    else:
        print('No conectado')

def fetchDataDucto():
    if(ExcelService.ductoServiceDB()):
      balance_id= '2'
      ExcelService.lecturaValoresDiarios(balance_id)  
    else:
        print('No hay conexión')

iniciarApp()