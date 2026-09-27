import os
import psycopg2
from psycopg2.extras import RealDictCursor

def obtener_conexion():
    try:
        # Lee la dirección de la base de datos que te dará Render
        db_url = os.environ.get('DATABASE_URL')
        
        if db_url:
            # Corrección requerida por Render
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            conexion = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
        else:
            # Si pruebas en tu computadora con PostgreSQL local
            conexion = psycopg2.connect(
                host="localhost",
                user="postgres",       # Usuario por defecto de PostgreSQL
                password="admin123",   # Tu contraseña de PostgreSQL local
                dbname="ferreteria_db",# Nombre de tu BD
                port="5432",
                cursor_factory=RealDictCursor
            )
        
        return conexion
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None