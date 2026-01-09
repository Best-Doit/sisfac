# -*- mode: python ; coding: utf-8 -*-
# Configuración optimizada para AppImage autónomo
# Build reproducible y optimizado para producción

import sys
from PyInstaller.utils.hooks import collect_submodules

# ============================================
# CONFIGURACIÓN OPTIMIZADA PARA --ONEFILE
# ============================================

# Datos a incluir (solo lo esencial)
datas = [
    ('app', 'app'),  # Todo el código de la aplicación
]

# Binarios adicionales (ninguno por ahora)
binaries = []

# Hidden imports - Solo lo esencial (optimizado)
hiddenimports = [
    # Flask core
    'flask',
    'flask.app',
    'flask.helpers',
    'flask.json',
    'flask.wrappers',
    'werkzeug',
    'werkzeug.serving',
    'werkzeug.routing',
    'werkzeug.wrappers',
    'werkzeug.exceptions',
    
    # SQLAlchemy
    'sqlalchemy',
    'sqlalchemy.engine',
    'sqlalchemy.pool',
    'sqlalchemy.sql',
    'sqlalchemy.dialects.sqlite',
    'flask_sqlalchemy',
    
    # Jinja2 (templates)
    'jinja2',
    'jinja2.loaders',
    'jinja2.ext',
    'markupsafe',
    
    # OpenPyXL (Excel)
    'openpyxl',
    'openpyxl.cell',
    'openpyxl.workbook',
    'openpyxl.worksheet',
    'openpyxl.styles',
    'openpyxl.utils',
    'et_xmlfile',
    
    # Utilidades
    'itsdangerous',
    'click',
    'blinker',
    'greenlet',
    'dateutil',
    'dateutil.parser',
    'dateutil.relativedelta',
    
    # Módulos estándar http (requeridos por Werkzeug/Flask)
    'http',
    'http.client',
    'http.server',
]

# Excluir módulos innecesarios para reducir tamaño
excludes = [
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'PIL.tests',
    'tkinter',
    'pydoc',
    'unittest',
    'test',
    'tests',
    'distutils',
    'setuptools',
    'urllib3',
    'certifi',
    'charset_normalizer',
    'idna',
]

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
    optimize=2,  # Optimización nivel 2 (balance tamaño/velocidad)
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# ============================================
# CONFIGURACIÓN EXE --ONEFILE OPTIMIZADA
# ============================================
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='sisfac-backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Stripear símbolos para reducir tamaño
    upx=True,    # Comprimir con UPX si está disponible
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Mantener consola para logs en producción
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Optimizaciones adicionales
    icon=None,  # Sin icono (no necesario para backend)
)
