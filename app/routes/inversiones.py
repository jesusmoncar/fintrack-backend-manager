"""
Blueprint de inversiones
Rutas: /inversiones/*
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.inversion_service import InversionService
from app.services.historial_service import HistorialService
from datetime import datetime, date

bp = Blueprint('inversiones', __name__)


@bp.route('/nueva', methods=['GET', 'POST'])
def nueva():
    """Crear nueva inversión"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = float(request.form['cantidad'])
        precio_compra = float(request.form['precio_compra'])
        fecha_compra_str = request.form['fecha_compra']
        
        # Convertir fecha
        fecha_compra = datetime.strptime(fecha_compra_str, '%Y-%m-%d').date()
        
        # Calcular inversión
        inversion_total = cantidad * precio_compra
        inversion_neta = inversion_total
        
        # Crear inversión
        inversion_id = InversionService.create(
            nombre, cantidad, precio_compra, 
            fecha_compra, inversion_total, inversion_neta
        )
        
        # Crear primer registro en historial
        HistorialService.create(
            inversion_id, fecha_compra, 
            precio_compra, inversion_neta, 0
        )
        
        flash('Inversión agregada correctamente!', 'success')
        return redirect(url_for('main.index'))
    
    today = date.today().strftime('%Y-%m-%d')
    return render_template('pages/nueva_inversion.html', today=today)


@bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_precio(id):
    """Actualizar precio de una inversión"""
    precio_actual = float(request.form['precio_actual'])
    fecha_str = request.form['fecha_registro']
    fecha_registro = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    
    # Obtener datos de la inversión
    inversion = InversionService.get_by_id(id)
    if not inversion:
        flash('Inversión no encontrada', 'danger')
        return redirect(url_for('main.index'))
    
    cantidad = float(inversion[2])
    inversion_total = float(inversion[5])
    
    # Calcular valores
    valor_actual = cantidad * precio_actual
    ganancia_perdida = valor_actual - inversion_total
    
    # Actualizar o crear registro en historial
    HistorialService.update_or_create(
        id, fecha_registro, precio_actual, 
        valor_actual, ganancia_perdida
    )
    
    flash('Precio actualizado correctamente!', 'success')
    return redirect(url_for('main.index'))


@bp.route('/actualizar_todos', methods=['POST'])
def actualizar_todos():
    """Actualizar todos los precios automáticamente"""
    from app.services.precio_service import PrecioService
    
    inversiones = InversionService.get_all()
    fecha_hoy = date.today()
    actualizados = 0
    errores = []
    
    for inv in inversiones:
        try:
            inv_id, nombre, cantidad, _, _, inversion_total, _ = inv[:7]
            
            # Obtener precio actual
            precio_actual = PrecioService.obtener_precio(nombre)
            
            if precio_actual:
                valor_actual = float(cantidad) * precio_actual
                ganancia_perdida = valor_actual - float(inversion_total)
                
                HistorialService.update_or_create(
                    inv_id, fecha_hoy, precio_actual,
                    valor_actual, ganancia_perdida
                )
                actualizados += 1
            else:
                errores.append(f'{nombre}: No se pudo obtener precio')
                
        except Exception as e:
            errores.append(f'{nombre}: {str(e)}')
    
    if actualizados > 0:
        flash(f'✅ {actualizados} precios actualizados correctamente!', 'success')
    
    for error in errores:
        flash(f'⚠️ {error}', 'warning')
    
    return redirect(url_for('main.index'))


@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    """Eliminar una inversión"""
    InversionService.delete(id)
    flash('Inversión eliminada correctamente!', 'success')
    return redirect(url_for('main.index'))