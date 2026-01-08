from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    # SECRET_KEY: Cambiar en producción por seguridad
    app.config['SECRET_KEY'] = 'sisfac-secret-key-change-in-production-2024'
    
    # Obtener ruta de la base de datos
    from app.config import get_database_path
    db_path = get_database_path()
    
    # Asegurar que el directorio de la base de datos existe
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Log de la ruta de la base de datos (solo en desarrollo o si hay error)
    if not getattr(sys, 'frozen', False):
        print(f"📁 Base de datos: {db_path}")
    
    # Inicializar base de datos
    db.init_app(app)
    
    # Registrar filtros de Jinja2
    from app.utils import numero_a_texto
    app.jinja_env.filters['numero_a_texto'] = numero_a_texto
    
    # Registrar rutas
    from app.routes import clientes, inventario, facturas, main, talonarios, ajustes
    
    app.register_blueprint(main.bp)
    app.register_blueprint(clientes.bp, url_prefix='/clientes')
    app.register_blueprint(inventario.bp, url_prefix='/inventario')
    app.register_blueprint(facturas.bp, url_prefix='/facturas')
    app.register_blueprint(talonarios.bp)
    app.register_blueprint(ajustes.bp, url_prefix='/ajustes')
    
    # Registrar ruta de facturar directamente (sin prefijo)
    from app.routes.facturas import facturar
    app.add_url_rule('/facturar', 'facturar', facturar, methods=['GET', 'POST'])
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    # Manejo de errores global
    @app.errorhandler(404)
    def not_found(error):
        """Maneja errores 404 (página no encontrada)"""
        from flask import request, redirect, url_for
        # Ignorar favicon.ico y otros recursos estáticos
        if request.path.startswith('/favicon.ico') or request.path.startswith('/static/'):
            return '', 204  # No Content
        # Para otras rutas 404, redirigir a la página principal
        return redirect(url_for('main.index'))
    
    @app.errorhandler(500)
    def internal_error(error):
        import traceback
        error_msg = str(error)
        print(f"❌ Error 500: {error_msg}")
        traceback.print_exc()
        
        # En desarrollo, mostrar el error completo
        if not getattr(sys, 'frozen', False):
            from flask import render_template_string
            return render_template_string('''
                <h1>Error Interno del Servidor</h1>
                <p>{{ error }}</p>
                <pre>{{ traceback }}</pre>
            ''', error=error_msg, traceback=traceback.format_exc()), 500
        else:
            # En producción, redirigir a la página principal con mensaje
            from flask import redirect, url_for, flash
            flash('Ocurrió un error interno. Por favor, contacte al administrador.', 'error')
            return redirect(url_for('main.index'))
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        from werkzeug.exceptions import HTTPException
        
        # No manejar excepciones HTTP (404, 500, etc.) aquí, ya tienen sus handlers
        if isinstance(e, HTTPException):
            raise e
        
        import traceback
        error_msg = str(e)
        print(f"❌ Error no manejado: {error_msg}")
        traceback.print_exc()
        
        # Log del error
        import logging
        logging.error(f"Error no manejado: {error_msg}\n{traceback.format_exc()}")
        
        # Retornar error 500
        from flask import jsonify, request, redirect, url_for, flash
        if request.is_json:
            return jsonify({'error': 'Error interno del servidor', 'message': error_msg}), 500
        else:
            flash(f'Error: {error_msg}', 'error')
            return redirect(url_for('main.index'))
    
    return app

