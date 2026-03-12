"""
Blueprint principal - Dashboard
Ruta: /
"""
from flask import Blueprint, render_template
from app.services.inversion_service import InversionService
from datetime import date

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Dashboard principal con resumen del portfolio"""
    
    # Obtener todas las inversiones con datos actuales
    inversiones = InversionService.get_all_with_current_data()
    
    # Calcular totales del portfolio
    total_invertido = 0
    valor_actual_total = 0
    ganancia_total = 0
    
    for inv in inversiones:
        inversion_total = float(inv[5]) if inv[5] else 0
        valor_actual = float(inv[9]) if inv[9] else 0
        ganancia = float(inv[10]) if inv[10] else 0
        
        total_invertido += inversion_total
        valor_actual_total += valor_actual
        ganancia_total += ganancia
    
    # Calcular porcentaje
    porcentaje_total = (ganancia_total / total_invertido * 100) if total_invertido > 0 else 0
    
    # Estado del portfolio
    if ganancia_total > 0:
        portfolio_status = {'color': 'success', 'emoji': '📈', 'texto': 'En ganancia'}
    elif ganancia_total < 0:
        portfolio_status = {'color': 'danger', 'emoji': '📉', 'texto': 'En pérdida'}
    else:
        portfolio_status = {'color': 'secondary', 'emoji': '➡️', 'texto': 'Sin cambios'}
    
    today = date.today().strftime('%Y-%m-%d')
    
    return render_template(
        'pages/index.html',
        inversiones=inversiones,
        today=today,
        total_invertido=total_invertido,
        valor_actual_total=valor_actual_total,
        ganancia_total=ganancia_total,
        porcentaje_total=porcentaje_total,
        portfolio_status=portfolio_status,
        num_inversiones=len(inversiones)
    )