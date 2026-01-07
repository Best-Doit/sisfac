@echo off
REM Script para preparar el entorno Python en Windows
REM - Crea un venv
REM - Instala dependencias de requirements.txt (incluye PyInstaller)

SETLOCAL ENABLEDELAYEDEXPANSION

echo.
echo ================================
echo   Preparar entorno SISFAC (Win)
echo ================================
echo.

SET ROOT_DIR=%~dp0..
PUSHD "%ROOT_DIR%"

IF NOT EXIST "venv" (
    echo [1/2] Creando entorno virtual (venv)...
    python -m venv venv
    IF ERRORLEVEL 1 (
        echo   ERROR: No se pudo crear el entorno virtual.
        EXIT /B 1
    )
) ELSE (
    echo [1/2] Entorno virtual 'venv' ya existe.
)

echo [2/2] Instalando dependencias desde requirements.txt...
CALL venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

IF ERRORLEVEL 1 (
    echo   ERROR: Fallo la instalacion de dependencias.
    EXIT /B 1
)

echo.
echo Entorno listo. Para usarlo:
echo   venv\Scripts\activate

POPD
ENDLOCAL

