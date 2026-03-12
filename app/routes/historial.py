"""
Blueprint de historial
Rutas: /historial/*
"""
from flask import Blueprint, render_template, redirect, url_for, flash
from app.services.historial_service import HistorialService
from app.services.inversion_service import InversionService
from datetime import datetime, timedelta

bp = Blueprint('historial', __name__)


@bp.route('/<int:id>')
def ver_historial(id):
    """Ver historial de una inversión con paginación"""
    from flask import request
    
    # Obtener inversión
    inversion = InversionService.get_by_id(id)
    if not inversion:
        from flask import flash, redirect, url_for
        flash('Inversión no encontrada', 'danger')
        return redirect(url_for('main.index'))
    
    # Paginación
    page = request.args.get('page', 1, type=int)
    per_page = 21  # 3 semanas × 7 días
    
    # Obtener historial paginado
    historial_data = HistorialService.get_by_inversion_paginated(id, page, per_page)
    total_registros = HistorialService.count_by_inversion(id)
    total_paginas = (total_registros + per_page - 1) // per_page
    
    # Agrupar por semanas
    historial_por_semanas = {}
    for registro in historial_data:
        fecha_obj = registro[2]  # fecha
        
        # Calcular inicio de semana (lunes)
        dias_desde_lunes = fecha_obj.weekday()
        inicio_semana = fecha_obj - timedelta(days=dias_desde_lunes)
        fin_semana = inicio_semana + timedelta(days=6)
        
        semana_key = f"{inicio_semana.strftime('%Y-%m-%d')} al {fin_semana.strftime('%Y-%m-%d')}"
        
        if semana_key not in historial_por_semanas:
            historial_por_semanas[semana_key] = {
                'inicio': inicio_semana,
                'fin': fin_semana,
                'registros': []
            }
        
        historial_por_semanas[semana_key]['registros'].append(registro)
    
    # Datos para gráfico (últimos 60 registros)
    datos_grafico = HistorialService.get_for_chart(id, limit=60)
    
    return render_template(
        'pages/historial.html',
        inversion=inversion,
        historial_por_semanas=historial_por_semanas,
        datos_grafico=datos_grafico,
        page=page,
        total_paginas=total_paginas,
        total_registros=total_registros
    )

@bp.route('/eliminar_registro/<int:registro_id>', methods=['POST'])
def eliminar_registro(registro_id):
    """Eliminar un registro específico del historial"""
    from app.utils.database import get_db_cursor
    from flask import flash, redirect, request
    
    with get_db_cursor(commit=True) as cursor:
        # Obtener el inversion_id antes de eliminar
        cursor.execute("SELECT inversion_id FROM historial_precios WHERE id = %s", (registro_id,))
        resultado = cursor.fetchone()
        
        if resultado:
            inversion_id = resultado[0]
            
            # Eliminar registro
            cursor.execute("DELETE FROM historial_precios WHERE id = %s", (registro_id,))
            flash('Registro eliminado correctamente', 'success')
            
            return redirect(url_for('historial.ver_historial', id=inversion_id))
        else:
            flash('Registro no encontrado', 'danger')
            return redirect(url_for('main.index'))