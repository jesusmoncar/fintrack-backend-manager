"""
Servicio de precios
Obtiene precios actuales de APIs externas (CoinGecko, Yahoo Finance)
"""
import requests
from flask import current_app


class PrecioService:
    """Servicio para obtener precios de activos"""
    
    # Mapeo de nombres a IDs de CoinGecko
    CRYPTO_MAP = {
        'Bitcoin': 'bitcoin',
        'BTC': 'bitcoin',
        'Ethereum': 'ethereum',
        'ETH': 'ethereum',
        'Solana': 'solana',
        'SOL': 'solana',
        'Cardano': 'cardano',
        'ADA': 'cardano',
        'XRP': 'ripple',
        'Ripple': 'ripple',
        'Polkadot': 'polkadot',
        'DOT': 'polkadot',
        'Dogecoin': 'dogecoin',
        'DOGE': 'dogecoin',
        'Avalanche': 'avalanche-2',
        'AVAX': 'avalanche-2',
        'Chainlink': 'chainlink',
        'LINK': 'chainlink',
        'Polygon': 'matic-network',
        'MATIC': 'matic-network',
    }
    
    # Mapeo de metales a símbolos Yahoo Finance
    METALS_MAP = {
        'Oro': 'GC=F',
        'Gold': 'GC=F',
        'Plata': 'SI=F',
        'Silver': 'SI=F',
        'Platino': 'PL=F',
        'Platinum': 'PL=F',
        'XPT': 'PL=F',
        'Paladio': 'PA=F',
        'Palladium': 'PA=F',
    }
    
    @staticmethod
    def obtener_precio(nombre):
        """
        Obtener precio actual de un activo
        
        Args:
            nombre: Nombre del activo
        
        Returns:
            float: Precio en EUR
        """
        # Intentar como cripto primero
        if nombre in PrecioService.CRYPTO_MAP:
            return PrecioService.obtener_precio_crypto(nombre)
        
        # Intentar como metal
        if nombre in PrecioService.METALS_MAP:
            return PrecioService.obtener_precio_metal(nombre)
        
        return None
    
    @staticmethod
    def obtener_precio_crypto(nombre):
        """Obtener precio de criptomoneda desde CoinGecko"""
        try:
            crypto_id = PrecioService.CRYPTO_MAP.get(nombre)
            if not crypto_id:
                return None
            
            url = f"{current_app.config['COINGECKO_API_URL']}/simple/price"
            params = {
                'ids': crypto_id,
                'vs_currencies': 'eur'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            precio = data.get(crypto_id, {}).get('eur')
            
            return float(precio) if precio else None
            
        except Exception as e:
            print(f"Error obteniendo precio crypto de {nombre}: {e}")
            return None
    
    @staticmethod
    def obtener_precio_metal(nombre):
        """Obtener precio de metal desde Yahoo Finance"""
        try:
            symbol = PrecioService.METALS_MAP.get(nombre)
            if not symbol:
                return None
            
            url = f"{current_app.config['YAHOO_FINANCE_BASE_URL']}/{symbol}"
            params = {
                'interval': '1d',
                'range': '1d'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            quote = data['chart']['result'][0]['meta']['regularMarketPrice']
            
            # Convertir de USD a EUR con spread de Revolut
            precio_usd = float(quote)
            # Asumiendo tasa USD/EUR aproximada (deberías obtenerla de una API)
            tasa_eur = 0.92  # Aproximado
            precio_eur = precio_usd * tasa_eur * current_app.config['REVOLUT_SPREAD']
            
            return precio_eur
            
        except Exception as e:
            print(f"Error obteniendo precio metal de {nombre}: {e}")
            return None
    
    @staticmethod
    def obtener_top_cryptos(limit=10):
        """Obtener top criptomonedas por market cap"""
        try:
            url = f"{current_app.config['COINGECKO_API_URL']}/coins/markets"
            params = {
                'vs_currency': 'eur',
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h,7d,30d'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error obteniendo top cryptos: {e}")
            return []
    
    @staticmethod
    def obtener_precios_metales():
        """Obtener precios de los 4 metales principales"""
        metales = ['Oro', 'Plata', 'Platino', 'Paladio']
        precios = {}
        
        for metal in metales:
            precio = PrecioService.obtener_precio_metal(metal)
            if precio:
                precios[metal] = precio
        
        return precios