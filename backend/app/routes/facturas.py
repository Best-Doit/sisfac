from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, make_response
from app import db
from app.models import Factura, Producto, Cliente
from app.services.facturacion_service import FacturacionService
from datetime import datetime
import random
import traceback

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
        # Convertir fecha_emision a date object
        fecha_emision = datetime.strptime(request.form['fecha_emision'], '%Y-%m-%d').date()
        # Crear copia mutable del form para modificar fecha_emision
        form_data = request.form.copy()
        form_data['fecha_emision'] = fecha_emision
        
        # Crear un objeto similar a request.form pero con fecha convertida
        class FormData:
            def __init__(self, data):
                self._data = data
            
            def __getitem__(self, key):
                return self._data[key]
            
            def get(self, key, default=None):
                return self._data.get(key, default)
            
            def getlist(self, key):
                return request.form.getlist(key)
        
        form_obj = FormData(form_data)
        factura, error = FacturacionService.crear_factura(form_obj)
        
        if error:
            flash(error, 'error')
            datos = FacturacionService.obtener_datos_formulario()
            return render_template('facturas/form.html', **datos)
        
        flash('Factura registrada correctamente', 'success')
        return redirect(url_for('facturas.detalle', id=factura.id))
    
    # GET: preparar datos
    datos = FacturacionService.obtener_datos_formulario()
    cliente_seleccionado_id = random.choice(datos['clientes']).id if datos['clientes'] else None
    talonario_por_defecto = datos['talonarios'][0] if datos['talonarios'] else None
    numero_factura_sugerido = None
    if talonario_por_defecto:
        numero_factura_sugerido = talonario_por_defecto.obtener_siguiente_numero()
    
    return render_template(
        'facturas/form.html',
        clientes=datos['clientes'],
        productos=datos['productos'],
        talonarios=datos['talonarios'],
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
            # Convertir fecha_emision a date object
            fecha_emision = datetime.strptime(request.form['fecha_emision'], '%Y-%m-%d').date()
            # Crear copia mutable del form para modificar fecha_emision
            form_data = request.form.copy()
            form_data['fecha_emision'] = fecha_emision
            
            # Crear un objeto similar a request.form pero con fecha convertida
            class FormData:
                def __init__(self, data):
                    self._data = data
                
                def __getitem__(self, key):
                    return self._data[key]
                
                def get(self, key, default=None):
                    return self._data.get(key, default)
                
                def getlist(self, key):
                    return request.form.getlist(key)
            
            form_obj = FormData(form_data)
            factura, error = FacturacionService.crear_factura(form_obj)
            
            if error:
                flash(error, 'error')
                datos = FacturacionService.obtener_datos_formulario(con_numeros_sugeridos=True)
                return render_template('facturas/facturar.html', 
                                     productos=datos['productos'],
                                     clientes=datos['clientes'],
                                     talonarios=datos['talonarios'],
                                     talonarios_data=datos.get('talonarios_data', []))
            
            flash('Factura registrada correctamente', 'success')
            return redirect(url_for('facturas.detalle', id=factura.id))
        
        # GET: preparar datos con selección automática
        datos = FacturacionService.obtener_datos_formulario(con_numeros_sugeridos=True)
        
        cliente_seleccionado_id = random.choice(datos['clientes']).id if datos['clientes'] else None
        talonario_por_defecto = datos['talonarios'][0] if datos['talonarios'] else None
        talonario_seleccionado_id = None
        numero_factura_sugerido = None
        
        if talonario_por_defecto and 'talonarios_data' in datos:
            for talonario_data in datos['talonarios_data']:
                if talonario_data['id'] == talonario_por_defecto.id:
                    talonario_seleccionado_id = talonario_data['id']
                    numero_factura_sugerido = talonario_data.get('numero_sugerido', '')
                    break
        
        return render_template(
            'facturas/facturar.html',
            productos=datos['productos'],
            clientes=datos['clientes'],
            talonarios=datos['talonarios'],
            talonarios_data=datos.get('talonarios_data', []),
            cliente_seleccionado_id=cliente_seleccionado_id,
            talonario_seleccionado_id=talonario_seleccionado_id,
            numero_factura_sugerido=numero_factura_sugerido or ''
        )
    except Exception as e:
        error_msg = f"Error en facturar: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        flash(f'Error al cargar la página de facturación: {str(e)}', 'error')
        try:
            return redirect(url_for('facturas.listar'))
        except:
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
