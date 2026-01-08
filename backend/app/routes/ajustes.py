from flask import Blueprint, render_template, request, flash, send_file, jsonify, redirect, url_for, make_response
from app import db
from app.models import Cliente, Producto, Factura, DetalleFactura, Talonario, Configuracion
from sqlalchemy import text, func
import os
import sys
import shutil
from datetime import datetime, timedelta
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

bp = Blueprint('ajustes', __name__)

def get_db_path():
    """Obtiene la ruta del archivo de base de datos"""
    try:
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
    except Exception as e:
        import traceback
        print(f"❌ Error en get_db_path: {e}")
        traceback.print_exc()
        # Fallback: usar directorio actual
        return os.path.join(os.getcwd(), 'sisfac.db')

def get_backups_dir():
    """Obtiene o crea el directorio de backups"""
    try:
        # Si está empaquetado con PyInstaller
        if getattr(sys, 'frozen', False):
            # Cuando está empaquetado y ejecutado desde Electron:
            # - Los recursos están en un sistema de archivos de solo lectura (AppImage)
            # - Necesitamos usar un directorio escribible en el home del usuario
            
            # Usar el directorio home del usuario para guardar los backups
            home_dir = os.path.expanduser('~')
            app_data_dir = os.path.join(home_dir, '.sisfac')
            backups_dir = os.path.join(app_data_dir, 'backups')
        else:
            # Modo desarrollo: usar ruta relativa al proyecto
            basedir = os.path.abspath(os.path.dirname(__file__))
            backups_dir = os.path.join(basedir, "..", "..", "backups")
            backups_dir = os.path.abspath(backups_dir)
        
        # Crear el directorio si no existe
        os.makedirs(backups_dir, exist_ok=True)
        return backups_dir
    except Exception as e:
        import traceback
        print(f"❌ Error en get_backups_dir: {e}")
        traceback.print_exc()
        # Fallback: usar directorio actual
        backups_dir = os.path.join(os.getcwd(), 'backups')
        os.makedirs(backups_dir, exist_ok=True)
        return backups_dir

@bp.route('/')
def index():
    """Pantalla principal de ajustes"""
    try:
        db_path = get_db_path()
        db_size = 0
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path)
        
        # Listar backups disponibles
        backups_dir = get_backups_dir()
        backups = []
        try:
            if os.path.exists(backups_dir):
                for file in os.listdir(backups_dir):
                    if file.endswith('.db'):
                        file_path = os.path.join(backups_dir, file)
                        backups.append({
                            'nombre': file,
                            'fecha': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d/%m/%Y %H:%M:%S'),
                            'tamaño': os.path.getsize(file_path)
                        })
                backups.sort(key=lambda x: x['fecha'], reverse=True)
        except Exception as e:
            print(f"⚠️ Error al listar backups: {e}")
            backups = []
        
        # Obtener configuraciones
        try:
            umbral_stock = Configuracion.obtener_int('umbral_stock_bajo', 10)
        except Exception as e:
            print(f"⚠️ Error al obtener configuración: {e}")
            umbral_stock = 10
        
        # Estadísticas del sistema
        stats = {
            'total_clientes': 0,
            'total_productos': 0,
            'total_facturas': 0,
            'facturas_pagadas': 0,
            'facturas_anuladas': 0,
            'total_facturado': 0,
            'productos_stock_bajo': 0
        }
        
        try:
            stats['total_clientes'] = Cliente.query.filter_by(activo=True).count()
        except Exception as e:
            print(f"⚠️ Error al contar clientes: {e}")
        
        try:
            stats['total_productos'] = Producto.query.filter_by(activo=True).count()
        except Exception as e:
            print(f"⚠️ Error al contar productos: {e}")
        
        try:
            stats['total_facturas'] = Factura.query.count()
        except Exception as e:
            print(f"⚠️ Error al contar facturas: {e}")
        
        try:
            stats['facturas_pagadas'] = Factura.query.filter_by(estado='PAGADA').count()
        except Exception as e:
            print(f"⚠️ Error al contar facturas pagadas: {e}")
        
        try:
            stats['facturas_anuladas'] = Factura.query.filter_by(estado='ANULADA').count()
        except Exception as e:
            print(f"⚠️ Error al contar facturas anuladas: {e}")
        
        try:
            stats['total_facturado'] = db.session.query(func.sum(Factura.total)).filter(
                Factura.estado == 'PAGADA'
            ).scalar() or 0
        except Exception as e:
            print(f"⚠️ Error al calcular total facturado: {e}")
        
        try:
            stats['productos_stock_bajo'] = Producto.query.filter(
                Producto.stock < umbral_stock,
                Producto.activo == True
            ).count()
        except Exception as e:
            print(f"⚠️ Error al contar productos con stock bajo: {e}")
        
        return render_template('ajustes/index.html', 
                             db_size=db_size, 
                             backups=backups,
                             umbral_stock=umbral_stock,
                             stats=stats)
    except Exception as e:
        import traceback
        error_msg = f"Error en ajustes.index: {str(e)}"
        print(f"❌ {error_msg}")
        traceback.print_exc()
        flash(f'Error al cargar la página de ajustes: {str(e)}', 'error')
        # Intentar mostrar la página con valores por defecto
        return render_template('ajustes/index.html', 
                             db_size=0, 
                             backups=[],
                             umbral_stock=10,
                             stats={
                                 'total_clientes': 0,
                                 'total_productos': 0,
                                 'total_facturas': 0,
                                 'facturas_pagadas': 0,
                                 'facturas_anuladas': 0,
                                 'total_facturado': 0,
                                 'productos_stock_bajo': 0
                             })

@bp.route('/backup', methods=['POST'])
def crear_backup():
    """Crear una copia de seguridad de la base de datos"""
    try:
        db_path = get_db_path()
        if not os.path.exists(db_path):
            flash('No se encontró la base de datos', 'error')
            return jsonify({'success': False, 'message': 'No se encontró la base de datos'})
        
        backups_dir = get_backups_dir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'sisfac_backup_{timestamp}.db'
        backup_path = os.path.join(backups_dir, backup_filename)
        
        shutil.copy2(db_path, backup_path)
        
        flash(f'Backup creado: {backup_filename}', 'success')
        return jsonify({'success': True, 'message': f'Backup creado: {backup_filename}'})
    except Exception as e:
        flash(f'Error al crear backup: {str(e)}', 'error')
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/restaurar', methods=['POST'])
def restaurar_backup():
    """Restaurar un backup"""
    try:
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return jsonify({'success': False, 'message': 'No se seleccionó ningún archivo'})
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return jsonify({'success': False, 'message': 'No se seleccionó ningún archivo'})
        
        if not archivo.filename.endswith('.db'):
            flash('El archivo debe ser una base de datos (.db)', 'error')
            return jsonify({'success': False, 'message': 'El archivo debe ser una base de datos (.db)'})
        
        db_path = get_db_path()
        
        # Cerrar todas las conexiones de la base de datos antes de restaurar
        db.session.close()
        
        # Crear backup del estado actual antes de restaurar
        if os.path.exists(db_path):
            backups_dir = get_backups_dir()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_actual = os.path.join(backups_dir, f'sisfac_antes_restaurar_{timestamp}.db')
            shutil.copy2(db_path, backup_actual)
        
        # Guardar el archivo subido
        archivo.save(db_path)
        
        flash('Backup restaurado correctamente. Reinicia la aplicación.', 'success')
        return jsonify({'success': True, 'message': 'Backup restaurado correctamente'})
    except Exception as e:
        flash(f'Error al restaurar backup: {str(e)}', 'error')
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/descargar-backup/<nombre>')
def descargar_backup(nombre):
    """Descargar un archivo de backup"""
    try:
        backups_dir = get_backups_dir()
        backup_path = os.path.join(backups_dir, nombre)
        
        if not os.path.exists(backup_path) or not nombre.endswith('.db'):
            flash('Archivo no encontrado', 'error')
            return jsonify({'success': False, 'message': 'Archivo no encontrado'})
        
        return send_file(backup_path, as_attachment=True, download_name=nombre)
    except Exception as e:
        flash(f'Error al descargar backup: {str(e)}', 'error')
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/borrar-datos', methods=['POST'])
def borrar_datos():
    """Borrar todos los datos de las tablas principales"""
    try:
        import traceback
        
        # Detectar si es una llamada AJAX/JSON o un POST normal
        is_ajax = request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        # Obtener confirmación del formulario o JSON (acepta 'confirmar' o 'confirmacion')
        if request.is_json:
            data = request.get_json(silent=True) or {}
            confirmacion = data.get('confirmar') or data.get('confirmacion') or ''
        else:
            confirmacion = request.form.get('confirmar') or request.form.get('confirmacion') or ''
        
        print(f"🔍 Confirmación recibida: '{confirmacion}'")
        
        # Validar confirmación (acepta "borrar" o "BORRAR")
        confirmacion_limpia = confirmacion.strip().lower()
        if confirmacion_limpia != 'borrar':
            msg = f'Debes escribir "BORRAR" para confirmar. Recibido: "{confirmacion}"'
            print(f"❌ {msg}")
            if is_ajax:
                return jsonify({'success': False, 'message': msg})
            flash(msg, 'error')
            return redirect(url_for('ajustes.index'))
        
        print("✅ Confirmación válida, procediendo a borrar datos...")
        
        # Crear backup antes de borrar
        db_path = get_db_path()
        backup_creado = False
        if os.path.exists(db_path):
            try:
                backups_dir = get_backups_dir()
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_antes_borrar = os.path.join(backups_dir, f'sisfac_antes_borrar_{timestamp}.db')
                shutil.copy2(db_path, backup_antes_borrar)
                backup_creado = True
                print(f"✅ Backup creado: {backup_antes_borrar}")
            except Exception as e:
                print(f"⚠️ Error al crear backup: {e}")
                # Continuar aunque falle el backup
        
        # Deshabilitar temporalmente las foreign keys en SQLite
        try:
            db.session.execute(text('PRAGMA foreign_keys = OFF'))
            print("✅ Foreign keys deshabilitadas")
        except Exception as e:
            print(f"⚠️ Error al deshabilitar foreign keys: {e}")
        
        # Borrar datos de todas las tablas en el orden correcto (primero las dependientes)
        try:
            print("🗑️ Borrando DetalleFactura...")
            count_detalles = db.session.query(DetalleFactura).count()
            db.session.query(DetalleFactura).delete(synchronize_session=False)
            print(f"   Eliminados {count_detalles} detalles de factura")
            
            print("🗑️ Borrando Factura...")
            count_facturas = db.session.query(Factura).count()
            db.session.query(Factura).delete(synchronize_session=False)
            print(f"   Eliminadas {count_facturas} facturas")
            
            print("🗑️ Borrando Producto...")
            count_productos = db.session.query(Producto).count()
            db.session.query(Producto).delete(synchronize_session=False)
            print(f"   Eliminados {count_productos} productos")
            
            print("🗑️ Borrando Cliente...")
            count_clientes = db.session.query(Cliente).count()
            db.session.query(Cliente).delete(synchronize_session=False)
            print(f"   Eliminados {count_clientes} clientes")
            
            print("🗑️ Borrando Talonario...")
            count_talonarios = db.session.query(Talonario).count()
            db.session.query(Talonario).delete(synchronize_session=False)
            print(f"   Eliminados {count_talonarios} talonarios")
            
            print("💾 Guardando cambios...")
            db.session.commit()
            print("✅ Cambios guardados correctamente")
            
            # Verificar que se borraron los datos
            total_restante = (
                db.session.query(DetalleFactura).count() +
                db.session.query(Factura).count() +
                db.session.query(Producto).count() +
                db.session.query(Cliente).count() +
                db.session.query(Talonario).count()
            )
            if total_restante > 0:
                print(f"⚠️ Advertencia: Aún quedan {total_restante} registros en las tablas")
            else:
                print("✅ Verificación: Todas las tablas están vacías")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al borrar datos: {e}")
            traceback.print_exc()
            raise e
        finally:
            # Rehabilitar las foreign keys
            try:
                db.session.execute(text('PRAGMA foreign_keys = ON'))
                print("✅ Foreign keys rehabilitadas")
            except Exception as e:
                print(f"⚠️ Error al rehabilitar foreign keys: {e}")
        
        msg_ok = 'Datos borrados correctamente.'
        if backup_creado:
            msg_ok += ' Se creó un backup automático.'
        
        print(f"✅ {msg_ok}")
        
        if is_ajax:
            return jsonify({'success': True, 'message': msg_ok})
        flash(msg_ok, 'success')
        return redirect(url_for('ajustes.index'))
    except Exception as e:
        import traceback
        db.session.rollback()
        msg_err = f'Error al borrar datos: {str(e)}'
        print(f"❌ {msg_err}")
        traceback.print_exc()
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': msg_err})
        flash(msg_err, 'error')
        return redirect(url_for('ajustes.index'))

@bp.route('/configuracion', methods=['POST'])
def guardar_configuracion():
    """Guardar configuración del sistema"""
    try:
        umbral_stock = request.form.get('umbral_stock', '10')
        
        Configuracion.establecer('umbral_stock_bajo', umbral_stock, 'Umbral de stock bajo para alertas')
        
        flash('Configuración guardada correctamente', 'success')
        return jsonify({'success': True, 'message': 'Configuración guardada correctamente'})
    except Exception as e:
        flash(f'Error al guardar configuración: {str(e)}', 'error')
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/exportar-datos')
def exportar_datos():
    """Exportar todos los datos a Excel"""
    try:
        wb = Workbook()
        
        # Hoja de Clientes
        ws_clientes = wb.active
        ws_clientes.title = "Clientes"
        headers = ['ID', 'Nombre', 'CI/RUC', 'Dirección', 'Teléfono', 'Email', 'Fecha Registro']
        ws_clientes.append(headers)
        for cliente in Cliente.query.filter_by(activo=True).all():
            ws_clientes.append([
                cliente.id,
                cliente.nombre,
                cliente.ruc_ci or '',
                cliente.direccion or '',
                cliente.telefono or '',
                cliente.email or '',
                cliente.fecha_registro.strftime('%d/%m/%Y %H:%M:%S') if cliente.fecha_registro else ''
            ])
        
        # Hoja de Productos
        ws_productos = wb.create_sheet("Productos")
        headers = ['ID', 'Código', 'Nombre', 'Descripción', 'Precio Principal', 'Precio P1', 'Precio P2', 'Stock', 'Fecha Registro']
        ws_productos.append(headers)
        for producto in Producto.query.filter_by(activo=True).all():
            ws_productos.append([
                producto.id,
                producto.codigo,
                producto.nombre,
                producto.descripcion or '',
                producto.precio_unitario,
                producto.precio_1 or '',
                producto.precio_2 or '',
                producto.stock,
                producto.fecha_registro.strftime('%d/%m/%Y %H:%M:%S') if producto.fecha_registro else ''
            ])
        
        # Hoja de Talonarios
        ws_talonarios = wb.create_sheet("Talonarios")
        headers = ['ID', 'Nombre', 'Prefijo', 'Número Inicio', 'Número Fin', 'Número Actual', 'Activo']
        ws_talonarios.append(headers)
        for talonario in Talonario.query.all():
            ws_talonarios.append([
                talonario.id,
                talonario.nombre,
                talonario.prefijo,
                talonario.numero_inicio,
                talonario.numero_fin,
                talonario.numero_actual,
                'Sí' if talonario.activo else 'No'
            ])
        
        # Hoja de Facturas
        ws_facturas = wb.create_sheet("Facturas")
        headers = ['ID', 'Número Factura', 'Cliente ID', 'Cliente Nombre', 'Talonario ID', 'Talonario Nombre', 
                  'Fecha Emisión', 'Fecha Vencimiento', 'Fecha Creación', 'Fecha Edición', 
                  'Subtotal', 'IVA', 'Total', 'Estado', 'Notas']
        ws_facturas.append(headers)
        for factura in Factura.query.all():
            ws_facturas.append([
                factura.id,
                factura.numero_factura,
                factura.cliente_id,
                factura.cliente.nombre if factura.cliente else '',
                factura.talonario_id or '',
                factura.talonario.nombre if factura.talonario else '',
                factura.fecha_emision.strftime('%d/%m/%Y') if factura.fecha_emision else '',
                factura.fecha_vencimiento.strftime('%d/%m/%Y') if factura.fecha_vencimiento else '',
                factura.fecha_creacion.strftime('%d/%m/%Y %H:%M:%S') if factura.fecha_creacion else '',
                factura.fecha_edicion.strftime('%d/%m/%Y %H:%M:%S') if factura.fecha_edicion else '',
                factura.subtotal,
                factura.iva,
                factura.total,
                factura.estado,
                factura.notas or ''
            ])
        
        # Hoja de Detalles de Factura
        ws_detalles = wb.create_sheet("DetallesFactura")
        headers = ['ID', 'Factura ID', 'Número Factura', 'Producto ID', 'Producto Código', 'Producto Nombre', 'Cantidad', 'Precio Unitario', 'Subtotal']
        ws_detalles.append(headers)
        for detalle in DetalleFactura.query.all():
            ws_detalles.append([
                detalle.id,
                detalle.factura_id,
                detalle.factura.numero_factura if detalle.factura else '',
                detalle.producto_id,
                detalle.producto.codigo if detalle.producto else '',
                detalle.producto.nombre if detalle.producto else '',
                detalle.cantidad,
                detalle.precio_unitario,
                detalle.subtotal
            ])
        
        # Estilizar encabezados
        for ws in wb.worksheets:
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF")
            for cell in ws[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center")
        
        # Guardar en memoria
        from io import BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'sisfac_datos_export_{fecha}.xlsx'
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        flash('Datos exportados correctamente', 'success')
        return response
    except Exception as e:
        flash(f'Error al exportar datos: {str(e)}', 'error')
        return redirect(url_for('ajustes.index'))


@bp.route('/limpiar-backups', methods=['POST'])
def limpiar_backups():
    """Eliminar backups antiguos (más de 30 días)"""
    try:
        backups_dir = get_backups_dir()
        if not os.path.exists(backups_dir):
            return jsonify({'success': False, 'message': 'Directorio de backups no encontrado'})
        
        fecha_limite = datetime.now() - timedelta(days=30)
        eliminados = 0
        
        for file in os.listdir(backups_dir):
            if file.endswith('.db'):
                file_path = os.path.join(backups_dir, file)
                fecha_modificacion = datetime.fromtimestamp(os.path.getmtime(file_path))
                if fecha_modificacion < fecha_limite:
                    os.remove(file_path)
                    eliminados += 1
        
        flash(f'Se eliminaron {eliminados} backup(s) antiguo(s)', 'success')
        return jsonify({'success': True, 'message': f'Se eliminaron {eliminados} backup(s) antiguo(s)'})
    except Exception as e:
        flash(f'Error al limpiar backups: {str(e)}', 'error')
        return jsonify({'success': False, 'message': str(e)})
