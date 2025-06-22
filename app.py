from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

from models import db
from models.usuario import Usuario
from models.producto import Producto
from forms import LoginForm, RegistroForm, ProductoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'j4rd1nes.23'  # Cambia esto por una clave segura
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'compras.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(usuario=form.usuario.data).first()
        if user and user.estado and check_password_hash(user.clave, form.clave.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuario o clave incorrectos, o usuario inactivo.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        # Verifica si el usuario o correo ya existen
        existe_usuario = Usuario.query.filter_by(usuario=form.usuario.data).first()
        existe_correo = Usuario.query.filter_by(correo=form.correo.data).first()
        if existe_usuario:
            flash('El nombre de usuario ya está registrado. Elige otro.')
            return render_template('registro.html', form=form)
        if existe_correo:
            flash('El correo ya está registrado. Usa otro correo.')
            return render_template('registro.html', form=form)
        hashed_password = generate_password_hash(form.clave.data)
        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            correo=form.correo.data,
            usuario=form.usuario.data,
            clave=hashed_password,
            estado=True,
            es_admin=False  # <--- Importante: los usuarios registrados no son admin
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario registrado correctamente.')
        return redirect(url_for('login'))
    return render_template('registro.html', form=form)

@app.route('/admin/usuarios')
@login_required
def admin_usuarios():
    if not current_user.es_admin:
        flash('No tienes permisos para acceder a esta página.')
        return redirect(url_for('index'))
    usuarios = Usuario.query.all()
    return render_template('admin_usuarios.html', usuarios=usuarios)

@app.route('/admin/usuario/<int:usuario_id>/cambiar_estado', methods=['POST'])
@login_required
def cambiar_estado_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    # Evita que el usuario actual se desactive a sí mismo (opcional)
    if usuario.id == current_user.id:
        flash('No puedes cambiar tu propio estado.')
        return redirect(url_for('admin_usuarios'))
    usuario.estado = not usuario.estado
    db.session.commit()
    flash('Estado del usuario actualizado.')
    return redirect(url_for('admin_usuarios'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/productos')
@login_required
def lista_productos():
    # Aquí deberías obtener los productos de la base de datos
    productos = Producto.query.all()
    return render_template('lista_productos.html', productos=productos)

@app.route('/productos/agregar', methods=['GET', 'POST'])
@login_required
def agregar_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        producto = Producto(
            nombre=form.nombre.data,
            cantidad=form.cantidad.data,
            medida=form.medida.data,
            comprado=form.comprado.data
        )
        db.session.add(producto)
        db.session.commit()
        flash('Producto agregado correctamente.')
        return redirect(url_for('lista_productos'))
    return render_template('agregar_producto.html', form=form)

@app.route('/productos/editar/<int:producto_id>', methods=['GET', 'POST'])
@login_required
def editar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    form = ProductoForm(obj=producto)
    if form.validate_on_submit():
        producto.nombre = form.nombre.data
        producto.cantidad = form.cantidad.data
        producto.medida = form.medida.data
        producto.comprado = form.comprado.data
        db.session.commit()
        flash('Producto actualizado correctamente.')
        return redirect(url_for('lista_productos'))
    return render_template('editar_producto.html', form=form, producto=producto)

@app.route('/productos/eliminar/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado correctamente.')
    return redirect(url_for('lista_productos'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Crear usuario admin solo si no existe
        if not Usuario.query.filter_by(usuario='admin').first():
            admin = Usuario(
                nombre='Administrador',
                correo='admin@correo.com',
                usuario='admin',
                clave=generate_password_hash('admin123'),
                estado=True,
                es_admin=True
            )
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)