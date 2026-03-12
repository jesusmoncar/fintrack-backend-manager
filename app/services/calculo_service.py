"""
Servicio de cálculos financieros
Cálculos reutilizables para el portfolio
"""


class CalculoService:
    """Servicio para cálculos financieros"""
    
    @staticmethod
    def calcular_ganancia_porcentaje(ganancia, inversion):
        """Calcular porcentaje de ganancia"""
        if inversion == 0:
            return 0
        return (ganancia / inversion) * 100
    
    @staticmethod
    def calcular_roi(valor_actual, inversion):
        """Calcular Return on Investment (ROI)"""
        if inversion == 0:
            return 0
        return ((valor_actual - inversion) / inversion) * 100
    
    @staticmethod
    def calcular_promedio_ponderado(valores, pesos):
        """Calcular promedio ponderado"""
        if sum(pesos) == 0:
            return 0
        return sum(v * p for v, p in zip(valores, pesos)) / sum(pesos)
    
    @staticmethod
    def calcular_volatilidad(precios):
        """Calcular volatilidad (desviación estándar)"""
        if len(precios) < 2:
            return 0
        
        media = sum(precios) / len(precios)
        varianza = sum((p - media) ** 2 for p in precios) / len(precios)
        return varianza ** 0.5
    
    @staticmethod
    def calcular_sharpe_ratio(rendimiento, volatilidad, tasa_libre_riesgo=0.02):
        """Calcular Sharpe Ratio"""
        if volatilidad == 0:
            return 0
        return (rendimiento - tasa_libre_riesgo) / volatilidad
    
    @staticmethod
    def calcular_diversificacion(distribuciones):
        """
        Calcular índice de diversificación (0-100)
        100 = perfectamente diversificado
        0 = todo en un solo activo
        """
        if not distribuciones:
            return 0
        
        # Índice Herfindahl–Hirschman inverso
        hhi = sum(d ** 2 for d in distribuciones)
        max_hhi = 10000  # 100^2 (concentración máxima)
        
        return ((max_hhi - hhi) / max_hhi) * 100
    
    @staticmethod
    def proyectar_valor_futuro(valor_actual, tasa_crecimiento_anual, años):
        """Proyectar valor futuro con crecimiento compuesto"""
        return valor_actual * ((1 + tasa_crecimiento_anual) ** años)
    
    @staticmethod
    def calcular_drawdown(precios):
        """Calcular máximo drawdown (caída desde máximo)"""
        if not precios:
            return 0
        
        max_precio = precios[0]
        max_drawdown = 0
        
        for precio in precios:
            if precio > max_precio:
                max_precio = precio
            
            drawdown = ((max_precio - precio) / max_precio) * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        return max_drawdown