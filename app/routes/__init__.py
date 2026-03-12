"""
Blueprints de la aplicación
Importar y exponer todos los blueprints
"""
from app.routes.main import bp as main_bp
from app.routes.inversiones import bp as inversiones_bp
from app.routes.historial import bp as historial_bp
from app.routes.ajustes import bp as ajustes_bp
from app.routes.analisis import bp as analisis_bp

__all__ = [
    'main_bp',
    'inversiones_bp',
    'historial_bp',
    'ajustes_bp',
    'analisis_bp'
]