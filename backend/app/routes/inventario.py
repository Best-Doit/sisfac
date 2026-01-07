from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file
from app import db
from app.models import Producto
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from werkzeug.utils import secure_filename
import os
import uuid

bp = Blueprint('inventario', __name__)

@bp.route('/')
def listar():
    q = request.args.get('q', '')
    productos = Producto.query.filter_by(activo=True)
    if q:
        productos = productos.filter(Producto.nombre.contains(q) | 
                                     Producto.codigo.contains(q))
    productos = productos.order_by(Producto.nombre).all()
    return render_template('inventario/list.html', productos=productos, q=q)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        precio_1 = float(request.form['precio_1'])
        precio_2 = float(request.form.get('precio_2')) if request.form.get('precio_2') else None
        
        # Validar que P1 sea mayor o igual que P2
        if precio_2 and precio_2 > precio_1:
            flash('El Precio 2 no puede ser mayor que el Precio 1. P1 debe ser el precio más alto.', 'error')
            return render_template('inventario/form.html')
        
        # precio_unitario será igual a precio_1 (para compatibilidad)
        producto = Producto(
            codigo=request.form['codigo'],
            nombre=request.form['nombre'],
            descripcion=request.form.get('descripcion', ''),
            precio_unitario=precio_1,  # Mantener para compatibilidad, pero igual a precio_1
            precio_1=precio_1,
            precio_2=precio_2,
            stock=int(request.form.get('stock', 0))
        )
        db.session.add(producto)
        db.session.commit()
        flash('Producto creado correctamente', 'success')
        return redirect(url_for('inventario.listar'))
    return render_template('inventario/form.html')

@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        precio_1 = float(request.form['precio_1'])
        precio_2 = float(request.form.get('precio_2')) if request.form.get('precio_2') else None
        
        # Validar que P1 sea mayor o igual que P2
        if precio_2 and precio_2 > precio_1:
            flash('El Precio 2 no puede ser mayor que el Precio 1. P1 debe ser el precio más alto.', 'error')
            return render_template('inventario/form.html', producto=producto)
        
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form.get('descripcion', '')
        producto.precio_unitario = precio_1  # Mantener para compatibilidad
        producto.precio_1 = precio_1
        producto.precio_2 = precio_2
        producto.stock = int(request.form.get('stock', 0))
        db.session.commit()
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('inventario.listar'))
    return render_template('inventario/form.html', producto=producto)

@bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    producto = Producto.query.get_or_404(id)
    if producto.detalles:
        flash('No se puede eliminar un producto con facturas asociadas', 'error')
        return redirect(url_for('inventario.listar'))
    producto.activo = False
    db.session.commit()
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('inventario.listar'))

@bp.route('/api/buscar')
def api_buscar():
    q = request.args.get('q', '')
    productos = Producto.query.filter_by(activo=True)
    if q:
        productos = productos.filter(Producto.nombre.contains(q) | 
                                    Producto.codigo.contains(q))
    productos = productos.limit(10).all()
    return jsonify([p.to_dict() for p in productos])

@bp.route('/api/<int:id>/stock')
def api_stock(id):
    producto = Producto.query.get_or_404(id)
    return jsonify({
        'producto_id': producto.id,
        'stock_disponible': producto.stock,
        'stock_bajo': producto.stock < 10
    })

@bp.route('/importar', methods=['GET', 'POST'])
def importar():
    if request.method == 'POST':
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('inventario.importar'))
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('inventario.importar'))
        
        if not archivo.filename.endswith(('.xlsx', '.xls')):
            flash('El archivo debe ser Excel (.xlsx o .xls)', 'error')
            return redirect(url_for('inventario.importar'))
        
        # Guardar archivo temporalmente
        filename = secure_filename(archivo.filename)
        temp_filename = f"{uuid.uuid4()}_{filename}"
        upload_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, temp_filename)
        archivo.save(filepath)
        
        try:
            # Leer archivo Excel
            wb = load_workbook(filepath, data_only=True)
            ws = wb.active
            
            # Buscar la fila de encabezados
            header_row = None
            for row_idx, row in enumerate(ws.iter_rows(min_row=1, max_row=20), 1):
                valores = [str(cell.value).lower() if cell.value else '' for cell in row]
                if any('nombre' in v or 'producto' in v for v in valores):
                    header_row = row_idx
                    break
            
            if not header_row:
                flash('No se encontraron encabezados válidos en el archivo Excel', 'error')
                os.remove(filepath)
                return redirect(url_for('inventario.importar'))
            
            # Mapear columnas
            headers = [str(cell.value).strip() if cell.value else '' for cell in ws[header_row]]
            col_indices = {}
            
            # Buscar columnas por diferentes nombres posibles
            # Nota: El orden importa - primero buscar nombres más específicos
            for idx, header in enumerate(headers):
                if not header:
                    continue
                header_lower = str(header).lower().strip()
                
                # Nombre de producto (más específico primero)
                if 'nombre' in header_lower and 'producto' in header_lower:
                    if 'nombre' not in col_indices:
                        col_indices['nombre'] = idx
                elif 'nombre' in header_lower or 'producto' in header_lower:
                    if 'nombre' not in col_indices:
                        col_indices['nombre'] = idx
                # Código
                elif 'codigo' in header_lower or 'código' in header_lower:
                    if 'codigo' not in col_indices:
                        col_indices['codigo'] = idx
                # Precio de compra
                elif 'precio de compra' in header_lower or 'precio compra' in header_lower:
                    if 'precio_compra' not in col_indices:
                        col_indices['precio_compra'] = idx
                # Precio de Venta 1 (más específico primero)
                elif ('precio' in header_lower and 'venta' in header_lower and '1' in header_lower) or \
                     'precio de venta 1' in header_lower or 'precio venta 1' in header_lower or \
                     'p1' in header_lower or 'precio 1' in header_lower:
                    if 'precio_1' not in col_indices:
                        col_indices['precio_1'] = idx
                # Precio de Venta 2 (más específico primero)
                elif ('precio' in header_lower and 'venta' in header_lower and '2' in header_lower) or \
                     'precio de venta 2' in header_lower or 'precio venta 2' in header_lower or \
                     'p2' in header_lower or 'precio 2' in header_lower:
                    if 'precio_2' not in col_indices:
                        col_indices['precio_2'] = idx
                # Precio unitario (solo si no se asignó precio_1 o precio_2)
                elif ('precio unitario' in header_lower or 'precio_unitario' in header_lower) and \
                     'precio_1' not in col_indices and 'precio_2' not in col_indices:
                    if 'precio' not in col_indices:
                        col_indices['precio'] = idx
                # Precio genérico (solo si no hay otros precios asignados)
                elif 'precio' in header_lower and 'precio_1' not in col_indices and 'precio_2' not in col_indices:
                    if 'precio' not in col_indices:
                        col_indices['precio'] = idx
                # Saldo para facturar (tiene prioridad sobre Cantidad)
                elif 'saldo para facturar' in header_lower or ('saldo' in header_lower and 'facturar' in header_lower):
                    col_indices['stock'] = idx  # Siempre sobrescribir si existe
                # Cantidad facturada
                elif 'cantidad facturada' in header_lower:
                    if 'cantidad_facturada' not in col_indices:
                        col_indices['cantidad_facturada'] = idx
                # Stock (genérico)
                elif 'stock' in header_lower:
                    if 'stock' not in col_indices:
                        col_indices['stock'] = idx
                # Cantidad (solo si no se asignó stock - tiene menor prioridad)
                elif 'cantidad' in header_lower and 'facturada' not in header_lower:
                    if 'stock' not in col_indices:
                        col_indices['stock'] = idx
                # Descripción
                elif 'descripcion' in header_lower or 'descripción' in header_lower:
                    if 'descripcion' not in col_indices:
                        col_indices['descripcion'] = idx
            
            if 'nombre' not in col_indices:
                headers_encontrados = [h for h in headers if h]
                flash(f'No se encontró la columna "Nombre" o "Producto" en el archivo. Columnas encontradas: {", ".join(headers_encontrados) if headers_encontrados else "ninguna"}', 'error')
                os.remove(filepath)
                return redirect(url_for('inventario.importar'))
            
            # Procesar filas
            productos_creados = 0
            productos_actualizados = 0
            errores = []
            
            for row_idx, row in enumerate(ws.iter_rows(min_row=header_row + 1), header_row + 1):
                # Obtener valores
                nombre = None
                codigo = None
                precio = 0
                precio_1 = None
                precio_2 = None
                stock = 0
                descripcion = ''
                
                try:
                    if 'nombre' in col_indices:
                        nombre_cell = row[col_indices['nombre']]
                        nombre = str(nombre_cell.value).strip() if nombre_cell.value else None
                    
                    if not nombre or nombre.lower() in ['', 'none', 'null']:
                        continue
                    
                    if 'codigo' in col_indices:
                        codigo_cell = row[col_indices['codigo']]
                        codigo = str(codigo_cell.value).strip() if codigo_cell.value else None
                    
                    if 'precio' in col_indices:
                        precio_cell = row[col_indices['precio']]
                        try:
                            precio = float(precio_cell.value) if precio_cell.value else 0
                        except (ValueError, TypeError):
                            precio = 0
                    
                    # Leer precio_1 si existe la columna
                    if 'precio_1' in col_indices:
                        precio_1_cell = row[col_indices['precio_1']]
                        try:
                            precio_1 = float(precio_1_cell.value) if precio_1_cell.value else None
                        except (ValueError, TypeError):
                            precio_1 = None
                    
                    # Leer precio_2 si existe la columna
                    if 'precio_2' in col_indices:
                        precio_2_cell = row[col_indices['precio_2']]
                        try:
                            precio_2 = float(precio_2_cell.value) if precio_2_cell.value else None
                        except (ValueError, TypeError):
                            precio_2 = None
                    
                    if 'stock' in col_indices:
                        stock_cell = row[col_indices['stock']]
                        try:
                            stock = int(float(stock_cell.value)) if stock_cell.value else 0
                        except (ValueError, TypeError):
                            stock = 0
                    
                    if 'descripcion' in col_indices:
                        desc_cell = row[col_indices['descripcion']]
                        descripcion = str(desc_cell.value).strip() if desc_cell.value else ''
                    
                    # Generar código si no existe
                    if not codigo:
                        codigo = f"PROD-{uuid.uuid4().hex[:8].upper()}"
                    
                    # Validar que P1 sea mayor o igual que P2
                    if precio_1 and precio_2 and precio_2 > precio_1:
                        errores.append(f"Fila {row_num}: El Precio 2 no puede ser mayor que el Precio 1. P1 debe ser el precio más alto.")
                        continue
                    
                    # Asegurar que precio_1 tenga un valor (es obligatorio)
                    if not precio_1 or precio_1 == 0:
                        # Si no hay precio_1, intentar usar precio_unitario como fallback
                        if precio and precio > 0:
                            precio_1 = precio
                        else:
                            errores.append(f"Fila {row_num}: El Precio 1 es obligatorio.")
                            continue
                    
                    # precio_unitario será igual a precio_1 (para compatibilidad)
                    precio = precio_1
                    
                    # Verificar si el producto ya existe (por código o nombre)
                    producto_existente = None
                    if codigo:
                        producto_existente = Producto.query.filter_by(codigo=codigo, activo=True).first()
                    
                    if not producto_existente:
                        producto_existente = Producto.query.filter_by(nombre=nombre, activo=True).first()
                    
                    if producto_existente:
                        # Actualizar producto existente
                        producto_existente.nombre = nombre
                        producto_existente.precio_unitario = precio_1  # Compatibilidad
                        producto_existente.precio_1 = precio_1
                        producto_existente.precio_2 = precio_2
                        producto_existente.stock = stock
                        if descripcion:
                            producto_existente.descripcion = descripcion
                        productos_actualizados += 1
                    else:
                        # Crear nuevo producto
                        nuevo_producto = Producto(
                            codigo=codigo,
                            nombre=nombre,
                            descripcion=descripcion,
                            precio_unitario=precio_1,  # Compatibilidad, igual a precio_1
                            precio_1=precio_1,
                            precio_2=precio_2 if precio_2 else None,
                            stock=stock
                        )
                        db.session.add(nuevo_producto)
                        productos_creados += 1
                
                except Exception as e:
                    errores.append(f"Fila {row_idx}: {str(e)}")
                    continue
            
            # Guardar cambios
            db.session.commit()
            
            # Eliminar archivo temporal
            os.remove(filepath)
            
            # Mensaje de resultado
            mensaje = f"Importación completada: {productos_creados} productos creados, {productos_actualizados} productos actualizados"
            if errores:
                mensaje += f". {len(errores)} errores encontrados."
                flash(mensaje, 'warning')
            else:
                flash(mensaje, 'success')
            
            return redirect(url_for('inventario.listar'))
        
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            flash(f'Error al procesar el archivo: {str(e)}', 'error')
            return redirect(url_for('inventario.importar'))
    
    return render_template('inventario/importar.html')

@bp.route('/descargar-plantilla')
def descargar_plantilla():
    """Genera y descarga la plantilla Excel para importar productos"""
    # Crear workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'Plantilla Importación'
    
    # Estilos para encabezados
    header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
    header_font = Font(bold=True, color='FFFFFF', size=11)
    center_align = Alignment(horizontal='center', vertical='center')
    
    # Encabezados
    headers = ['Nombre de Producto', 'Cantidad', 'Precio de Compra', 'Precio de Venta 1', 'Precio de Venta 2', 'Saldo para Facturar', 'Cantidad Facturada']
    ws.append(headers)
    
    # Aplicar estilos a encabezados
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
    
    # Datos de ejemplo
    ejemplos = [
        ['Producto Ejemplo 1', 100, 50.00, 75.00, 80.00, 100, 0],
        ['Producto Ejemplo 2', 50, 30.00, 45.00, 50.00, 50, 0],
        ['Producto Ejemplo 3', 200, 25.00, 40.00, 45.00, 200, 0],
    ]
    
    for fila in ejemplos:
        ws.append(fila)
    
    # Ajustar ancho de columnas
    column_widths = [25, 12, 15, 15, 15, 18, 18]
    for col_idx, width in enumerate(column_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=col_idx).column_letter].width = width
    
    # Guardar en memoria
    from io import BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='plantilla_importacion_productos.xlsx'
    )

@bp.route('/exportar')
def exportar():
    """Exporta el inventario actual a un archivo Excel"""
    q = request.args.get('q', '')
    
    productos_query = Producto.query.filter_by(activo=True)
    if q:
        productos_query = productos_query.filter(
            Producto.nombre.contains(q) | Producto.codigo.contains(q)
        )
    productos = productos_query.order_by(Producto.nombre).all()
    
    # Crear workbook en memoria
    wb = Workbook()
    ws = wb.active
    ws.title = 'Inventario'
    
    # Estilos de encabezado
    header_fill = PatternFill(start_color='2563EB', end_color='2563EB', fill_type='solid')
    header_font = Font(bold=True, color='FFFFFF', size=11)
    center_align = Alignment(horizontal='center', vertical='center')
    
    # Encabezados
    headers = [
        'Código',
        'Nombre',
        'Descripción',
        'Precio 1',
        'Precio 2',
        'Stock',
        'Fecha Registro'
    ]
    ws.append(headers)
    
    for col_idx, _ in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
    
    # Datos
    for producto in productos:
        ws.append([
            producto.codigo,
            producto.nombre,
            producto.descripcion or '',
            producto.precio_1 or producto.precio_unitario or 0,
            producto.precio_2 if producto.precio_2 is not None else '',
            producto.stock
        ])
    
    # Ajustar ancho de columnas
    column_widths = [18, 30, 40, 16, 12, 12, 12, 10, 18, 16]
    for col_idx, width in enumerate(column_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=col_idx).column_letter].width = width
    
    # Guardar en memoria
    from io import BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='inventario_sisfac.xlsx'
    )
