"""
Modelo de Historial de Precios
Representación de la tabla historial_precios
"""

class HistorialPrecio:
    """Modelo de historial de precios"""
    
    def __init__(self, id, inversion_id, fecha, precio_actual, 
                 valor_actual, ganancia_perdida):
        self.id = id
        self.inversion_id = inversion_id
        self.fecha = fecha
        self.precio_actual = precio_actual
        self.valor_actual = valor_actual
        self.ganancia_perdida = ganancia_perdida
    
    def __repr__(self):
        return f"<HistorialPrecio {self.fecha} - €{self.precio_actual}>"
    
    @classmethod
    def from_tuple(cls, data):
        """Crear instancia desde tupla de base de datos"""
        return cls(*data)