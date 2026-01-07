@echo off
REM Script para preparar el entorno Python en Windows
REM - Verifica Python y pip
REM - Crea un venv
REM - Instala dependencias de requirements.txt (incluye PyInstaller)

SETLOCAL ENABLEDELAYEDEXPANSION

echo.
echo ================================
echo   Preparar entorno SISFAC (Win)
echo ================================
echo.

REM Verificar que Python esté instalado
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ERROR: Python no encontrado. Verifica que Python este instalado.
    echo Intenta con: py --version o py -3.12 --version
    EXIT /B 1
)

echo [0/3] Verificando Python...
python --version
python -m pip --version
IF ERRORLEVEL 1 (
    echo ERROR: pip no disponible. Verifica la instalacion de Python.
    EXIT /B 1
)
echo.

SET ROOT_DIR=%~dp0..
PUSHD "%ROOT_DIR%"

IF NOT EXIST "venv" (
    echo [1/3] Creando entorno virtual (venv)...
    python -m venv venv
    IF ERRORLEVEL 1 (
        echo   ERROR: No se pudo crear el entorno virtual.
        echo   Intenta manualmente: python -m venv venv
        EXIT /B 1
    )
) ELSE (
    echo [1/3] Entorno virtual 'venv' ya existe.
)

echo [2/3] Activando entorno virtual...
CALL venv\Scripts\activate.bat
IF ERRORLEVEL 1 (
    echo   ERROR: No se pudo activar el entorno virtual.
    EXIT /B 1
)

echo [3/3] Instalando dependencias desde requirements.txt...
python -m pip install --upgrade pip
IF ERRORLEVEL 1 (
    echo   ERROR: No se pudo actualizar pip.
    EXIT /B 1
)

python -m pip install -r requirements.txt
IF ERRORLEVEL 1 (
    echo   ERROR: Fallo la instalacion de dependencias.
    echo   Intenta manualmente: python -m pip install -r requirements.txt
    EXIT /B 1
)

echo.
echo ================================
echo   Entorno listo correctamente!
echo ================================
echo.
echo Para usar el entorno:
echo   venv\Scripts\activate
echo   cd backend
echo   python run.py
echo.

POPD
ENDLOCAL

