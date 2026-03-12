"""
Utilidades de base de datos
Conexión y gestión de MySQL
"""
import mysql.connector
from flask import current_app
from contextlib import contextmanager


def conectar_db():
    """
    Conectar a la base de datos MySQL
    
    Returns:
        mysql.connector.connection: Conexión a la base de datos
    """
    try:
        conn = mysql.connector.connect(
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME']
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error conectando a la base de datos: {err}")
        raise


@contextmanager
def get_db_cursor(commit=False):
    """
    Context manager para manejar cursores de base de datos
    
    Args:
        commit: Si True, hace commit automáticamente
    
    Uso:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("INSERT ...")
    """
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def execute_query(query, params=None, fetch_one=False, fetch_all=True, commit=False):
    """
    Ejecutar query de forma simplificada
    
    Args:
        query: SQL query
        params: Parámetros de la query
        fetch_one: Si True, retorna solo un resultado
        fetch_all: Si True, retorna todos los resultados
        commit: Si True, hace commit
    
    Returns:
        Resultado de la query
    """
    # DEBUG
    print(f"\n=== DEBUG EXECUTE_QUERY ===")
    print(f"Query: {query[:100]}...")
    print(f"Params: {params}")
    print(f"Params type: {type(params)}")
    if params:
        print(f"Params length: {len(params)}")
        for i, p in enumerate(params):
            print(f"  Param {i}: {p} (type: {type(p)})")
    print(f"===========================\n")
    
    with get_db_cursor(commit=commit) as cursor:
        cursor.execute(query, params or ())
        
        if fetch_one:
            return cursor.fetchone()
        elif fetch_all:
            return cursor.fetchall()
        else:
            return cursor.lastrowid if commit else None
        
