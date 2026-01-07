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

REM Verificar que Python esté instalado (múltiples métodos de detección)
SET PYTHON_CMD=
SET PYTHON_FOUND=0

echo Buscando Python instalado...
echo.

REM Método 1: python directo
python --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=python
    SET PYTHON_FOUND=1
    echo   [OK] Python encontrado con: python
    GOTO :PYTHON_FOUND
)

REM Método 2: py launcher (múltiples variantes)
py --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=py
    SET PYTHON_FOUND=1
    echo   [OK] Python encontrado con: py
    GOTO :PYTHON_FOUND
)

py -3 --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=py -3
    SET PYTHON_FOUND=1
    echo   [OK] Python encontrado con: py -3
    GOTO :PYTHON_FOUND
)

py -3.12 --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=py -3.12
    SET PYTHON_FOUND=1
    echo   [OK] Python encontrado con: py -3.12
    GOTO :PYTHON_FOUND
)

py -3.11 --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=py -3.11
    SET PYTHON_FOUND=1
    echo   [OK] Python encontrado con: py -3.11
    GOTO :PYTHON_FOUND
)

py -3.10 --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=py -3.10
    SET PYTHON_FOUND=1
    echo   [OK] Python encontrado con: py -3.10
    GOTO :PYTHON_FOUND
)

py -3.9 --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=py -3.9
    SET PYTHON_FOUND=1
    echo   [OK] Python encontrado con: py -3.9
    GOTO :PYTHON_FOUND
)

REM Método 3: Buscar en ubicaciones comunes
IF EXIST "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: %LOCALAPPDATA%\Programs\Python\Python312\
        GOTO :PYTHON_FOUND
    )
)

IF EXIST "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: %LOCALAPPDATA%\Programs\Python\Python311\
        GOTO :PYTHON_FOUND
    )
)

IF EXIST "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: %LOCALAPPDATA%\Programs\Python\Python310\
        GOTO :PYTHON_FOUND
    )
)

IF EXIST "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: %LOCALAPPDATA%\Programs\Python\Python39\
        GOTO :PYTHON_FOUND
    )
)

IF EXIST "%ProgramFiles%\Python312\python.exe" (
    "%ProgramFiles%\Python312\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%ProgramFiles%\Python312\python.exe"
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: %ProgramFiles%\Python312\
        GOTO :PYTHON_FOUND
    )
)

IF EXIST "%ProgramFiles%\Python311\python.exe" (
    "%ProgramFiles%\Python311\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%ProgramFiles%\Python311\python.exe"
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: %ProgramFiles%\Python311\
        GOTO :PYTHON_FOUND
    )
)

IF EXIST "%ProgramFiles%\Python310\python.exe" (
    "%ProgramFiles%\Python310\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%ProgramFiles%\Python310\python.exe"
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: %ProgramFiles%\Python310\
        GOTO :PYTHON_FOUND
    )
)

IF EXIST "%ProgramFiles%\Python39\python.exe" (
    "%ProgramFiles%\Python39\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%ProgramFiles%\Python39\python.exe"
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: %ProgramFiles%\Python39\
        GOTO :PYTHON_FOUND
    )
)

IF EXIST "C:\Python312\python.exe" (
    "C:\Python312\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="C:\Python312\python.exe"
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: C:\Python312\
        GOTO :PYTHON_FOUND
    )
)

IF EXIST "C:\Python311\python.exe" (
    "C:\Python311\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="C:\Python311\python.exe"
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: C:\Python311\
        GOTO :PYTHON_FOUND
    )
)

IF EXIST "C:\Python310\python.exe" (
    "C:\Python310\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="C:\Python310\python.exe"
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: C:\Python310\
        GOTO :PYTHON_FOUND
    )
)

IF EXIST "C:\Python39\python.exe" (
    "C:\Python39\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="C:\Python39\python.exe"
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: C:\Python39\
        GOTO :PYTHON_FOUND
    )
)

REM Método 4: Buscar en el registro de Windows (si está disponible)
FOR /F "tokens=2*" %%A IN ('reg query "HKLM\SOFTWARE\Python\PythonCore" /s /v ExecutablePath 2^>nul ^| findstr /i "ExecutablePath"') DO (
    IF EXIST "%%B" (
        "%%B" --version >nul 2>&1
        IF NOT ERRORLEVEL 1 (
            SET PYTHON_CMD="%%B"
            SET PYTHON_FOUND=1
            echo   [OK] Python encontrado en registro: %%B
            GOTO :PYTHON_FOUND
        )
    )
)

REM Si no se encontró Python
IF %PYTHON_FOUND%==0 (
    echo.
    echo ========================================
    echo   ERROR: Python NO ENCONTRADO
    echo ========================================
    echo.
    echo Python no esta instalado o no esta en el PATH del sistema.
    echo.
    echo SOLUCIONES:
    echo.
    echo 1. INSTALAR PYTHON:
    echo    - Visita: https://www.python.org/downloads/
    echo    - Descarga Python 3.9 o superior
    echo    - IMPORTANTE: Durante la instalacion, marca la opcion:
    echo      "Add Python to PATH" o "Agregar Python al PATH"
    echo    - Reinicia la terminal despues de instalar
    echo.
    echo 2. VERIFICAR INSTALACION:
    echo    Abre una nueva terminal y ejecuta:
    echo      python --version
    echo    O intenta:
    echo      py --version
    echo.
    echo 3. AGREGAR AL PATH MANUALMENTE:
    echo    Si Python esta instalado pero no funciona:
    echo    - Busca donde esta instalado (normalmente):
    echo      C:\Users\%USERNAME%\AppData\Local\Programs\Python\
    echo    - O: C:\Python3X\
    echo    - Agrega esa ruta al PATH del sistema
    echo.
    echo 4. REINICIAR TERMINAL:
    echo    Despues de instalar Python, CIERRA y ABRE una nueva terminal
    echo    antes de ejecutar este script nuevamente.
    echo.
    EXIT /B 1
)

:PYTHON_FOUND

echo.
echo [0/3] Verificando Python...
%PYTHON_CMD% --version
IF ERRORLEVEL 1 (
    echo ERROR: No se pudo verificar la version de Python.
    echo El comando usado fue: %PYTHON_CMD%
    EXIT /B 1
)

echo   Verificando pip...
%PYTHON_CMD% -m pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo   ADVERTENCIA: pip no disponible. Intentando instalar pip...
    %PYTHON_CMD% -m ensurepip --default-pip
    IF ERRORLEVEL 1 (
        echo ERROR: pip no disponible y no se pudo instalar.
        echo Verifica la instalacion de Python.
        EXIT /B 1
    )
)
echo   Python y pip verificados correctamente.
echo.

SET ROOT_DIR=%~dp0..
PUSHD "%ROOT_DIR%"

IF NOT EXIST "venv" (
    echo [1/3] Creando entorno virtual (venv)...
    %PYTHON_CMD% -m venv venv
    IF ERRORLEVEL 1 (
        echo   ERROR: No se pudo crear el entorno virtual.
        echo   Intenta manualmente: %PYTHON_CMD% -m venv venv
        EXIT /B 1
    )
    echo   Entorno virtual creado correctamente.
) ELSE (
    echo [1/3] Entorno virtual 'venv' ya existe. Verificando...
)

REM Verificar que el venv existe antes de activarlo
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo   ERROR: El directorio venv existe pero no tiene Scripts\activate.bat
    echo   Elimina el directorio venv y ejecuta este script nuevamente.
    EXIT /B 1
)

echo [2/3] Activando entorno virtual...
CALL venv\Scripts\activate.bat
IF ERRORLEVEL 1 (
    echo   ERROR: No se pudo activar el entorno virtual.
    echo   Verifica que venv\Scripts\activate.bat existe.
    EXIT /B 1
)

REM Usar python del venv activado
SET PYTHON_VENV=python
SET PIP_VENV=python -m pip

echo [3/3] Instalando dependencias desde requirements.txt...
echo   Actualizando pip...
%PIP_VENV% install --upgrade pip --quiet
IF ERRORLEVEL 1 (
    echo   ERROR: No se pudo actualizar pip.
    EXIT /B 1
)

IF NOT EXIST "requirements.txt" (
    echo   ERROR: No se encontro requirements.txt en el directorio raiz.
    EXIT /B 1
)

echo   Instalando dependencias (esto puede tardar unos minutos)...
%PIP_VENV% install -r requirements.txt
IF ERRORLEVEL 1 (
    echo   ERROR: Fallo la instalacion de dependencias.
    echo   Intenta manualmente: %PIP_VENV% install -r requirements.txt
    EXIT /B 1
)

echo   Verificando instalacion...
%PYTHON_VENV% -c "import flask; import sqlalchemy; import flask_sqlalchemy; import openpyxl; import reportlab; import dateutil; import PyInstaller" 2>NUL
IF ERRORLEVEL 1 (
    echo   ADVERTENCIA: Algunas dependencias pueden no estar instaladas correctamente.
    echo   Reintentando instalacion...
    %PIP_VENV% install -r requirements.txt --force-reinstall --no-cache-dir
    IF ERRORLEVEL 1 (
        echo   ERROR: Fallo la reinstalacion de dependencias.
        EXIT /B 1
    )
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

