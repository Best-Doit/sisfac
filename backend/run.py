import sys
import os
from app import create_app

# Detectar si estamos ejecutando desde PyInstaller
if getattr(sys, 'frozen', False):
    # Si estamos empaquetados, ajustar rutas
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

app = create_app()

if __name__ == '__main__':
    # En producción (empaquetado), no usar debug
    debug_mode = not getattr(sys, 'frozen', False)
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)

