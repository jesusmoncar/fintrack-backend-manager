"""
Servicio de historial de precios
"""
from app.utils.database import execute_query, get_db_cursor


class HistorialService:
    """Servicio para manejar historial de precios"""
    
    @staticmethod
    def create(inversion_id, fecha, precio_actual, valor_actual, ganancia_perdida):
        """Crear registro en historial"""
        query = """
        INSERT INTO historial_precios (inversion_id, fecha, precio_actual, valor_actual, ganancia_perdida)
        VALUES (%s, %s, %s, %s, %s)
        """
        return execute_query(
            query,
            (inversion_id, fecha, precio_actual, valor_actual, ganancia_perdida),
            commit=True
        )
    
    @staticmethod
    def update_or_create(inversion_id, fecha, precio_actual, valor_actual, ganancia_perdida):
        """Actualizar o crear registro en historial"""
        with get_db_cursor(commit=True) as cursor:
            # Verificar si existe
            check_query = """
            SELECT id FROM historial_precios 
            WHERE inversion_id = %s AND fecha = %s
            """
            cursor.execute(check_query, (inversion_id, fecha))
            existe = cursor.fetchone()
            
            if existe:
                # Actualizar
                update_query = """
                UPDATE historial_precios
                SET precio_actual = %s, valor_actual = %s, ganancia_perdida = %s
                WHERE inversion_id = %s AND fecha = %s
                """
                cursor.execute(update_query, (precio_actual, valor_actual, ganancia_perdida, inversion_id, fecha))
            else:
                # Crear
                insert_query = """
                INSERT INTO historial_precios (inversion_id, fecha, precio_actual, valor_actual, ganancia_perdida)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (inversion_id, fecha, precio_actual, valor_actual, ganancia_perdida))
    
    @staticmethod
    def get_by_inversion_paginated(inversion_id, page=1, per_page=21):
        """Obtener historial paginado"""
        offset = (page - 1) * per_page
        query = """
        SELECT * FROM historial_precios
        WHERE inversion_id = %s
        ORDER BY fecha DESC
        LIMIT %s OFFSET %s
        """
        return execute_query(query, (inversion_id, per_page, offset))
    
    @staticmethod
    def count_by_inversion(inversion_id):
        """Contar registros de una inversión"""
        query = "SELECT COUNT(*) FROM historial_precios WHERE inversion_id = %s"
        result = execute_query(query, (inversion_id,), fetch_one=True)
        return result[0] if result else 0
    
    @staticmethod
    def get_for_chart(inversion_id, limit=60):
        """Obtener datos para gráfico"""
        query = """
        SELECT fecha, precio_actual, valor_actual, ganancia_perdida
        FROM historial_precios
        WHERE inversion_id = %s
        ORDER BY fecha DESC
        LIMIT %s
        """
        return execute_query(query, (inversion_id, limit))
