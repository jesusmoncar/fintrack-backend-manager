"""
Modelo de Inversión
Representación de la tabla inversiones
"""

class Inversion:
    """Modelo de inversión"""
    
    def __init__(self, id, nombre, cantidad, precio_compra, fecha_compra, 
                 inversion_total, inversion_neta, ajuste_manual=0):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio_compra = precio_compra
        self.fecha_compra = fecha_compra
        self.inversion_total = inversion_total
        self.inversion_neta = inversion_neta
        self.ajuste_manual = ajuste_manual
    
    def __repr__(self):
        return f"<Inversion {self.nombre} - €{self.inversion_total}>"
    
    @classmethod
    def from_tuple(cls, data):
        """Crear instancia desde tupla de base de datos"""
        return cls(*data)