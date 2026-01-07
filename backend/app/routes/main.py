from flask import Blueprint, render_template
from app import db
from app.models import Cliente, Producto, Factura, Configuracion
from datetime import datetime, timedelta
from sqlalchemy import func

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Fechas para cálculos del mes
    hoy = datetime.now().date()
    inicio_mes = hoy.replace(day=1)
    inicio_mes_anterior = (inicio_mes - timedelta(days=1)).replace(day=1)
    fin_mes_anterior = inicio_mes - timedelta(days=1)
    
    # Facturas del mes actual
    facturas_mes = Factura.query.filter(
        Factura.fecha_emision >= inicio_mes,
        Factura.estado == 'PAGADA'
    ).all()
    
    # Facturas del mes anterior
    facturas_mes_anterior = Factura.query.filter(
        Factura.fecha_emision >= inicio_mes_anterior,
        Factura.fecha_emision <= fin_mes_anterior,
        Factura.estado == 'PAGADA'
    ).all()
    
    # Total facturado del mes
    total_facturado_mes = sum(f.total for f in facturas_mes)
    total_facturado_mes_anterior = sum(f.total for f in facturas_mes_anterior)
    
    # Total facturado general
    total_facturado_general = db.session.query(func.sum(Factura.total)).filter(
        Factura.estado == 'PAGADA'
    ).scalar() or 0
    
    # Últimas facturas
    ultimas_facturas = Factura.query.order_by(
        Factura.fecha_emision.desc()
    ).limit(5).all()
    
    # Obtener umbral de stock bajo desde configuración
    umbral_stock = Configuracion.obtener_int('umbral_stock_bajo', 10)
    
    # Productos con stock bajo (top 5)
    productos_stock_bajo = Producto.query.filter(
        Producto.stock < umbral_stock,
        Producto.activo == True
    ).order_by(Producto.stock.asc()).limit(5).all()
    
    stats = {
        'total_clientes': Cliente.query.filter_by(activo=True).count(),
        'total_productos': Producto.query.filter_by(activo=True).count(),
        'total_facturas': Factura.query.count(),
        'facturas_pagadas': Factura.query.filter_by(estado='PAGADA').count(),
        'facturas_anuladas': Factura.query.filter_by(estado='ANULADA').count(),
        'productos_stock_bajo': Producto.query.filter(Producto.stock < umbral_stock, Producto.activo == True).count(),
        'total_facturado_mes': total_facturado_mes,
        'total_facturado_mes_anterior': total_facturado_mes_anterior,
        'total_facturado_general': total_facturado_general,
        'facturas_mes': len(facturas_mes),
        'ultimas_facturas': ultimas_facturas,
        'productos_stock_bajo_lista': productos_stock_bajo
    }
    return render_template('index.html', stats=stats)

