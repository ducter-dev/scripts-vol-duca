from email.errors import InvalidMultipartContentTransferEncodingDefect
from turtle import bgcolor
from datetime import datetime, timedelta
from .balancesBD import cnx as conection
from .balancesBD import Balance, Contenedor, EntradaDetalle, BalanceMovimiento, ContenedorMovimiento, ContenedorBalance, SalidaDetalle, Empresa

def iniciarApp():
    if conection.is_closed():
        
        conection.connect()
        print('Conexion Exitosa')
            
        conection.create_tables([
            Empresa,
            Contenedor,
            Balance,
            EntradaDetalle,
            SalidaDetalle,
            ContenedorMovimiento,
            BalanceMovimiento,
            ContenedorBalance,
        ])

iniciarApp()