from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    basedir = os.path.abspath(os.path.dirname(__file__))
    # SECRET_KEY: Cambiar en producción por seguridad
    app.config['SECRET_KEY'] = 'sisfac-secret-key-change-in-production-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "..", "..", "sisfac.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
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
    
    return app

