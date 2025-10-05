from tohally_app import app, db, Usuario
from dotenv import load_dotenv
import os
import bcrypt

# Cargar variables del .env
load_dotenv()

ADMIN_CORREO = os.getenv("ADMIN_CORREO")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_NOMBRE = os.getenv("ADMIN_NOMBRE", "Administrador")

# 🔹 Usar contexto de la app
with app.app_context():
    # Verificar si ya existe
    existing = Usuario.query.filter_by(correo=ADMIN_CORREO).first()
    
    if existing:
        print("El usuario administrador ya existe.")
    else:
        # Crear nuevo usuario admin
        hashed_password = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt())
        admin_user = Usuario(
            nombre=ADMIN_NOMBRE,
            correo=ADMIN_CORREO,
            contraseña=hashed_password.decode('utf-8'),
            rol="admin"
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Usuario administrador creado correctamente.")
