"""
Servicio de facturación - Lógica de negocio para facturas
"""
from app import db
from app.models import Factura, DetalleFactura, Cliente, Producto, Talonario

# region agent log
import json as _agent_json_fs  # solo para depuración de esta sesión
import time as _agent_time_fs  # solo para depuración de esta sesión
import os as _agent_os_fs  # solo para depuración de esta sesión


def _agent_debug_log_facturacion(hypothesis_id, message, data):
    """
    Log compacto en NDJSON para debug de FacturacionService.
    No debe usarse fuera de esta sesión de depuración.
    """
    try:
        ts_ms = int(_agent_time_fs.time() * 1000)
        entry = {
            "sessionId": "fee812",
            "id": f"log_{ts_ms}_{hypothesis_id}",
            "timestamp": ts_ms,
            "location": "backend/app/services/facturacion_service.py:FacturacionService",
            "message": message,
            "data": data,
            "runId": "pre-fix",
            "hypothesisId": hypothesis_id,
        }
        # Asegurar que escribimos en la raíz del workspace: debug-fee812.log
        base_dir = _agent_os_fs.path.abspath(
            _agent_os_fs.path.join(_agent_os_fs.path.dirname(__file__), "..", "..")
        )
        log_path = _agent_os_fs.path.join(base_dir, "debug-fee812.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(_agent_json_fs.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        # La depuración nunca debe romper el flujo de la app
        pass


# endregion


class FacturacionService:
    """Servicio para manejar la lógica de facturación"""
    
    @staticmethod
    def crear_factura(request_form, actualizar_stock=True):
        """
        Crea una factura desde datos del formulario
        
        Args:
            request_form: objeto request.form de Flask
            actualizar_stock: si debe actualizar el stock de productos
            
        Returns:
            tuple: (factura, error_message)
        """
        try:
            # Validar cliente obligatorio
            cliente_val = request_form.get('cliente_id', '').strip()
            if not cliente_val:
                return None, 'Debe seleccionar un cliente.'
            try:
                cliente_id = int(cliente_val)
            except (ValueError, TypeError):
                return None, 'Cliente no válido.'
            if not Cliente.query.get(cliente_id):
                return None, 'El cliente seleccionado no existe.'
            
            numero_factura = request_form.get('numero_factura', '').strip()
            fecha_emision = request_form.get('fecha_emision')
            if not fecha_emision:
                return None, 'Debe indicar la fecha de emisión.'
            talonario_id = request_form.get('talonario_id')
            
            # Convertir talonario_id
            if talonario_id:
                talonario_id = int(talonario_id)
            else:
                talonario_id = None
            
            talonario = Talonario.query.get(talonario_id) if talonario_id else None
            
            # Regla:
            # - Si hay talonario seleccionado, SIEMPRE generamos el número automáticamente
            #   usando el talonario (ignoramos el número escrito a mano).
            # - Si NO hay talonario, usamos el número que venga en el formulario.
            if talonario:
                # region agent log
                _agent_debug_log_facturacion(
                    "H3",
                    "generar_numero_factura_en_servicio",
                    {
                        "talonario_id": talonario_id,
                        "numero_factura_inicial": numero_factura,
                        "talonario_existe": bool(talonario),
                    },
                )
                # endregion

                numero_factura = talonario.obtener_siguiente_numero()

                # region agent log
                _agent_debug_log_facturacion(
                    "H3",
                    "numero_factura_generado_en_servicio",
                    {
                        "talonario_id": talonario_id,
                        "numero_factura_final": numero_factura,
                    },
                )
                # endregion
            
            # Validar que el número de factura exista y no se repita
            if not numero_factura:
                if talonario:
                    return None, 'No se pudo generar un número de factura desde el talonario seleccionado.'
                return None, 'Debe indicar un número de factura.'
            
            if Factura.query.filter_by(numero_factura=numero_factura).first():
                return None, f'El número de factura {numero_factura} ya existe'
            
            # Crear factura
            factura = Factura(
                numero_factura=numero_factura,
                cliente_id=cliente_id,
                talonario_id=talonario_id,
                fecha_emision=fecha_emision,
                fecha_vencimiento=None,
                iva=0,
                notas='',
                subtotal=0,
                total=0,
            )
            db.session.add(factura)
            db.session.flush()
            
            # Agregar detalles
            subtotal = 0
            productos_ids = request_form.getlist('producto_id[]')
            cantidades = request_form.getlist('cantidad[]')
            precios = request_form.getlist('precio_unitario[]')
            
            for i, producto_id in enumerate(productos_ids):
                if not producto_id or producto_id == '':
                    continue
                
                producto = Producto.query.get(int(producto_id))
                if not producto:
                    continue
                
                cantidad = int(cantidades[i]) if cantidades[i] else 0
                precio_unitario = float(precios[i]) if precios[i] else 0
                
                if cantidad <= 0 or precio_unitario <= 0:
                    continue
                
                # Validar stock solo si se va a actualizar
                stock_actual = producto.stock if producto.stock is not None else 0
                if actualizar_stock and stock_actual < cantidad:
                    db.session.rollback()
                    return None, f'Stock insuficiente para {producto.nombre}. Disponible: {stock_actual}'
                
                # Crear detalle
                detalle = DetalleFactura(
                    factura_id=factura.id,
                    producto_id=producto.id,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=cantidad * precio_unitario
                )
                db.session.add(detalle)
                subtotal += detalle.subtotal
                
                # Actualizar stock
                if actualizar_stock:
                    producto.stock = stock_actual - cantidad
            
            # Debe haber al menos una línea de detalle
            if subtotal == 0:
                db.session.rollback()
                return None, 'Debe agregar al menos un producto a la factura.'
            
            # Calcular totales
            iva_monto = subtotal * 0  # IVA siempre en 0
            total = subtotal + iva_monto
            
            factura.subtotal = subtotal
            factura.iva = iva_monto
            factura.total = total
            
            db.session.commit()
            return factura, None
            
        except Exception as e:
            db.session.rollback()
            return None, f'Error al crear factura: {str(e)}'
    
    @staticmethod
    def obtener_datos_formulario(con_numeros_sugeridos=False):
        """
        Obtiene los datos necesarios para el formulario de facturación
        
        Args:
            con_numeros_sugeridos: si True, incluye números sugeridos para talonarios
        """
        clientes = Cliente.query.order_by(Cliente.nombre).all()
        productos = Producto.query.filter_by(activo=True).order_by(Producto.stock.desc(), Producto.nombre).all()
        talonarios = Talonario.query.filter_by(activo=True).order_by(Talonario.id.desc()).all()
        
        resultado = {
            'clientes': clientes,
            'productos': productos,
            'talonarios': talonarios
        }
        
        if con_numeros_sugeridos:
            talonarios_data = []
            for talonario in talonarios:
                try:
                    numero_sugerido = talonario.sugerir_siguiente_numero()
                except Exception as e:
                    # Si hay error, usar el número actual + 1
                    numero_sugerido = f"{talonario.prefijo}-{talonario.numero_actual + 1:04d}" if talonario.numero_actual else None
                
                talonarios_data.append({
                    'id': talonario.id,
                    'nombre': talonario.nombre,
                    'prefijo': talonario.prefijo,
                    'numero_actual': talonario.numero_actual,
                    'numero_fin': talonario.numero_fin,
                    'numero_sugerido': numero_sugerido
                })
            resultado['talonarios_data'] = talonarios_data
        
        return resultado

