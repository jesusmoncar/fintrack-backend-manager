"""
Servicio de recomendaciones
Genera recomendaciones personalizadas basadas en el portfolio
"""
from app.services.inversion_service import InversionService
from app.services.precio_service import PrecioService
from app.services.calculo_service import CalculoService


class RecomendacionService:
    """Servicio para generar recomendaciones"""
    
    @staticmethod
    def generar_recomendaciones():
        """Generar recomendaciones completas del portfolio"""
        inversiones = InversionService.get_all_with_current_data()
        
        # Calcular distribución
        distribucion = RecomendacionService._calcular_distribucion(inversiones)
        
        # Calcular score
        score = RecomendacionService._calcular_score(distribucion, inversiones)
        
        # Generar recomendaciones personalizadas
        recomendaciones = RecomendacionService._generar_recomendaciones_personalizadas(
            distribucion, inversiones
        )
        
        # Obtener top cryptos y metales
        top_criptos = PrecioService.obtener_top_cryptos(10)
        top_metales = PrecioService.obtener_precios_metales()
        
        return {
            'score': score,
            'distribucion': distribucion,
            'recomendaciones': recomendaciones,
            'top_criptos': top_criptos,
            'top_metales': top_metales
        }
    
    @staticmethod
    def _calcular_distribucion(inversiones):
        """Calcular distribución por categoría"""
        categorias = {
            'criptomonedas': 0,
            'metales': 0,
            'otros': 0
        }
        
        total = 0
        
        for inv in inversiones:
            nombre = inv[1]
            valor = float(inv[9]) if inv[9] else 0
            
            if nombre in PrecioService.CRYPTO_MAP:
                categorias['criptomonedas'] += valor
            elif nombre in PrecioService.METALS_MAP:
                categorias['metales'] += valor
            else:
                categorias['otros'] += valor
            
            total += valor
        
        # Convertir a porcentajes
        if total > 0:
            for key in categorias:
                categorias[key] = (categorias[key] / total) * 100
        
        return categorias
    
    @staticmethod
    def _calcular_score(distribucion, inversiones):
        """Calcular score del portfolio (0-100)"""
        score = 50  # Base
        
        # Penalizar concentración excesiva
        max_concentracion = max(distribucion.values())
        if max_concentracion > 80:
            score -= 30
        elif max_concentracion > 60:
            score -= 15
        
        # Bonificar diversificación
        num_categorias = sum(1 for v in distribucion.values() if v > 5)
        if num_categorias >= 3:
            score += 10
        elif num_categorias >= 2:
            score += 20
        
        # Bonificar balance crypto/metales
        if 30 <= distribucion['criptomonedas'] <= 50:
            score += 10
        if 30 <= distribucion['metales'] <= 50:
            score += 10
        
        # Limitar entre 0-100
        return max(0, min(100, score))
    
    @staticmethod
    def _generar_recomendaciones_personalizadas(distribucion, inversiones):
        """Generar recomendaciones basadas en el portfolio"""
        recomendaciones = []
        
        total_invertido = sum(float(inv[5]) for inv in inversiones if inv[5])
        
        # Recomendaciones por concentración
        if distribucion['criptomonedas'] > 70:
            recomendaciones.append({
                'tipo': 'advertencia',
                'prioridad': 'Alta',
                'titulo': 'Portfolio muy concentrado en criptomonedas',
                'descripcion': f'El {distribucion["criptomonedas"]:.1f}% de tu portfolio está en crypto. Considera diversificar en metales preciosos.',
                'accion': 'Invertir en Oro o Plata para reducir riesgo'
            })
        
        if distribucion['metales'] > 70:
            recomendaciones.append({
                'tipo': 'advertencia',
                'prioridad': 'Alta',
                'titulo': 'Portfolio muy concentrado en metales',
                'descripcion': f'El {distribucion["metales"]:.1f}% está en metales preciosos. Considera añadir criptomonedas para potencial de crecimiento.',
                'accion': 'Diversificar con Bitcoin o Ethereum'
            })
        
        # Recomendaciones por ausencia de activos clave
        tiene_bitcoin = any(inv[1] in ['Bitcoin', 'BTC'] for inv in inversiones)
        if not tiene_bitcoin and total_invertido > 500:
            recomendaciones.append({
                'tipo': 'oportunidad',
                'prioridad': 'Media',
                'titulo': 'Considera añadir Bitcoin',
                'descripcion': 'Bitcoin es el activo más establecido en crypto y actúa como "oro digital".',
                'accion': 'Invertir 10-20% en Bitcoin (BTC)'
            })
        
        tiene_oro = any(inv[1] in ['Oro', 'Gold'] for inv in inversiones)
        if not tiene_oro:
            recomendaciones.append({
                'tipo': 'oportunidad',
                'prioridad': 'Media',
                'titulo': 'Oro como refugio seguro',
                'descripcion': 'El oro es un activo refugio tradicional que protege contra inflación.',
                'accion': 'Invertir 20-30% en Oro'
            })
        
        # Recomendación de balance ideal
        if len(recomendaciones) == 0:
            recomendaciones.append({
                'tipo': 'exito',
                'prioridad': 'Baja',
                'titulo': '¡Portfolio bien balanceado!',
                'descripcion': 'Tu distribución de activos es saludable. Mantén el balance actual.',
                'accion': 'Continuar con la estrategia actual'
            })
        
        return recomendaciones