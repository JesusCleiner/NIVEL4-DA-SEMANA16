from tohally_app import app, db
from sqlalchemy import inspect

with app.app_context():
    # Verifica la URL de la base de datos
    print("URL de la DB:", db.engine.url)
    
    # Usa el inspector para listar tablas
    inspector = inspect(db.engine)
    print("Tablas en la DB:", inspector.get_table_names())
