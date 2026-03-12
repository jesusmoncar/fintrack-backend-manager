"""
Blueprint de análisis
Rutas: /analisis/*
"""
from flask import Blueprint, render_template
from app.services.recomendacion_service import RecomendacionService
from app.services.riesgo_service import RiesgoService
from app.services.proyeccion_service import ProyeccionService

bp = Blueprint('analisis', __name__)


@bp.route('/recomendaciones')
def recomendaciones():
    """Mostrar recomendaciones personalizadas"""
    data = RecomendacionService.generar_recomendaciones()
    
    return render_template(
        'pages/recomendaciones.html',
        score=data['score'],
        recomendaciones=data['recomendaciones'],
        distribucion=data['distribucion'],
        top_criptos=data['top_criptos'],
        top_metales=data['top_metales']
    )


@bp.route('/riesgo')
def analisis_riesgo():
    """Análisis de riesgo del portfolio"""
    data = RiesgoService.analizar_portfolio()
    
    return render_template(
        'pages/analisis_riesgo.html',
        nivel_riesgo=data['nivel_riesgo'],
        metricas=data['metricas'],
        recomendaciones=data['recomendaciones']
    )


@bp.route('/proyeccion/<int:id>')
def proyeccion(id):
    """Proyección de una inversión"""
    from app.services.inversion_service import InversionService
    
    inversion = InversionService.get_by_id(id)
    if not inversion:
        from flask import flash, redirect, url_for
        flash('Inversión no encontrada', 'danger')
        return redirect(url_for('main.index'))
    
    proyecciones = ProyeccionService.calcular_proyecciones(id)
    
    return render_template(
        'pages/proyeccion.html',
        inversion=inversion,
        proyecciones=proyecciones
    )