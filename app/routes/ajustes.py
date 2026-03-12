"""
Blueprint de ajustes
Rutas: /ajustes/*
"""
from flask import Blueprint, request, redirect, url_for, flash
from app.services.ajuste_service import AjusteService

bp = Blueprint('ajustes', __name__)


@bp.route('/individual/<int:id>', methods=['POST'])
def ajustar_individual(id):
    """Ajustar una inversión individual"""
    
    print("\n=== DEBUG AJUSTE INDIVIDUAL ===")
    print(f"ID: {id}")
    print(f"Form data completo: {dict(request.form)}")
    
    cantidad = float(request.form.get('cantidad'))
    precio_compra = float(request.form.get('precio_compra'))
    inversion_total = float(request.form.get('inversion_total'))
    inversion_neta = float(request.form.get('inversion_neta'))
    precio_actual = float(request.form.get('precio_actual'))
    
    print(f"Cantidad parseada: {cantidad}")
    print(f"Precio compra parseado: {precio_compra}")
    print(f"Inversión total parseada: {inversion_total}")
    print(f"Inversión neta parseada: {inversion_neta}")
    print(f"Precio actual parseado: {precio_actual}")
    print("================================\n")
    
    try:
        AjusteService.ajustar_completo(
            id, cantidad, precio_compra, 
            inversion_total, inversion_neta, precio_actual
        )
        flash('✅ Inversión ajustada completamente', 'success')
    except Exception as e:
        print(f"ERROR en ajuste: {e}")
        import traceback
        traceback.print_exc()
        flash(f'❌ Error: {str(e)}', 'danger')
    
    return redirect(url_for('main.index'))


@bp.route('/masivo', methods=['POST'])
def ajustar_masivo():
    """Ajustar múltiples inversiones a la vez"""
    inversiones_ids = request.form.getlist('inversion_id[]')
    ajustes_aplicados = 0
    errores = []
    
    for inv_id in inversiones_ids:
        try:
            tipo_ajuste = request.form.get(f'tipo_ajuste_{inv_id}')
            
            if not tipo_ajuste or tipo_ajuste == '':
                continue
            
            if tipo_ajuste == 'porcentaje':
                porcentaje = request.form.get(f'porcentaje_{inv_id}')
                if porcentaje and porcentaje.strip():
                    AjusteService.ajustar_por_porcentaje(inv_id, float(porcentaje))
                    ajustes_aplicados += 1
            
            elif tipo_ajuste == 'precio':
                ganancia = request.form.get(f'ganancia_{inv_id}')
                if ganancia and ganancia.strip():
                    AjusteService.ajustar_por_ganancia(inv_id, float(ganancia))
                    ajustes_aplicados += 1
                    
        except Exception as e:
            errores.append(f'ID {inv_id}: {str(e)}')
    
    if ajustes_aplicados > 0:
        flash(f'✅ {ajustes_aplicados} inversiones ajustadas', 'success')
    
    for error in errores:
        flash(f'⚠️ {error}', 'warning')
    
    if ajustes_aplicados == 0 and not errores:
        flash('ℹ️ No se seleccionaron inversiones para ajustar', 'info')
    
    return redirect(url_for('main.index'))