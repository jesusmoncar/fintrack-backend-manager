"""
Gestior de inversiones - Punto de entrada de la aplicación - Ejecuta la aplicación Flask
"""

from app import create_app
import os

#crear la aplicación
app = create_app()

if __name__ == "__main__":
    #modo debug en desarrollo
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'

    #puerto configurable
    port = int(os.getenv('FLASK_PORT', 5001))

    print(f"""
    ╔════════════════════════════════════════╗
    ║   GESTOR DE INVERSIONES - RUNNING     ║
    ╠════════════════════════════════════════╣
    ║  URL: http://127.0.0.1:{port}          ║
    ║  Debug: {debug_mode}                           ║
    ╚════════════════════════════════════════╝
    """)

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
