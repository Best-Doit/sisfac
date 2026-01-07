from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Talonario

bp = Blueprint('talonarios', __name__, url_prefix='/talonarios')

@bp.route('/')
def listar():
    talonarios = Talonario.query.filter_by(activo=True).order_by(Talonario.id.desc()).all()
    return render_template('talonarios/list.html', talonarios=talonarios)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        talonario = Talonario(
            nombre=request.form['nombre'],
            numero_inicio=int(request.form['numero_inicio']),
            numero_fin=int(request.form['numero_fin']),
            prefijo=request.form.get('prefijo', 'FAC')
        )
        db.session.add(talonario)
        db.session.commit()
        flash('Talonario creado correctamente', 'success')
        return redirect(url_for('talonarios.listar'))
    return render_template('talonarios/form.html')

@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    talonario = Talonario.query.get_or_404(id)
    if request.method == 'POST':
        talonario.nombre = request.form['nombre']
        talonario.numero_inicio = int(request.form['numero_inicio'])
        talonario.numero_fin = int(request.form['numero_fin'])
        talonario.prefijo = request.form.get('prefijo', 'FAC')
        db.session.commit()
        flash('Talonario actualizado correctamente', 'success')
        return redirect(url_for('talonarios.listar'))
    return render_template('talonarios/form.html', talonario=talonario)

@bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    talonario = Talonario.query.get_or_404(id)
    talonario.activo = False
    db.session.commit()
    flash('Talonario eliminado correctamente', 'success')
    return redirect(url_for('talonarios.listar'))

