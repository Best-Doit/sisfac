"""
Script para unificar precios: eliminar precio_3 y mantener solo precio_1 y precio_2
"""
import sqlite3
import os

# Ruta a la base de datos
db_path = os.path.join(os.path.dirname(__file__), '..', 'sisfac.db')

if not os.path.exists(db_path):
    print(f"❌ No se encontró la base de datos en {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Verificar si existe la columna precio_3
    cursor.execute("PRAGMA table_info(productos)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'precio_3' in columns:
        print("📝 Eliminando columna precio_3...")
        # SQLite no permite eliminar columnas directamente, necesitamos recrear la tabla
        cursor.execute("""
            CREATE TABLE productos_new (
                id INTEGER PRIMARY KEY,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio_unitario REAL NOT NULL,
                precio_1 REAL,
                precio_2 REAL,
                stock INTEGER DEFAULT 0,
                categoria TEXT,
                fecha_registro TEXT,
                activo INTEGER DEFAULT 1
            )
        """)
        
        cursor.execute("""
            INSERT INTO productos_new 
            (id, codigo, nombre, descripcion, precio_unitario, precio_1, precio_2, stock, categoria, fecha_registro, activo)
            SELECT 
                id, codigo, nombre, descripcion, precio_unitario, precio_1, precio_2, stock, categoria, fecha_registro, activo
            FROM productos
        """)
        
        cursor.execute("DROP TABLE productos")
        cursor.execute("ALTER TABLE productos_new RENAME TO productos")
        
        print("✅ Columna precio_3 eliminada correctamente")
    else:
        print("ℹ️  La columna precio_3 no existe, no es necesario migrar")
    
    conn.commit()
    print("✅ Migración completada exitosamente")
    
except Exception as e:
    conn.rollback()
    print(f"❌ Error durante la migración: {e}")
    raise
finally:
    conn.close()

