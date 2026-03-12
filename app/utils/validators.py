"""
Validadores de datos
Funciones para validar entradas de usuario
"""
from datetime import datetime


class Validator:
    """Clase con métodos de validación"""
    
    @staticmethod
    def is_positive_number(value):
        """Validar que es un número positivo"""
        try:
            num = float(value)
            return num > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_date(date_string, format='%Y-%m-%d'):
        """Validar formato de fecha"""
        try:
            datetime.strptime(date_string, format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_asset_name(name):
        """Validar nombre de activo"""
        if not name or not isinstance(name, str):
            return False
        
        # Solo letras, números, espacios y guiones
        return all(c.isalnum() or c.isspace() or c == '-' for c in name)
    
    @staticmethod
    def sanitize_string(text, max_length=100):
        """Limpiar y limitar longitud de string"""
        if not text:
            return ""
        
        # Eliminar espacios extras
        cleaned = ' '.join(text.split())
        
        # Limitar longitud
        return cleaned[:max_length]