"""
Configuración de la aplicación
Soporta diferentes entornos: development, production, testing
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base"""
    
    # Secret key para sesiones
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuración de base de datos MySQL
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'gestor_inversiones')
    
    # Configuración de sesiones
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # APIs externas
    COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'
    YAHOO_FINANCE_BASE_URL = 'https://query1.finance.yahoo.com/v8/finance/chart'
    
    # Spread de Revolut (1.5%)
    REVOLUT_SPREAD = 1.015
    
    # Timezone
    TIMEZONE = 'Europe/Madrid'
    
    # Flask configuración
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Templates
    TEMPLATES_AUTO_RELOAD = True


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False
    
    # Más logging en desarrollo
    EXPLAIN_TEMPLATE_LOADING = True


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False
    
    # En producción, secret key DEBE estar en .env
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production!")


class TestingConfig(Config):
    """Configuración para testing"""
    DEBUG = True
    TESTING = True
    
    # Base de datos de prueba
    DB_NAME = 'gestor_inversiones_test'


# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Obtener configuración según entorno"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])