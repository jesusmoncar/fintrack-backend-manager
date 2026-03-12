"""
Servicio de ajustes manuales
"""
from app.utils.database import get_db_cursor, execute_query
from app.services.inversion_service import InversionService
from app.services.historial_service import HistorialService


class AjusteService:
    """Servicio para ajustes manuales"""
    
    @staticmethod
    def ajustar_completo(inv_id, cantidad, precio_compra, inversion_total, inversion_neta, precio_actual):
        """Ajustar todos los parámetros de una inversión"""
        from datetime import date
        
        # Calcular valores
        valor_actual = cantidad * precio_actual
        ganancia_perdida = valor_actual - inversion_total
        
        with get_db_cursor(commit=True) as cursor:
            # 1. Actualizar inversión
            cursor.execute("""
                UPDATE inversiones
                SET cantidad = %s, precio_compra = %s, 
                    inversion_total = %s, inversion_neta = %s
                WHERE id = %s
            """, (cantidad, precio_compra, inversion_total, inversion_neta, inv_id))
            
            # 2. Obtener fecha máxima en una query separada
            cursor.execute("""
                SELECT MAX(fecha) FROM historial_precios WHERE inversion_id = %s
            """, (inv_id,))
            
            resultado = cursor.fetchone()
            max_fecha = resultado[0] if resultado else None
            
            # 3. Actualizar o crear historial
            if max_fecha:
                cursor.execute("""
                    UPDATE historial_precios
                    SET precio_actual = %s, valor_actual = %s, ganancia_perdida = %s
                    WHERE inversion_id = %s AND fecha = %s
                """, (precio_actual, valor_actual, ganancia_perdida, inv_id, max_fecha))
            else:
                cursor.execute("""
                    INSERT INTO historial_precios 
                    (inversion_id, fecha, precio_actual, valor_actual, ganancia_perdida)
                    VALUES (%s, %s, %s, %s, %s)
                """, (inv_id, date.today(), precio_actual, valor_actual, ganancia_perdida))

                
    @staticmethod
    def ajustar_por_porcentaje(inv_id, porcentaje_deseado):
        """Ajustar por porcentaje deseado"""
        with get_db_cursor(commit=True) as cursor:
            # Obtener datos
            cursor.execute("""
                SELECT i.inversion_total, hp.ganancia_perdida
                FROM inversiones i
                LEFT JOIN historial_precios hp ON i.id = hp.inversion_id
                WHERE i.id = %s
                ORDER BY hp.fecha DESC LIMIT 1
            """, (inv_id,))
            
            result = cursor.fetchone()
            if not result:
                raise ValueError("Inversión no encontrada")
            
            inversion_total = float(result[0])
            ganancia_base = float(result[1]) if result[1] else 0
            
            # Calcular ajuste
            ganancia_deseada = (porcentaje_deseado / 100) * inversion_total
            ajuste = ganancia_deseada - ganancia_base
            
            # Guardar ajuste
            cursor.execute("UPDATE inversiones SET ajuste_manual = %s WHERE id = %s", (ajuste, inv_id))
    
    @staticmethod
    def ajustar_por_ganancia(inv_id, ganancia_deseada):
        """Ajustar por ganancia deseada"""
        with get_db_cursor(commit=True) as cursor:
            # Obtener ganancia base
            cursor.execute("""
                SELECT hp.ganancia_perdida
                FROM historial_precios hp
                WHERE hp.inversion_id = %s
                ORDER BY hp.fecha DESC LIMIT 1
            """, (inv_id,))
            
            result = cursor.fetchone()
            if not result:
                raise ValueError("No hay historial para esta inversión")
            
            ganancia_base = float(result[0]) if result[0] else 0
            
            # Calcular ajuste
            ajuste = ganancia_deseada - ganancia_base
            
            # Guardar ajuste
            cursor.execute("UPDATE inversiones SET ajuste_manual = %s WHERE id = %s", (ajuste, inv_id))