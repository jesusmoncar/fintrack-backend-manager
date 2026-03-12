"""
Gestor de Inversiones - Aplicación Factory
Crea y configura la aplicación Flask
"""

from flask import Flask
from config import get_config
import os
def create_app(config_name=None):
    """
    factory para crear la aplicación Flask

    Args:
        config_name (str): nombre de la configuración ('development', 'production', 'testing')
    Returns:
        Flask app configurada
    """
    #crear instancia de Flask
    app = Flask(__name__)

    #cargar configuración
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    config_class =  get_config()
    app.config.from_object(config_class)

    #registrar Blueprints
    register_blueprints(app)

    # Registrar filtros de template
    register_template_filters(app)
    
    # Registrar manejadores de errores
    register_error_handlers(app)

    # Contexto de la aplicación
    with app.app_context():
        # Aquí podrías inicializar extensiones, DB migrations, etc.
        pass
    
    return app


def register_blueprints(app):
    """Registrar todos los blueprints de la aplicación"""
    from app.routes import main_bp, inversiones_bp, historial_bp, ajustes_bp, analisis_bp
    
    # Blueprint principal (dashboard)
    app.register_blueprint(main_bp)
    
    # Blueprints de módulos
    app.register_blueprint(inversiones_bp, url_prefix='/inversiones')
    app.register_blueprint(historial_bp, url_prefix='/historial')
    app.register_blueprint(ajustes_bp, url_prefix='/ajustes')
    app.register_blueprint(analisis_bp, url_prefix='/analisis')


def register_template_filters(app):
    """Registrar filtros personalizados para templates"""
    
    @app.template_filter('currency')
    def currency_filter(value):
        """Formatear como moneda"""
        if value is None:
            return "€0.00"
        return f"€{value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @app.template_filter('percentage')
    def percentage_filter(value):
        """Formatear como porcentaje"""
        if value is None:
            return "0.00%"
        sign = '+' if value >= 0 else ''
        return f"{sign}{value:.2f}%"
    
    @app.template_filter('number')
    def number_filter(value, decimals=2):
        """Formatear número con decimales"""
        if value is None:
            return "0.00"
        return f"{value:.{decimals}f}"


def register_error_handlers(app):
    """Registrar manejadores de errores personalizados"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        return render_template('errors/500.html'), 500
        







