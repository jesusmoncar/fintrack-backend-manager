"""
Formateadores de datos
Funciones para formatear números, fechas y monedas
"""
from datetime import datetime


class Formatter:
    """Clase con métodos de formateo"""
    
    @staticmethod
    def currency(value, symbol='€'):
        """
        Formatear como moneda
        Ejemplo: 1234.56 -> €1,234.56
        """
        if value is None:
            return f"{symbol}0.00"
        
        formatted = f"{abs(value):,.2f}"
        sign = '-' if value < 0 else ''
        
        return f"{sign}{symbol}{formatted}"
    
    @staticmethod
    def percentage(value, decimals=2):
        """
        Formatear como porcentaje
        Ejemplo: 0.1234 -> +12.34%
        """
        if value is None:
            return "0.00%"
        
        sign = '+' if value >= 0 else ''
        return f"{sign}{value:.{decimals}f}%"
    
    @staticmethod
    def large_number(value):
        """
        Formatear números grandes con K, M, B
        Ejemplo: 1500000 -> 1.5M
        """
        if value is None:
            return "0"
        
        abs_value = abs(value)
        sign = '-' if value < 0 else ''
        
        if abs_value >= 1_000_000_000:
            return f"{sign}{abs_value/1_000_000_000:.2f}B"
        elif abs_value >= 1_000_000:
            return f"{sign}{abs_value/1_000_000:.2f}M"
        elif abs_value >= 1_000:
            return f"{sign}{abs_value/1_000:.2f}K"
        else:
            return f"{sign}{abs_value:.2f}"
    
    @staticmethod
    def date_spanish(date_obj):
        """
        Formatear fecha en español
        Ejemplo: 2025-12-25 -> 25 de diciembre de 2025
        """
        if not date_obj:
            return ""
        
        meses = [
            'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
            'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
        ]
        
        if isinstance(date_obj, str):
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d')
        
        return f"{date_obj.day} de {meses[date_obj.month - 1]} de {date_obj.year}"
    
    @staticmethod
    def compact_number(value, decimals=2):
        """
        Formatear número con separadores de miles
        Ejemplo: 1234567.89 -> 1,234,567.89
        """
        if value is None:
            return "0.00"
        
        return f"{value:,.{decimals}f}"