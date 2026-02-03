from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Talonario

bp = Blueprint('talonarios', __name__, url_prefix='/talonarios')

def _is_xhr():
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

@bp.route('/')
def listar():
    talonarios = Talonario.query.filter_by(activo=True).order_by(Talonario.id.desc()).all()
    return render_template('talonarios/list.html', talonarios=talonarios)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        try:
            numero_inicio = int(request.form['numero_inicio'])
            talonario = Talonario(
                nombre=request.form['nombre'].strip(),
                numero_inicio=numero_inicio,
                numero_fin=int(request.form['numero_fin']),
                prefijo=request.form.get('prefijo', 'FAC').strip(),
                numero_actual=numero_inicio
            )
            db.session.add(talonario)
            db.session.commit()
            if _is_xhr():
                return jsonify({'success': True, 'message': 'Talonario creado correctamente'})
            flash('Talonario creado correctamente', 'success')
            return redirect(url_for('talonarios.listar'))
        except Exception as e:
            if _is_xhr():
                return jsonify({'success': False, 'message': str(e)}), 400
            raise
    return render_template('talonarios/form.html')

@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    talonario = Talonario.query.get_or_404(id)
    if request.method == 'POST':
        try:
            talonario.nombre = request.form['nombre'].strip()
            talonario.numero_inicio = int(request.form['numero_inicio'])
            talonario.numero_fin = int(request.form['numero_fin'])
            talonario.prefijo = request.form.get('prefijo', 'FAC').strip()
            db.session.commit()
            if _is_xhr():
                return jsonify({'success': True, 'message': 'Talonario actualizado correctamente'})
            flash('Talonario actualizado correctamente', 'success')
            return redirect(url_for('talonarios.listar'))
        except Exception as e:
            if _is_xhr():
                return jsonify({'success': False, 'message': str(e)}), 400
            raise
    return render_template('talonarios/form.html', talonario=talonario)

@bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    talonario = Talonario.query.get_or_404(id)
    talonario.activo = False
    db.session.commit()
    flash('Talonario eliminado correctamente', 'success')
    return redirect(url_for('talonarios.listar'))
