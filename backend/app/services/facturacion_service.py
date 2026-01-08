"""
Servicio de facturación - Lógica de negocio para facturas
"""
from app import db
from app.models import Factura, DetalleFactura, Cliente, Producto, Talonario


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
            cliente_id = int(request_form['cliente_id'])
            numero_factura = request_form.get('numero_factura', '').strip()
            fecha_emision = request_form['fecha_emision']
            talonario_id = request_form.get('talonario_id')
            
            # Convertir talonario_id
            if talonario_id:
                talonario_id = int(talonario_id)
            else:
                talonario_id = None
            
            # Si no se envía número de factura, generarlo automáticamente
            if not numero_factura:
                talonario = Talonario.query.get(talonario_id) if talonario_id else None
                if talonario:
                    numero_factura = talonario.obtener_siguiente_numero()
            
            # Validar que el número de factura exista y no se repita
            if not numero_factura:
                return None, 'No se pudo generar un número de factura. Verifique el talonario seleccionado.'
            
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
                if actualizar_stock and producto.stock < cantidad:
                    db.session.rollback()
                    return None, f'Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}'
                
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
                    producto.stock -= cantidad
            
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
        clientes = Cliente.query.filter_by(activo=True).order_by(Cliente.nombre).all()
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

