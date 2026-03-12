"""
Servicios de la aplicación
Lógica de negocio centralizada
"""
from app.services.inversion_service import InversionService
from app.services.historial_service import HistorialService
from app.services.precio_service import PrecioService
from app.services.calculo_service import CalculoService
from app.services.ajuste_service import AjusteService
from app.services.recomendacion_service import RecomendacionService
from app.services.riesgo_service import RiesgoService
from app.services.proyeccion_service import ProyeccionService

__all__ = [
    'InversionService',
    'HistorialService',
    'PrecioService',
    'CalculoService',
    'AjusteService',
    'RecomendacionService',
    'RiesgoService',
    'ProyeccionService'
]