from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file
from app import db
from app.models import Cliente, Factura
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from io import BytesIO
import os

bp = Blueprint('clientes', __name__)

@bp.route('/')
def listar():
    q = request.args.get('q', '')
    clientes = Cliente.query.filter_by(activo=True)
    if q:
        clientes = clientes.filter(Cliente.nombre.contains(q) | 
                                  Cliente.ruc_ci.contains(q))
    clientes = clientes.order_by(Cliente.nombre).all()
    return render_template('clientes/list.html', clientes=clientes, q=q)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        cliente = Cliente(
            nombre=request.form['nombre'],
            ruc_ci=request.form.get('ruc_ci', '')
        )
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente creado correctamente', 'success')
        return redirect(url_for('clientes.listar'))
    return render_template('clientes/form.html')

@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.ruc_ci = request.form.get('ruc_ci', '')
        db.session.commit()
        flash('Cliente actualizado correctamente', 'success')
        return redirect(url_for('clientes.listar'))
    return render_template('clientes/form.html', cliente=cliente)

@bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    cliente = Cliente.query.get_or_404(id)
    if cliente.facturas:
        flash('No se puede eliminar un cliente con facturas asociadas', 'error')
        return redirect(url_for('clientes.listar'))
    cliente.activo = False
    db.session.commit()
    flash('Cliente eliminado correctamente', 'success')
    return redirect(url_for('clientes.listar'))

@bp.route('/<int:id>/historial')
def historial(id):
    cliente = Cliente.query.get_or_404(id)
    facturas = Factura.query.filter_by(cliente_id=id).order_by(Factura.fecha_emision.desc()).all()
    return render_template('clientes/historial.html', cliente=cliente, facturas=facturas)

@bp.route('/api/buscar')
def api_buscar():
    q = request.args.get('q', '')
    clientes = Cliente.query.filter_by(activo=True)
    if q:
        clientes = clientes.filter(Cliente.nombre.contains(q))
    clientes = clientes.limit(10).all()
    return jsonify([c.to_dict() for c in clientes])

@bp.route('/importar', methods=['GET', 'POST'])
def importar():
    """Importar clientes desde Excel"""
    if request.method == 'POST':
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('clientes.importar'))
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('clientes.importar'))
        
        try:
            from openpyxl import load_workbook
            wb = load_workbook(archivo, data_only=True)
            ws = wb.active
            
            # Buscar la fila de encabezados
            header_row = None
            for row_idx, row in enumerate(ws.iter_rows(min_row=1, max_row=20), 1):
                valores = [str(cell.value).lower() if cell.value else '' for cell in row]
                if any('nombre' in v for v in valores):
                    header_row = row_idx
                    break
            
            if not header_row:
                flash('No se encontraron encabezados válidos en el archivo Excel', 'error')
                return redirect(url_for('clientes.importar'))
            
            # Leer encabezados
            headers = [str(cell.value).strip() if cell.value else '' for cell in ws[header_row]]
            
            # Buscar índices de columnas (más robusto)
            col_indices = {}
            for idx, header in enumerate(headers):
                if not header:
                    continue
                header_lower = str(header).lower().strip()
                
                # Nombre (más específico primero)
                if 'nombre' in header_lower:
                    if 'nombre' not in col_indices:
                        col_indices['nombre'] = idx
                # Cédula de Identidad (más específico primero)
                elif ('cédula' in header_lower or 'cedula' in header_lower) and 'identidad' in header_lower:
                    if 'ci' not in col_indices:
                        col_indices['ci'] = idx
                # CI o Cédula
                elif 'cedula' in header_lower or 'cédula' in header_lower or header_lower == 'ci':
                    if 'ci' not in col_indices:
                        col_indices['ci'] = idx
                # RUC/CI
                elif 'ruc' in header_lower and 'ci' in header_lower:
                    if 'ci' not in col_indices:
                        col_indices['ci'] = idx
                # RUC
                elif header_lower == 'ruc':
                    if 'ci' not in col_indices:
                        col_indices['ci'] = idx
            
            if 'nombre' not in col_indices:
                headers_encontrados = [h for h in headers if h]
                flash(f'No se encontró la columna "Nombre" en el archivo. Columnas encontradas: {", ".join(headers_encontrados) if headers_encontrados else "ninguna"}', 'error')
                return redirect(url_for('clientes.importar'))
            
            # Procesar filas
            clientes_importados = 0
            clientes_actualizados = 0
            errores = []
            
            for row_idx, row in enumerate(ws.iter_rows(min_row=header_row + 1), header_row + 1):
                # Obtener valores de las celdas
                nombre = None
                ci = None
                
                try:
                    # Leer nombre
                    if 'nombre' in col_indices:
                        nombre_cell = row[col_indices['nombre']]
                        nombre = str(nombre_cell.value).strip() if nombre_cell.value else None
                    
                    # Validar que haya nombre
                    if not nombre or nombre.lower() in ['', 'none', 'null']:
                        continue
                    
                    # Leer CI
                    if 'ci' in col_indices:
                        ci_cell = row[col_indices['ci']]
                        ci = str(ci_cell.value).strip() if ci_cell.value else None
                        # Limpiar CI (quitar espacios, guiones, etc.)
                        if ci:
                            ci = ci.replace('-', '').replace(' ', '').strip()
                            if ci.lower() in ['none', 'null', '']:
                                ci = None
                
                    # Buscar si ya existe por nombre o CI
                    cliente_existente = None
                    if ci:
                        cliente_existente = Cliente.query.filter_by(ruc_ci=ci, activo=True).first()
                    
                    if not cliente_existente:
                        cliente_existente = Cliente.query.filter_by(nombre=nombre, activo=True).first()
                    
                    if cliente_existente:
                        # Actualizar
                        cliente_existente.nombre = nombre
                        if ci:
                            cliente_existente.ruc_ci = ci
                        clientes_actualizados += 1
                    else:
                        # Crear nuevo
                        nuevo_cliente = Cliente(
                            nombre=nombre,
                            ruc_ci=ci if ci else ''
                        )
                        db.session.add(nuevo_cliente)
                        clientes_importados += 1
                        
                except Exception as e:
                    errores.append(f'Fila {row_idx}: {str(e)}')
                    continue
            
            db.session.commit()
            
            mensaje = f'Importación completada: {clientes_importados} nuevos, {clientes_actualizados} actualizados'
            if errores:
                mensaje += f'. Errores: {len(errores)}'
            flash(mensaje, 'success' if not errores else 'warning')
            
            return redirect(url_for('clientes.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al importar: {str(e)}', 'error')
            return redirect(url_for('clientes.importar'))
    
    return render_template('clientes/importar.html')

@bp.route('/descargar-plantilla')
def descargar_plantilla():
    """Genera y descarga la plantilla Excel para importar clientes"""
    # Crear workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'Plantilla Importación'
    
    # Estilos para encabezados
    header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
    header_font = Font(bold=True, color='FFFFFF', size=11)
    center_align = Alignment(horizontal='center', vertical='center')
    
    # Encabezados (usar nombres que el código reconozca fácilmente)
    headers = ['Nombre', 'CI']
    ws.append(headers)
    
    # Aplicar estilos a encabezados
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
    
    # Datos de ejemplo
    ejemplos = [
        ['Juan Pérez', '1234567'],
        ['María González', '7654321'],
        ['Carlos Rodríguez', '1122334'],
    ]
    
    for fila in ejemplos:
        ws.append(fila)
    
    # Ajustar ancho de columnas
    column_widths = [30, 20]
    for col_idx, width in enumerate(column_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=col_idx).column_letter].width = width
    
    # Guardar en memoria
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='plantilla_importacion_clientes.xlsx'
    )

