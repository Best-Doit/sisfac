#!/usr/bin/env python3
"""
Script de migración para agregar nuevas columnas a la base de datos existente
"""
import sqlite3
import os
import sys

# Agregar el directorio backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

def migrate_database():
    # Ruta a la base de datos
    db_path = os.path.join(os.path.dirname(__file__), '..', 'sisfac.db')
    
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada. Se creará automáticamente al iniciar la aplicación.")
        return
    
    print(f"📦 Migrando base de datos: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar y agregar columnas a la tabla facturas
        cursor.execute("PRAGMA table_info(facturas)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'talonario_id' not in columns:
            print("  ➕ Agregando columna talonario_id a facturas...")
            cursor.execute("ALTER TABLE facturas ADD COLUMN talonario_id INTEGER")
            print("  ✅ Columna talonario_id agregada")
        else:
            print("  ✓ Columna talonario_id ya existe")
        
        if 'fecha_edicion' not in columns:
            print("  ➕ Agregando columna fecha_edicion a facturas...")
            cursor.execute("ALTER TABLE facturas ADD COLUMN fecha_edicion TEXT")
            print("  ✅ Columna fecha_edicion agregada")
        else:
            print("  ✓ Columna fecha_edicion ya existe")
        
        # Crear tabla talonarios si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS talonarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                numero_inicio INTEGER NOT NULL,
                numero_fin INTEGER NOT NULL,
                prefijo TEXT DEFAULT 'FAC',
                activo INTEGER DEFAULT 1,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("  ✅ Tabla talonarios verificada/creada")
        
        conn.commit()
        print("\n✅ Migración completada exitosamente!")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error durante la migración: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()

