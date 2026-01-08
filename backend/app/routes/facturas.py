from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app import db
from app.models import Factura, DetalleFactura, Cliente, Producto, Talonario
from datetime import datetime, date
import random

bp = Blueprint('facturas', __name__)

@bp.route('/')
def listar():
    q = request.args.get('q', '')
    fecha_desde = request.args.get('fecha_desde', '')
    fecha_hasta = request.args.get('fecha_hasta', '')
    
    facturas = Factura.query
    if q:
        facturas = facturas.filter(Factura.numero_factura.contains(q))
    if fecha_desde:
        facturas = facturas.filter(Factura.fecha_emision >= datetime.strptime(fecha_desde, '%Y-%m-%d').date())
    if fecha_hasta:
        facturas = facturas.filter(Factura.fecha_emision <= datetime.strptime(fecha_hasta, '%Y-%m-%d').date())
    
    facturas = facturas.order_by(Factura.fecha_emision.desc()).all()
    return render_template('facturas/list.html', facturas=facturas, 
                         q=q, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

@bp.route('/nueva', methods=['GET', 'POST'])
def nueva():
    if request.method == 'POST':
        cliente_id = int(request.form['cliente_id'])
        numero_factura = request.form['numero_factura'].strip()
        fecha_emision = datetime.strptime(request.form['fecha_emision'], '%Y-%m-%d').date()
        fecha_vencimiento = None
        
        talonario_id = request.form.get('talonario_id')
        if talonario_id:
            talonario_id = int(talonario_id)
        else:
            talonario_id = None
        
        iva_porcentaje = 0  # IVA siempre en 0
        notas = ''  # Notas siempre vacías
        actualizar_stock = True  # Siempre actualizar stock
        
        # Si no se envía número de factura, generarlo automáticamente a partir del talonario
        if not numero_factura:
            talonario = Talonario.query.get(talonario_id) if talonario_id else None
            if talonario:
                numero_factura = talonario.obtener_siguiente_numero()
            # Si no hay talonario o no hay número disponible, mantener vacío y dejar que la validación falle
        
        # Validar que el número de factura exista y no se repita
        if not numero_factura:
            flash('No se pudo generar un número de factura. Verifique el talonario seleccionado.', 'error')
            clientes = Cliente.query.filter_by(activo=True).order_by(Cliente.nombre).all()
            productos = Producto.query.filter_by(activo=True).order_by(Producto.nombre).all()
            talonarios = Talonario.query.filter_by(activo=True).all()
            return render_template('facturas/form.html', clientes=clientes, productos=productos, talonarios=talonarios)
        if Factura.query.filter_by(numero_factura=numero_factura).first():
            flash(f'El número de factura {numero_factura} ya existe', 'error')
            clientes = Cliente.query.filter_by(activo=True).order_by(Cliente.nombre).all()
            productos = Producto.query.filter_by(activo=True).order_by(Producto.nombre).all()
            talonarios = Talonario.query.filter_by(activo=True).all()
            return render_template('facturas/form.html', clientes=clientes, productos=productos, talonarios=talonarios)
        
        # Crear factura
        factura = Factura(
            numero_factura=numero_factura,
            cliente_id=cliente_id,
            talonario_id=talonario_id,
            fecha_emision=fecha_emision,
            fecha_vencimiento=fecha_vencimiento,
            iva=iva_porcentaje,
            notas=notas,
            subtotal=0,
            total=0,
        )
        db.session.add(factura)
        db.session.flush()
        
        # Agregar detalles desde la tabla
        subtotal = 0
        productos_ids = request.form.getlist('producto_id[]')
        cantidades = request.form.getlist('cantidad[]')
        precios = request.form.getlist('precio_unitario[]')
        
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
                flash(f'Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}', 'error')
                clientes = Cliente.query.filter_by(activo=True).order_by(Cliente.nombre).all()
                productos = Producto.query.filter_by(activo=True).order_by(Producto.nombre).all()
                talonarios = Talonario.query.filter_by(activo=True).all()
                return render_template('facturas/form.html', clientes=clientes, productos=productos, talonarios=talonarios)
            
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
            
            # Actualizar stock solo si está marcado
            if actualizar_stock:
                producto.stock -= cantidad
        
        # Calcular totales
        iva_monto = subtotal * (iva_porcentaje / 100)
        total = subtotal + iva_monto
        
        factura.subtotal = subtotal
        factura.iva = iva_monto
        factura.total = total
        
        db.session.commit()
        flash('Factura registrada correctamente', 'success')
        return redirect(url_for('facturas.detalle', id=factura.id))
    
    # GET: preparar datos con selección automática
    clientes = Cliente.query.filter_by(activo=True).order_by(Cliente.nombre).all()
    # Productos ordenados por stock descendente (más stock primero)
    productos = Producto.query.filter_by(activo=True).order_by(Producto.stock.desc(), Producto.nombre).all()
    talonarios = Talonario.query.filter_by(activo=True).order_by(Talonario.id.desc()).all()
    
    cliente_seleccionado_id = random.choice(clientes).id if clientes else None
    talonario_por_defecto = talonarios[0] if talonarios else None
    numero_factura_sugerido = None
    if talonario_por_defecto:
        numero_factura_sugerido = talonario_por_defecto.obtener_siguiente_numero()
    
    return render_template(
        'facturas/form.html',
        clientes=clientes,
        productos=productos,
        talonarios=talonarios,
        cliente_seleccionado_id=cliente_seleccionado_id,
        talonario_seleccionado_id=talonario_por_defecto.id if talonario_por_defecto else None,
        numero_factura_sugerido=numero_factura_sugerido or ''
    )

@bp.route('/<int:id>')
def detalle(id):
    factura = Factura.query.get_or_404(id)
    return render_template('facturas/detalle.html', factura=factura)

@bp.route('/<int:id>/anular', methods=['POST'])
def anular(id):
    """Anular una factura y revertir el stock"""
    factura = Factura.query.get_or_404(id)
    
    # Verificar que no esté ya anulada
    if factura.estado == 'ANULADA':
        flash('Esta factura ya está anulada', 'warning')
        return redirect(url_for('facturas.detalle', id=factura.id))
    
    try:
        # Revertir el stock de todos los productos de la factura
        for detalle in factura.detalles:
            producto = Producto.query.get(detalle.producto_id)
            if producto:
                producto.stock += detalle.cantidad
        
        # Cambiar el estado a ANULADA
        factura.estado = 'ANULADA'
        
        db.session.commit()
        flash(f'Factura {factura.numero_factura} anulada correctamente. El stock ha sido revertido.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al anular la factura: {str(e)}', 'error')
    
    return redirect(url_for('facturas.detalle', id=factura.id))


@bp.route('/api/clientes')
def api_clientes():
    clientes = Cliente.query.filter_by(activo=True).order_by(Cliente.nombre).all()
    return jsonify([c.to_dict() for c in clientes])

@bp.route('/facturar', methods=['GET', 'POST'])
def facturar():
    try:
        if request.method == 'POST':
            cliente_id = int(request.form['cliente_id'])
            numero_factura = request.form['numero_factura'].strip()
            fecha_emision = datetime.strptime(request.form['fecha_emision'], '%Y-%m-%d').date()
            fecha_vencimiento = None
            
            talonario_id = request.form.get('talonario_id')
            if talonario_id:
                talonario_id = int(talonario_id)
            else:
                talonario_id = None
            
            iva_porcentaje = 0  # IVA siempre en 0
            notas = ''  # Notas siempre vacías
            actualizar_stock = True  # Siempre actualizar stock
            
            # Si no se envía número de factura, generarlo automáticamente a partir del talonario
            if not numero_factura:
                talonario = Talonario.query.get(talonario_id) if talonario_id else None
                if talonario:
                    numero_factura = talonario.obtener_siguiente_numero()
            
            # Validar que el número de factura exista y no se repita
            if not numero_factura:
                flash('No se pudo generar un número de factura. Verifique el talonario seleccionado.', 'error')
                productos = Producto.query.filter_by(activo=True).order_by(Producto.stock.desc(), Producto.nombre).all()
                clientes = Cliente.query.filter_by(activo=True).order_by(Cliente.nombre).all()
                talonarios = Talonario.query.filter_by(activo=True).all()
                return render_template('facturas/facturar.html', productos=productos, clientes=clientes, talonarios=talonarios)
            if Factura.query.filter_by(numero_factura=numero_factura).first():
                flash(f'El número de factura {numero_factura} ya existe', 'error')
                productos = Producto.query.filter_by(activo=True).order_by(Producto.stock.desc(), Producto.nombre).all()
                clientes = Cliente.query.filter_by(activo=True).order_by(Cliente.nombre).all()
                talonarios = Talonario.query.filter_by(activo=True).all()
                return render_template('facturas/facturar.html', productos=productos, clientes=clientes, talonarios=talonarios)
            
            # Crear factura
            factura = Factura(
                numero_factura=numero_factura,
                cliente_id=cliente_id,
                talonario_id=talonario_id,
                fecha_emision=fecha_emision,
                fecha_vencimiento=fecha_vencimiento,
                iva=iva_porcentaje,
                notas=notas,
                subtotal=0,
                total=0,
            )
            db.session.add(factura)
            db.session.flush()
            
            # Agregar detalles desde la tabla
            subtotal = 0
            productos_ids = request.form.getlist('producto_id[]')
            cantidades = request.form.getlist('cantidad[]')
            precios = request.form.getlist('precio_unitario[]')
            
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
                    flash(f'Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}', 'error')
                    productos = Producto.query.filter_by(activo=True).order_by(Producto.stock.desc(), Producto.nombre).all()
                    clientes = Cliente.query.filter_by(activo=True).order_by(Cliente.nombre).all()
                    talonarios = Talonario.query.filter_by(activo=True).all()
                    return render_template('facturas/facturar.html', productos=productos, clientes=clientes, talonarios=talonarios)
                
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
                
                # Actualizar stock solo si está marcado
                if actualizar_stock:
                    producto.stock -= cantidad
            
            # Calcular totales
            iva_monto = subtotal * (iva_porcentaje / 100)
            total = subtotal + iva_monto
            
            factura.subtotal = subtotal
            factura.iva = iva_monto
            factura.total = total
            
            db.session.commit()
            flash('Factura registrada correctamente', 'success')
            return redirect(url_for('facturas.detalle', id=factura.id))
    
        # GET: preparar datos con selección automática
        productos = Producto.query.filter_by(activo=True).order_by(Producto.stock.desc(), Producto.nombre).all()
        clientes = Cliente.query.filter_by(activo=True).order_by(Cliente.nombre).all()
        talonarios = Talonario.query.filter_by(activo=True).order_by(Talonario.id.desc()).all()
        
        cliente_seleccionado_id = random.choice(clientes).id if clientes else None
        talonario_por_defecto = talonarios[0] if talonarios else None
        numero_factura_sugerido = None
        talonario_seleccionado_id = None
        
        # Preparar datos de talonarios para el frontend (con números sugeridos sin incrementar)
        talonarios_data = []
        for talonario in talonarios:
            try:
                numero_sugerido = talonario.sugerir_siguiente_numero()
            except Exception as e:
                # Si hay error al obtener el número sugerido, usar el número actual + 1
                import traceback
                print(f"Error al obtener número sugerido para talonario {talonario.id}: {e}")
                traceback.print_exc()
                numero_sugerido = f"{talonario.prefijo}{talonario.numero_actual + 1:04d}" if talonario.numero_actual else None
            
            talonarios_data.append({
                'id': talonario.id,
                'nombre': talonario.nombre,
                'prefijo': talonario.prefijo,
                'numero_actual': talonario.numero_actual,
                'numero_fin': talonario.numero_fin,
                'numero_sugerido': numero_sugerido
            })
            if talonario == talonario_por_defecto:
                talonario_seleccionado_id = talonario.id
                numero_factura_sugerido = numero_sugerido
        
        return render_template(
            'facturas/facturar.html',
            productos=productos,
            clientes=clientes,
            talonarios=talonarios,
            talonarios_data=talonarios_data,
            cliente_seleccionado_id=cliente_seleccionado_id,
            talonario_seleccionado_id=talonario_seleccionado_id,
            numero_factura_sugerido=numero_factura_sugerido or ''
        )
    except Exception as e:
        import traceback
        error_msg = f"Error en facturar: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        flash(f'Error al cargar la página de facturación: {str(e)}', 'error')
        # Intentar redirigir a la lista de facturas o mostrar error
        try:
            return redirect(url_for('facturas.listar'))
        except:
            from flask import make_response
            return make_response(f"Error interno: {error_msg}", 500)

@bp.route('/api/productos')
def api_productos():
    productos = Producto.query.filter_by(activo=True).order_by(Producto.nombre).all()
    return jsonify([p.to_dict() for p in productos])

@bp.route('/api/buscar')
def api_buscar():
    """API para búsqueda predictiva de facturas"""
    q = request.args.get('q', '')
    facturas = Factura.query
    if q:
        facturas = facturas.filter(Factura.numero_factura.contains(q))
    facturas = facturas.order_by(Factura.fecha_emision.desc()).limit(10).all()
    return jsonify([{
        'id': f.id,
        'numero_factura': f.numero_factura,
        'cliente_nombre': f.cliente.nombre if f.cliente else '',
        'total': float(f.total),
        'fecha_emision': f.fecha_emision.strftime('%d/%m/%Y') if f.fecha_emision else ''
    } for f in facturas])
