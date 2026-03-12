"""
Servicio de proyecciones
Calcula proyecciones futuras de inversiones
"""
from app.services.historial_service import HistorialService
from app.services.calculo_service import CalculoService


class ProyeccionService:
    """Servicio para calcular proyecciones"""
    
    @staticmethod
    def calcular_proyecciones(inversion_id):
        """Calcular proyecciones de una inversión"""
        # Obtener historial
        historial = HistorialService.get_for_chart(inversion_id, limit=90)
        
        if not historial or len(historial) < 2:
            return {
                'tiene_datos': False,
                'mensaje': 'No hay suficientes datos para proyectar'
            }
        
        # Extraer valores
        valores = [float(h[2]) for h in historial]  # valor_actual
        valor_actual = valores[0]  # Más reciente
        
        # Calcular tasa de crecimiento promedio
        tasa_crecimiento = ProyeccionService._calcular_tasa_crecimiento(valores)
        
        # Generar proyecciones
        escenarios = {
            'conservador': tasa_crecimiento * 0.5,
            'moderado': tasa_crecimiento,
            'optimista': tasa_crecimiento * 1.5
        }
        
        periodos = [30, 90, 180, 365]  # días
        proyecciones = {}
        
        for nombre, tasa in escenarios.items():
            proyecciones[nombre] = []
            for dias in periodos:
                años = dias / 365
                valor_proyectado = CalculoService.proyectar_valor_futuro(
                    valor_actual, tasa, años
                )
                proyecciones[nombre].append({
                    'periodo': f'{dias} días',
                    'valor': valor_proyectado,
                    'ganancia': valor_proyectado - valor_actual
                })
        
        return {
            'tiene_datos': True,
            'valor_actual': valor_actual,
            'tasa_crecimiento': tasa_crecimiento,
            'proyecciones': proyecciones,
            'volatilidad': CalculoService.calcular_volatilidad(valores)
        }
    
    @staticmethod
    def _calcular_tasa_crecimiento(valores):
        """Calcular tasa de crecimiento anualizada"""
        if len(valores) < 2:
            return 0
        
        # Usar primer y último valor
        valor_inicial = valores[-1]
        valor_final = valores[0]
        
        if valor_inicial == 0:
            return 0
        
        # Tasa de crecimiento simple anualizada
        dias = len(valores)
        tasa_total = (valor_final - valor_inicial) / valor_inicial
        tasa_anual = (tasa_total / dias) * 365
        
        return tasa_anual