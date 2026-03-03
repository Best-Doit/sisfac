from app import db
from datetime import datetime

# region agent log
import json as _agent_json  # solo para depuración de esta sesión
import time as _agent_time  # solo para depuración de esta sesión
import os as _agent_os  # solo para depuración de esta sesión


def _agent_debug_log_talonario(hypothesis_id, message, data):
    """
    Log compacto en NDJSON para debug de Talonario.
    No debe usarse fuera de esta sesión de depuración.
    """
    try:
        ts_ms = int(_agent_time.time() * 1000)
        entry = {
            "sessionId": "fee812",
            "id": f"log_{ts_ms}_{hypothesis_id}",
            "timestamp": ts_ms,
            "location": "backend/app/models.py:Talonario",
            "message": message,
            "data": data,
            "runId": "pre-fix",
            "hypothesisId": hypothesis_id,
        }
        # Asegurar que escribimos en la raíz del workspace: debug-fee812.log
        base_dir = _agent_os.path.abspath(
            _agent_os.path.join(_agent_os.path.dirname(__file__), "..", "..")
        )
        log_path = _agent_os.path.join(base_dir, "debug-fee812.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(_agent_json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        # La depuración nunca debe romper el flujo de la app
        pass


# endregion


class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    ruc_ci = db.Column(db.String(50))
    direccion = db.Column(db.String(500))
    telefono = db.Column(db.String(50))
    email = db.Column(db.String(100))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    facturas = db.relationship('Factura', backref='cliente', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'ruc_ci': self.ruc_ci,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    # Usamos 'precio_compra' como nombre de atributo, pero mantenemos el nombre
    # de columna 'precio_unitario' en la base de datos para compatibilidad.
    precio_compra = db.Column('precio_unitario', db.Float, nullable=False)
    precio_1 = db.Column(db.Float)
    precio_2 = db.Column(db.Float)
    stock = db.Column(db.Integer, default=0)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    # La relación con DetalleFactura se define en DetalleFactura con backref
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            # Para APIs nuevas exponemos 'precio_compra' como campo principal,
            # pero mantenemos 'precio_unitario' para no romper integraciones existentes.
            'precio_compra': self.precio_compra,
            'precio_unitario': self.precio_compra,
            'precio_1': self.precio_1,
            'precio_2': self.precio_2,
            'stock': self.stock,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }
    
    def obtener_precio(self, nivel=1):
        if nivel == 1 and self.precio_1:
            return self.precio_1
        elif nivel == 2 and self.precio_2:
            return self.precio_2
        
        # Fallback al precio de compra cuando no hay precios de venta definidos
        return self.precio_compra

    # Alias de compatibilidad para código existente que usa 'precio_unitario'
    @property
    def precio_unitario(self):
        return self.precio_compra

    @precio_unitario.setter
    def precio_unitario(self, value):
        self.precio_compra = value

class Factura(db.Model):
    __tablename__ = 'facturas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_factura = db.Column(db.String(50), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    talonario_id = db.Column(db.Integer, db.ForeignKey('talonarios.id'), nullable=True)
    fecha_emision = db.Column(db.Date, nullable=False)
    fecha_vencimiento = db.Column(db.Date)
    subtotal = db.Column(db.Float, nullable=False)
    iva = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), default='PAGADA')
    notas = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_edicion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    detalles = db.relationship('DetalleFactura', backref='factura', cascade='all, delete-orphan')
    talonario = db.relationship('Talonario', backref='facturas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero_factura': self.numero_factura,
            'cliente_id': self.cliente_id,
            'cliente_nombre': self.cliente.nombre if self.cliente else None,
            'fecha_emision': self.fecha_emision.isoformat() if self.fecha_emision else None,
            'fecha_vencimiento': self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            'subtotal': self.subtotal,
            'iva': self.iva,
            'total': self.total,
            'estado': self.estado,
            'notas': self.notas
        }

class DetalleFactura(db.Model):
    __tablename__ = 'detalle_factura'
    
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('facturas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    # Relaciones
    producto = db.relationship('Producto', backref='detalles')
    
    def to_dict(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'producto_nombre': self.producto.nombre if self.producto else None,
            'producto_codigo': self.producto.codigo if self.producto else None,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal
        }

class Talonario(db.Model):
    __tablename__ = 'talonarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    prefijo = db.Column(db.String(20), nullable=False)
    numero_inicio = db.Column(db.Integer, nullable=False)
    numero_fin = db.Column(db.Integer, nullable=False)
    numero_actual = db.Column(db.Integer, nullable=False, default=0)
    activo = db.Column(db.Boolean, default=True)
    
    def _get_numeros_safe(self):
        """Normaliza valores nulos para evitar errores en comparaciones."""
        numero_inicio = self.numero_inicio if self.numero_inicio is not None else 1
        numero_fin = self.numero_fin if self.numero_fin is not None else numero_inicio
        numero_actual = self.numero_actual if self.numero_actual is not None else numero_inicio
        if numero_actual < numero_inicio:
            numero_actual = numero_inicio
        return numero_inicio, numero_actual, numero_fin
    
    def obtener_siguiente_numero(self):
        """Obtiene el siguiente número de factura e incrementa el contador"""
        # region agent log
        _agent_debug_log_talonario(
            "H1",
            "obtener_siguiente_numero_called",
            {
                "talonario_id": self.id,
                "prefijo": self.prefijo,
                "numero_inicio": self.numero_inicio,
                "numero_actual": self.numero_actual,
                "numero_fin": self.numero_fin,
            },
        )
        # endregion

        _, numero_actual, numero_fin = self._get_numeros_safe()
        if numero_actual < numero_fin:
            numero = f"{self.prefijo}-{numero_actual:04d}"
            self.numero_actual = numero_actual + 1
            db.session.add(self)
            db.session.commit()

            # region agent log
            _agent_debug_log_talonario(
                "H1",
                "obtener_siguiente_numero_committed",
                {
                    "talonario_id": self.id,
                    "numero_generado": numero,
                    "nuevo_numero_actual": self.numero_actual,
                },
            )
            # endregion

            return numero
        return None
    
    def sugerir_siguiente_numero(self):
        """Sugiere el siguiente número sin incrementarlo (solo para mostrar)"""
        _, numero_actual, numero_fin = self._get_numeros_safe()
        if numero_actual < numero_fin:
            numero_sugerido = f"{self.prefijo}-{numero_actual:04d}"

            # region agent log
            _agent_debug_log_talonario(
                "H2",
                "sugerir_siguiente_numero_computed",
                {
                    "talonario_id": self.id,
                    "prefijo": self.prefijo,
                    "numero_actual": numero_actual,
                    "numero_fin": numero_fin,
                    "numero_sugerido": numero_sugerido,
                },
            )
            # endregion

            return numero_sugerido
        return None

class Configuracion(db.Model):
    __tablename__ = 'configuracion'
    
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text)
    descripcion = db.Column(db.String(500))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def obtener(clave, default=None):
        """Obtiene el valor de una configuración"""
        config = Configuracion.query.filter_by(clave=clave).first()
        if config:
            return config.valor
        return default
    
    @staticmethod
    def establecer(clave, valor, descripcion=None):
        """Establece o actualiza una configuración"""
        config = Configuracion.query.filter_by(clave=clave).first()
        if config:
            config.valor = str(valor)
            if descripcion:
                config.descripcion = descripcion
        else:
            config = Configuracion(clave=clave, valor=str(valor), descripcion=descripcion)
            db.session.add(config)
        db.session.commit()
        return config
    
    @staticmethod
    def obtener_int(clave, default=0):
        """Obtiene el valor de una configuración como entero"""
        valor = Configuracion.obtener(clave, default)
        try:
            return int(valor)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def obtener_float(clave, default=0.0):
        """Obtiene el valor de una configuración como float"""
        valor = Configuracion.obtener(clave, default)
        try:
            return float(valor)
        except (ValueError, TypeError):
            return default
