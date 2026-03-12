"""
Servicio de inversiones
Lógica de negocio para gestionar inversiones
"""
from app.utils.database import get_db_cursor, execute_query


class InversionService:
    """Servicio para manejar inversiones"""
    
    @staticmethod
    def get_all_with_current_data():
        """
        Obtener todas las inversiones con sus datos actuales
        
        Returns:
            Lista de tuplas con datos de inversiones
        """
        query = """
        SELECT i.id, i.nombre, i.cantidad, i.precio_compra, i.fecha_compra, 
               i.inversion_total, i.inversion_neta, i.ajuste_manual,
               hp.precio_actual, hp.valor_actual, 
               (hp.ganancia_perdida + IFNULL(i.ajuste_manual, 0)) AS ganancia_perdida_ajustada
        FROM inversiones i
        LEFT JOIN (
            SELECT hp1.inversion_id, hp1.precio_actual, hp1.valor_actual, hp1.ganancia_perdida
            FROM historial_precios hp1
            INNER JOIN (
                SELECT inversion_id, MAX(fecha) as max_fecha
                FROM historial_precios
                GROUP BY inversion_id
            ) hp2 ON hp1.inversion_id = hp2.inversion_id AND hp1.fecha = hp2.max_fecha
        ) hp ON i.id = hp.inversion_id
        """
        
        return execute_query(query)
    
    @staticmethod
    def get_all():
        """Obtener todas las inversiones sin datos de historial"""
        query = "SELECT * FROM inversiones"
        return execute_query(query)
    
    @staticmethod
    def get_by_id(inversion_id):
        """Obtener una inversión por ID"""
        query = "SELECT * FROM inversiones WHERE id = %s"
        return execute_query(query, (inversion_id,), fetch_one=True)
    
    @staticmethod
    def create(nombre, cantidad, precio_compra, fecha_compra, inversion_total, inversion_neta):
        """Crear una nueva inversión"""
        query = """
        INSERT INTO inversiones (nombre, cantidad, precio_compra, fecha_compra, inversion_total, inversion_neta)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return execute_query(
            query,
            (nombre, cantidad, precio_compra, fecha_compra, inversion_total, inversion_neta),
            commit=True
        )
    
    @staticmethod
    def update(inversion_id, **kwargs):
        """Actualizar una inversión"""
        # Construir query dinámicamente
        fields = ', '.join([f"{key} = %s" for key in kwargs.keys()])
        values = list(kwargs.values()) + [inversion_id]
        
        query = f"UPDATE inversiones SET {fields} WHERE id = %s"
        execute_query(query, tuple(values), commit=True)
    
    @staticmethod
    def delete(inversion_id):
        """Eliminar una inversión y su historial"""
        with get_db_cursor(commit=True) as cursor:
            # Primero eliminar historial
            cursor.execute("DELETE FROM historial_precios WHERE inversion_id = %s", (inversion_id,))
            # Luego eliminar inversión
            cursor.execute("DELETE FROM inversiones WHERE id = %s", (inversion_id,))
