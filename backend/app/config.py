"""
Configuración y utilidades de rutas del sistema
"""
import os
import sys
import shutil
import stat


def _get_home_dir():
    """Return a best-effort home dir for the current user."""
    home_dir = os.path.expanduser('~')
    if not home_dir or home_dir == '~':
        home_dir = os.environ.get('USERPROFILE') or os.environ.get('HOMEPATH') or os.getcwd()
    return home_dir


def _ensure_writable(path):
    """Best-effort: ensure a file is writable (avoid read-only DB copies)."""
    try:
        if os.path.exists(path):
            current_mode = os.stat(path).st_mode
            os.chmod(path, current_mode | stat.S_IWRITE)
    except Exception as e:
        print(f"Warning: no se pudo ajustar permisos de escritura en {path}: {e}")


def get_app_data_dir():
    """Get a writable app data directory."""
    try:
        if getattr(sys, 'frozen', False):
            home_dir = _get_home_dir()
            app_data_dir = os.path.join(home_dir, '.sisfac')
        else:
            basedir = os.path.abspath(os.path.dirname(__file__))
            app_data_dir = os.path.abspath(os.path.join(basedir, "..", ".."))

        os.makedirs(app_data_dir, exist_ok=True)
        return app_data_dir
    except Exception as e:
        print(f"Error in get_app_data_dir: {e}")
        fallback_dir = os.path.join(os.getcwd(), '.sisfac')
        os.makedirs(fallback_dir, exist_ok=True)
        return fallback_dir


def get_database_path():
    """Obtiene la ruta de la base de datos, considerando si está empaquetado o no"""
    # Si está empaquetado con PyInstaller
    if getattr(sys, 'frozen', False):
        # Cuando está empaquetado y ejecutado desde Electron:
        # - Los recursos están en un sistema de archivos de solo lectura (AppImage)
        # - Necesitamos usar un directorio escribible en el home del usuario
        
        # Usar el directorio home del usuario para guardar la base de datos
        app_data_dir = get_app_data_dir()
        db_path = os.path.join(app_data_dir, 'sisfac.db')
        
        # IMPORTANTE: Los datos de producción están en ~/.sisfac/ y NO se tocan
        # Si existe una base de datos en los recursos del AppImage (solo lectura), 
        # copiarla al directorio escribible SOLO si no existe ya una base de datos en ~/.sisfac/
        # Esto permite incluir datos iniciales en el AppImage sin afectar datos de producción
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
        
        # Solo copiar si NO existe ya una base de datos en producción
        # Esto garantiza que los datos de producción nunca se sobrescriban
        if resources_db and os.path.exists(resources_db) and not os.path.exists(db_path):
            try:
                shutil.copyfile(resources_db, db_path)
                _ensure_writable(db_path)
                print(f"📋 Base de datos inicial copiada desde recursos a: {db_path}")
                print(f"   ℹ️  Esta es la primera ejecución. Los datos futuros estarán en: {db_path}")
            except Exception as e:
                print(f"⚠️ No se pudo copiar la base de datos desde recursos: {e}")
        elif os.path.exists(db_path):
            # Base de datos de producción ya existe, asegurar que sea escribible
            _ensure_writable(db_path)
    else:
        # Modo desarrollo: usar ruta relativa al proyecto
        basedir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(basedir, "..", "..", "sisfac.db")
        db_path = os.path.abspath(db_path)
    
    return db_path


def get_backups_dir():
    """Obtiene o crea el directorio de backups"""
    try:
        # Si está empaquetado con PyInstaller
        if getattr(sys, 'frozen', False):
            # Cuando está empaquetado y ejecutado desde Electron:
            # - Los recursos están en un sistema de archivos de solo lectura (AppImage)
            # - Necesitamos usar un directorio escribible en el home del usuario
            
            # Usar el directorio home del usuario para guardar los backups
            app_data_dir = get_app_data_dir()
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


def get_uploads_dir():
    """Obtiene o crea el directorio de uploads"""
    try:
        if getattr(sys, 'frozen', False):
            app_data_dir = get_app_data_dir()
            uploads_dir = os.path.join(app_data_dir, 'uploads')
        else:
            basedir = os.path.abspath(os.path.dirname(__file__))
            uploads_dir = os.path.join(basedir, "..", "..", "uploads")
            uploads_dir = os.path.abspath(uploads_dir)

        os.makedirs(uploads_dir, exist_ok=True)
        return uploads_dir
    except Exception as e:
        print(f"Error in get_uploads_dir: {e}")
        uploads_dir = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        return uploads_dir
