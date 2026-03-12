"""
Servicio de análisis de riesgo
Evalúa el riesgo del portfolio
"""
from app.services.inversion_service import InversionService
from app.services.historial_service import HistorialService
from app.services.calculo_service import CalculoService


class RiesgoService:
    """Servicio para análisis de riesgo"""
    
    @staticmethod
    def analizar_portfolio():
        """Análisis completo de riesgo del portfolio"""
        inversiones = InversionService.get_all_with_current_data()
        
        # Calcular métricas de riesgo
        metricas = RiesgoService._calcular_metricas_riesgo(inversiones)
        
        # Determinar nivel de riesgo
        nivel_riesgo = RiesgoService._determinar_nivel_riesgo(metricas)
        
        # Generar recomendaciones de riesgo
        recomendaciones = RiesgoService._generar_recomendaciones_riesgo(nivel_riesgo, metricas)
        
        return {
            'nivel_riesgo': nivel_riesgo,
            'metricas': metricas,
            'recomendaciones': recomendaciones
        }
    
    @staticmethod
    def _calcular_metricas_riesgo(inversiones):
        """Calcular métricas de riesgo"""
        metricas = {
            'volatilidad_promedio': 0,
            'max_drawdown': 0,
            'concentracion': 0,
            'roi_promedio': 0,
            'num_activos': len(inversiones)
        }
        
        if not inversiones:
            return metricas
        
        # Calcular volatilidad promedio
        volatilidades = []
        drawdowns = []
        rois = []
        valores = []
        
        for inv in inversiones:
            inv_id = inv[0]
            inversion_total = float(inv[5]) if inv[5] else 0
            valor_actual = float(inv[9]) if inv[9] else 0
            
            valores.append(valor_actual)
            
            # ROI
            if inversion_total > 0:
                roi = ((valor_actual - inversion_total) / inversion_total) * 100
                rois.append(roi)
            
            # Obtener historial para calcular volatilidad
            historial = HistorialService.get_for_chart(inv_id, limit=30)
            if historial:
                precios = [float(h[1]) for h in historial]  # precio_actual
                
                if len(precios) > 1:
                    volatilidad = CalculoService.calcular_volatilidad(precios)
                    volatilidades.append(volatilidad)
                    
                    drawdown = CalculoService.calcular_drawdown(precios)
                    drawdowns.append(drawdown)
        
        # Promedios
        if volatilidades:
            metricas['volatilidad_promedio'] = sum(volatilidades) / len(volatilidades)
        
        if drawdowns:
            metricas['max_drawdown'] = max(drawdowns)
        
        if rois:
            metricas['roi_promedio'] = sum(rois) / len(rois)
        
        # Concentración (índice Herfindahl)
        total_valor = sum(valores)
        if total_valor > 0:
            porcentajes = [(v / total_valor) * 100 for v in valores]
            hhi = sum(p ** 2 for p in porcentajes)
            metricas['concentracion'] = hhi / 100  # Normalizado
        
        return metricas
    
    @staticmethod
    def _determinar_nivel_riesgo(metricas):
        """Determinar nivel de riesgo general"""
        score_riesgo = 0
        
        # Volatilidad
        if metricas['volatilidad_promedio'] > 50:
            score_riesgo += 30
        elif metricas['volatilidad_promedio'] > 20:
            score_riesgo += 15
        
        # Drawdown
        if metricas['max_drawdown'] > 40:
            score_riesgo += 25
        elif metricas['max_drawdown'] > 20:
            score_riesgo += 10
        
        # Concentración
        if metricas['concentracion'] > 50:
            score_riesgo += 25
        elif metricas['concentracion'] > 30:
            score_riesgo += 10
        
        # Número de activos
        if metricas['num_activos'] < 3:
            score_riesgo += 20
        elif metricas['num_activos'] < 5:
            score_riesgo += 10
        
        # Clasificar
        if score_riesgo >= 70:
            return {'nivel': 'Alto', 'color': 'danger', 'emoji': '⚠️'}
        elif score_riesgo >= 40:
            return {'nivel': 'Medio', 'color': 'warning', 'emoji': '⚡'}
        else:
            return {'nivel': 'Bajo', 'color': 'success', 'emoji': '✅'}
    
    @staticmethod
    def _generar_recomendaciones_riesgo(nivel_riesgo, metricas):
        """Generar recomendaciones basadas en riesgo"""
        recomendaciones = []
        
        if nivel_riesgo['nivel'] == 'Alto':
            recomendaciones.append({
                'tipo': 'advertencia',
                'titulo': 'Portfolio de alto riesgo',
                'descripcion': 'Tu portfolio tiene alto nivel de riesgo. Considera reducir exposición.'
            })
        
        if metricas['concentracion'] > 40:
            recomendaciones.append({
                'tipo': 'advertencia',
                'titulo': 'Alta concentración',
                'descripcion': 'Diversifica tu portfolio en más activos para reducir riesgo.'
            })
        
        if metricas['num_activos'] < 5:
            recomendaciones.append({
                'tipo': 'info',
                'titulo': 'Aumenta diversificación',
                'descripcion': 'Considera añadir más activos diferentes para reducir riesgo.'
            })
        
        if metricas['max_drawdown'] > 30:
            recomendaciones.append({
                'tipo': 'advertencia',
                'titulo': 'Alta volatilidad histórica',
                'descripcion': f'Has experimentado caídas de hasta {metricas["max_drawdown"]:.1f}%. Prepárate para volatilidad.'
            })
        
        return recomendaciones