import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin123',
            database='ferreteria_db',
            use_pure=True  # Usa el conector puro de Python sin librerias C propensas a colapso
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None