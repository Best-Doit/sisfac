from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys

db = SQLAlchemy()

def get_database_path():
    """Obtiene la ruta de la base de datos, considerando si está empaquetado o no"""
    # Si está empaquetado con PyInstaller
    if getattr(sys, 'frozen', False):
        # Cuando está empaquetado y ejecutado desde Electron:
        # - Los recursos están en un sistema de archivos de solo lectura (AppImage)
        # - Necesitamos usar un directorio escribible en el home del usuario
        
        # Usar el directorio home del usuario para guardar la base de datos
        home_dir = os.path.expanduser('~')
        app_data_dir = os.path.join(home_dir, '.sisfac')
        
        # Crear el directorio si no existe
        os.makedirs(app_data_dir, exist_ok=True)
        
        db_path = os.path.join(app_data_dir, 'sisfac.db')
        
        # Si existe una base de datos en los recursos (solo lectura), copiarla al directorio escribible
        # solo la primera vez
        resources_db = None
        try:
            cwd = os.getcwd()
            resources_db = os.path.join(cwd, 'sisfac.db')
            if not os.path.exists(resources_db):
                executable_dir = os.path.dirname(sys.executable)
                resources_dir = os.path.dirname(os.path.dirname(executable_dir))
                resources_db = os.path.join(resources_dir, 'sisfac.db')
        except:
            pass
        
        # Si hay una base de datos en recursos y no existe en el directorio escribible, copiarla
        if resources_db and os.path.exists(resources_db) and not os.path.exists(db_path):
            try:
                import shutil
                shutil.copy2(resources_db, db_path)
                print(f"📋 Base de datos copiada desde recursos a: {db_path}")
            except Exception as e:
                print(f"⚠️ No se pudo copiar la base de datos desde recursos: {e}")
    else:
        # Modo desarrollo: usar ruta relativa al proyecto
        basedir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(basedir, "..", "..", "sisfac.db")
        db_path = os.path.abspath(db_path)
    
    return db_path

def create_app():
    app = Flask(__name__)
    
    # Configuración
    # SECRET_KEY: Cambiar en producción por seguridad
    app.config['SECRET_KEY'] = 'sisfac-secret-key-change-in-production-2024'
    
    # Obtener ruta de la base de datos
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
    
    # Registrar ruta de facturar directamente (sin prefijo) - wrapper
    @app.route('/facturar', methods=['GET', 'POST'])
    def facturar_wrapper():
        from app.routes.facturas import facturar
        return facturar()
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    # Manejo de errores global
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
            # En producción, mostrar mensaje genérico
            from flask import render_template, flash
            flash('Ocurrió un error interno. Por favor, contacte al administrador.', 'error')
            return render_template('index.html'), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        import traceback
        error_msg = str(e)
        print(f"❌ Error no manejado: {error_msg}")
        traceback.print_exc()
        
        # Log del error
        import logging
        logging.error(f"Error no manejado: {error_msg}\n{traceback.format_exc()}")
        
        # Retornar error 500
        from flask import jsonify, request
        if request.is_json:
            return jsonify({'error': 'Error interno del servidor', 'message': error_msg}), 500
        else:
            from flask import render_template, flash
            flash(f'Error: {error_msg}', 'error')
            return render_template('index.html'), 500
    
    return app

