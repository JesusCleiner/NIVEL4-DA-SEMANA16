import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt 
import datetime 
import warnings 

# ------------------------
# CARGAR VARIABLES DE ENTORNO
# ------------------------
load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY", "clave_super_secreta_a_cambiar")
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
ADMIN_NAME = os.environ.get('ADMIN_NAME', 'Administrador')

# ------------------------
# INICIALIZAR APP
# ------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY 

# ------------------------
# CONFIGURACIÓN DE BASE DE DATOS
# ------------------------
DB_PATH = Path(__file__).parent / "database" / "tohally.db"
# Crear la carpeta database si no existe
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH.resolve()}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt_app = Bcrypt(app) 

# ------------------------
# CONFIGURACIÓN FLASK-LOGIN
# ------------------------
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'warning'
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."

# ------------------------
# MODELOS (Solo para DB: Usuario y Solicitudes de Alumnos)
# ------------------------
class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False) 
    rol = db.Column(db.String(20), nullable=False, default="admin")

class Alumno(db.Model):
    __tablename__ = "alumnos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, default=0) 
    categoria = db.Column(db.String(50), default='N/A') 
    contacto = db.Column(db.Text, nullable=False) 
    tipo_solicitud = db.Column(db.String(50), default='Pre-Inscripción')
    fecha_solicitud = db.Column(db.DateTime, default=db.func.current_timestamp())

# ------------------------
# FUNCIONES LOGIN
# ------------------------
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ------------------------
# RUTAS DE AUTENTICACIÓN
# ------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # Redirigir a HOME si ya está autenticado
        return redirect(url_for('home'))

    if request.method == "POST":
        correo = request.form.get("correo")
        contraseña = request.form.get("contraseña")
        user = Usuario.query.filter_by(correo=correo).first()

        # Validación con Bcrypt
        if user and bcrypt_app.check_password_hash(user.contraseña, contraseña):
            login_user(user)
            flash(f"Bienvenido, {user.nombre}", "success")
            
            # 🛑 REDIRECCIÓN CORREGIDA: Siempre a home si no hay 'next'
            next_page = request.args.get('next')
            return redirect(next_page or url_for("home"))
            
        else:
            flash("Credenciales incorrectas", "danger")
            
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("home")) 

# ------------------------
# RUTAS PÚBLICAS
# ------------------------
@app.route("/")
def home():
    """Página de inicio con noticias destacadas (datos simulados)."""
    # Usamos datos simulados para las noticias
    noticias_recientes = [
        {
            'titulo': '¡Goleada Histórica en el Torneo Regional!',
            'contenido': 'Nuestra categoría sub-15 demostró un dominio absoluto en la final. ¡Campeones!',
            'imagen': 'noticia1.jpg', 
            'fecha': '28/SEP'
        },
        {
            'titulo': 'Taller de Nutrición y Rendimiento Físico',
            'contenido': 'El Dr. Méndez impartió una charla clave sobre la dieta del futbolista de alto nivel.',
            'imagen': 'noticia2.jpg',
            'fecha': '20/SEP'
        },
        {
            'titulo': 'Entrenador Gutiérrez Viaja a Seminario UEFA',
            'contenido': 'Actualizando metodologías. El staff se mantiene a la vanguardia.',
            'imagen': 'noticia3.jpg',
            'fecha': '15/SEP'
        }
    ]
    return render_template("index.html", noticias=noticias_recientes)

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/servicios")
def servicios():
    return render_template("servicios.html")

@app.route("/noticias")
def noticias():
    """Página de noticias completa (datos simulados)."""
    # Usamos datos simulados para todas las noticias
    todas_las_noticias = [
        {
            'titulo': '¡Goleada Histórica en el Torneo Regional!',
            'contenido': 'Nuestra categoría sub-15 demostró un dominio absoluto en la final. El esfuerzo y la disciplina dieron frutos. Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            'imagen': 'noticia1.jpg', 
            'fecha': '28 de Septiembre, 2025'
        },
        {
            'titulo': 'Taller de Nutrición y Rendimiento Físico',
            'contenido': 'El Dr. Méndez impartió una charla clave sobre la dieta del futbolista de alto nivel. Se cubrieron hidratación, suplementos esenciales y planificación de comidas.',
            'imagen': 'noticia2.jpg',
            'fecha': '20 de Septiembre, 2025'
        },
        {
            'titulo': 'Entrenador Gutiérrez Viaja a Seminario UEFA',
            'contenido': 'Actualizando metodologías. El staff se mantiene a la vanguardia con las últimas técnicas de formación y entrenamiento de élite en Europa.',
            'imagen': 'noticia3.jpg',
            'fecha': '15 de Septiembre, 2025'
        },
        {
            'titulo': 'Próximo Partido Amistoso: TOHALLY vs. Academia XYZ',
            'contenido': 'Invitamos a todos los padres a asistir al encuentro amistoso de este sábado a las 10:00 am. ¡Apoyemos a nuestros jóvenes talentos!',
            'imagen': 'noticia4.jpg',
            'fecha': '10 de Septiembre, 2025'
        }
    ]
    return render_template("noticias.html", noticias=todas_las_noticias)

@app.route("/galeria") 
def galeria():
    return render_template("galeria.html")


@app.route("/contacto", methods=["GET", "POST"]) 
def contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        contacto_info = request.form.get('contacto')
        
        if 'edad' in request.form:
            # Es una Pre-Inscripción
            try:
                edad = int(request.form.get('edad'))
            except (ValueError, TypeError):
                edad = 0
            
            categoria = request.form.get('categoria', 'N/A')
            tipo = 'Pre-Inscripción'
            
        else:
            # Es una Consulta/Sugerencia
            email = request.form.get('email', 'N/A')
            mensaje = request.form.get('mensaje', 'Sin mensaje')
            
            contacto_info = f"Email: {email}. Mensaje: {mensaje}"
            edad = 0
            categoria = "Consulta"
            tipo = 'Sugerencia/Consulta'

        nueva_solicitud = Alumno(
            nombre=nombre,
            edad=edad,
            categoria=categoria,
            contacto=contacto_info,
            tipo_solicitud=tipo
        )
        
        try:
            db.session.add(nueva_solicitud)
            db.session.commit()
            flash('¡Tu solicitud ha sido enviada con éxito! Nos pondremos en contacto pronto.', 'success')
            return redirect(url_for('contacto'))
        except Exception as e:
            db.session.rollback()
            flash('Ocurrió un error al procesar tu solicitud. Intenta de nuevo.', 'danger')
            # print(f"Error al guardar solicitud: {e}") 
            
    return render_template("contacto.html")


# ------------------------
# RUTAS PRIVADAS (ADMIN) - CON LOGICA CRUD INTEGRADA
# ------------------------
# 🛑 Eliminada ruta /dashboard

# 🏆 RUTA DE GESTIÓN DE ALUMNOS (ANTERIORMENTE /alumnos y /movimiento)
@app.route("/movimiento")
@login_required # 🔒 PROTEGIDA
def movimiento():
    """Listado de todos los alumnos/registros para gestión (READ)."""
    # Listado completo de alumnos y sugerencias ordenados alfabéticamente
    todos_los_alumnos = Alumno.query.order_by(Alumno.nombre.asc()).all()
    # Ahora esta página actúa como el panel de gestión
    return render_template("movimiento.html", alumnos=todos_los_alumnos)


# 🏆 RUTA ÚNICA PARA CREAR Y EDITAR ALUMNO (CREATE/UPDATE)
# Se usa para el botón "Inscribir Alumno" (Creación) y para los botones "Editar"
@app.route("/inscribir", methods=["GET", "POST"], defaults={'alumno_id': None})
@app.route("/inscribir/<int:alumno_id>", methods=["GET", "POST"])
@login_required 
def inscribir_estudiante(alumno_id): 
    """Maneja la lógica para crear un nuevo alumno o editar uno existente."""
    alumno = None
    
    # Si hay un ID, estamos EDITANDO un registro existente
    if alumno_id:
        alumno = Alumno.query.get_or_404(alumno_id)
        
    if request.method == "POST":
        
        # 1. Recoger datos del formulario
        nombre_completo = f"{request.form.get('nombre')} {request.form.get('apellido')}"
        fecha_nac_str = request.form.get("fecha_nacimiento")
        contacto_padre = request.form.get("contacto_padre")
        categoria = request.form.get("categoria")
        
        # 2. Cálculo de la edad
        edad_calculada = 0
        try:
            fecha_nac = datetime.datetime.strptime(fecha_nac_str, '%Y-%m-%d').date()
            hoy = datetime.date.today()
            edad_calculada = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
        except (ValueError, TypeError):
            # Si hay un error, se usa la edad existente si es edición, o 0 si es nuevo
            edad_calculada = alumno.edad if alumno else 0 
            flash("Error en el formato de la Fecha de Nacimiento. Se usará la edad existente o 0.", "warning")

        # 3. Crear o Actualizar el registro
        if alumno is None:
            # Es un nuevo registro (CREATE)
            alumno = Alumno(
                nombre=nombre_completo,
                edad=edad_calculada,
                categoria=categoria,
                contacto=contacto_padre,
                tipo_solicitud='Inscrito por Admin'
            )
            db.session.add(alumno)
            mensaje = f"Estudiante '{nombre_completo}' registrado exitosamente."
        else:
            # Es una EDICIÓN (UPDATE)
            alumno.nombre = nombre_completo
            alumno.edad = edad_calculada
            alumno.categoria = categoria
            alumno.contacto = contacto_padre
            # Si se está editando una Pre-Inscripción, la marcamos como Inscrito por Admin
            if alumno.tipo_solicitud in ['Pre-Inscripción', 'Sugerencia/Consulta']:
                alumno.tipo_solicitud = 'Inscrito por Admin'
                
            mensaje = f"Estudiante '{nombre_completo}' actualizado exitosamente."

        try:
            db.session.commit()
            flash(mensaje, "success")
            # 🛑 Redirige a la página de gestión /movimiento
            return redirect(url_for("movimiento")) 
        except Exception as e:
            db.session.rollback()
            flash(f"Ocurrió un error al guardar en la base de datos: {e}", "danger")
            # Redirigir al mismo formulario para corregir
            return redirect(url_for("inscribir_estudiante", alumno_id=alumno_id))
            
    # Mostrar el formulario GET (RENDER)
    # Pasa el objeto alumno si existe (para edición) o None (para nuevo)
    return render_template("inscripciones.html", alumno=alumno)


# 4. RUTA PARA ELIMINAR ALUMNO (DELETE)
@app.route("/eliminar_alumno/<int:alumno_id>", methods=["POST"])
@login_required
def eliminar_alumno(alumno_id):
    """Elimina permanentemente un registro de alumno."""
    alumno = Alumno.query.get_or_404(alumno_id)
    
    try:
        db.session.delete(alumno)
        db.session.commit()
        flash(f"El registro de '{alumno.nombre}' ha sido eliminado.", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"Ocurrió un error al eliminar el registro: {e}", "danger")
    # 🛑 Redirige a la página de gestión /movimiento
    return redirect(url_for("movimiento"))


# ------------------------
# INICIALIZAR TABLAS Y ADMIN
# ------------------------

def init_db_and_admin():
    """Crea la base de datos y un usuario administrador inicial si no existe."""
    with app.app_context():
        # Crear todas las tablas (Ahora solo Usuarios y Alumnos)
        db.create_all()

        # Crear usuario administrador si no existe
        if ADMIN_EMAIL and ADMIN_PASSWORD:
            if not Usuario.query.filter_by(correo=ADMIN_EMAIL).first():
                try:
                    hashed_password = bcrypt_app.generate_password_hash(ADMIN_PASSWORD).decode('utf-8')
                    admin_user = Usuario(
                        nombre=ADMIN_NAME,
                        correo=ADMIN_EMAIL,
                        contraseña=hashed_password,
                        rol='admin'
                    )
                    db.session.add(admin_user)
                    db.session.commit()
                    print(f"\n*** ADMINISTRADOR CREADO: {ADMIN_EMAIL} ***\n")
                except Exception as e:
                    db.session.rollback()
                    print(f"ERROR: No se pudo crear el usuario administrador: {e}")
            else:
                print(f"ADVERTENCIA: Usuario administrador ({ADMIN_EMAIL}) ya existe.")
        else:
            print("ADVERTENCIA: Las variables ADMIN_EMAIL o ADMIN_PASSWORD no están en el archivo .env")

# ------------------------
# RUN
# ------------------------
if __name__ == "__main__":
    init_db_and_admin()
    app.run(debug=True)