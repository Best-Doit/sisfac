#!/usr/bin/env python3
"""
Script de migración para agregar columnas de precios múltiples
"""
import sqlite3
import os
import sys

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
        # Verificar y agregar columnas a la tabla productos
        cursor.execute("PRAGMA table_info(productos)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'precio_1' not in columns:
            print("  ➕ Agregando columna precio_1 a productos...")
            cursor.execute("ALTER TABLE productos ADD COLUMN precio_1 REAL")
            print("  ✅ Columna precio_1 agregada")
        else:
            print("  ✓ Columna precio_1 ya existe")
        
        if 'precio_2' not in columns:
            print("  ➕ Agregando columna precio_2 a productos...")
            cursor.execute("ALTER TABLE productos ADD COLUMN precio_2 REAL")
            print("  ✅ Columna precio_2 agregada")
        else:
            print("  ✓ Columna precio_2 ya existe")
        
        if 'precio_3' not in columns:
            print("  ➕ Agregando columna precio_3 a productos...")
            cursor.execute("ALTER TABLE productos ADD COLUMN precio_3 REAL")
            print("  ✅ Columna precio_3 agregada")
        else:
            print("  ✓ Columna precio_3 ya existe")
        
        conn.commit()
        print("\n✅ Migración de precios completada exitosamente!")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error durante la migración: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()

