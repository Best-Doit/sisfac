@echo off
REM Script para empaquetar SISFAC completo en Windows
REM Incluye: Backend (PyInstaller) + Frontend (Electron, instalador NSIS)

SETLOCAL ENABLEDELAYEDEXPANSION

echo.
echo ================================
echo   Empaquetar SISFAC - Windows
echo ================================
echo.

REM Detectar ruta del proyecto (directorio de este script)
SET SCRIPT_DIR=%~dp0
PUSHD "%SCRIPT_DIR%\.."

REM Paso 1: Backend con PyInstaller
echo [1/2] Compilando backend con PyInstaller...

SET VENV_DIR=%CD%\venv
SET PYTHON_CMD=
SET PIP_CMD=
SET PYTHON_FOUND=0

REM Función para buscar Python en el sistema
IF EXIST "%VENV_DIR%\Scripts\activate.bat" (
    echo   Activando entorno virtual...
    CALL "%VENV_DIR%\Scripts\activate.bat"
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD=python
        SET PIP_CMD=python -m pip
        SET PYTHON_FOUND=1
        echo   Entorno virtual activado.
    ) ELSE (
        echo   ADVERTENCIA: No se pudo activar el entorno virtual. Buscando Python del sistema...
    )
)

REM Si no se encontró Python en venv, buscar en el sistema
IF %PYTHON_FOUND%==0 (
    echo   Buscando Python instalado en el sistema...
    
    REM Intentar python
    python --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD=python
        SET PIP_CMD=python -m pip
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado con: python
        GOTO :python_found
    )
    
    REM Intentar py
    py --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD=py
        SET PIP_CMD=py -m pip
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado con: py
        GOTO :python_found
    )
    
    REM Intentar py -3
    py -3 --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD=py -3
        SET PIP_CMD=py -3 -m pip
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado con: py -3
        GOTO :python_found
    )
    
    REM Intentar py -3.12
    py -3.12 --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD=py -3.12
        SET PIP_CMD=py -3.12 -m pip
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado con: py -3.12
        GOTO :python_found
    )
    
    REM Intentar py -3.11
    py -3.11 --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD=py -3.11
        SET PIP_CMD=py -3.11 -m pip
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado con: py -3.11
        GOTO :python_found
    )
    
    REM Intentar py -3.10
    py -3.10 --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD=py -3.10
        SET PIP_CMD=py -3.10 -m pip
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado con: py -3.10
        GOTO :python_found
    )
    
    REM Buscar en ubicaciones comunes
    IF EXIST "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        SET PIP_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe" -m pip
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: %LOCALAPPDATA%\Programs\Python\Python312\
        GOTO :python_found
    )
    
    IF EXIST "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
        SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        SET PIP_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe" -m pip
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: %LOCALAPPDATA%\Programs\Python\Python311\
        GOTO :python_found
    )
    
    IF EXIST "%ProgramFiles%\Python312\python.exe" (
        SET PYTHON_CMD="%ProgramFiles%\Python312\python.exe"
        SET PIP_CMD="%ProgramFiles%\Python312\python.exe" -m pip
        SET PYTHON_FOUND=1
        echo   [OK] Python encontrado en: %ProgramFiles%\Python312\
        GOTO :python_found
    )
    
    REM Si no se encontró Python
    echo.
    echo   ============================================
    echo   ERROR: Python NO ENCONTRADO
    echo   ============================================
    echo.
    echo   Python no esta instalado o no esta en el PATH del sistema.
    echo.
    echo   SOLUCIONES:
    echo.
    echo   1. INSTALAR PYTHON:
    echo      - Visita: https://www.python.org/downloads/
    echo      - Descarga Python 3.9 o superior
    echo      - IMPORTANTE: Durante la instalacion, marca la opcion:
    echo        "Add Python to PATH" o "Agregar Python al PATH"
    echo      - Reinicia la terminal despues de instalar
    echo.
    echo   2. VERIFICAR INSTALACION:
    echo      Abre una nueva terminal y ejecuta:
    echo        python --version
    echo      O intenta:
    echo        py --version
    echo.
    echo   3. AGREGAR AL PATH MANUALMENTE:
    echo      Si Python esta instalado pero no funciona:
    echo      - Busca donde esta instalado (normalmente):
    echo        C:\Users\%USERNAME%\AppData\Local\Programs\Python\
    echo      - O: C:\Python3X\
    echo      - Agrega esa ruta al PATH del sistema
    echo.
    echo   4. REINICIAR TERMINAL:
    echo      Despues de instalar Python, CIERRA y ABRE una nueva terminal
    echo      antes de ejecutar este script nuevamente.
    echo.
    EXIT /B 1
)

:python_found

CD backend
IF ERRORLEVEL 1 (
    echo   ERROR: No se pudo cambiar al directorio backend
    EXIT /B 1
)

REM Verificar PyInstaller
%PYTHON_CMD% -c "import PyInstaller" 2>NUL
IF ERRORLEVEL 1 (
    echo   PyInstaller no esta instalado. Instalando...
    %PIP_CMD% install pyinstaller
    IF ERRORLEVEL 1 (
        echo   ERROR: No se pudo instalar PyInstaller
        EXIT /B 1
    )
)

IF NOT EXIST "sisfac-backend.spec" (
    echo   ERROR: No se encontro sisfac-backend.spec en el directorio backend
    EXIT /B 1
)

echo   Limpiando compilaciones anteriores...
IF EXIST build (
    RMDIR /S /Q build 2>NUL
    IF EXIST build (
        echo   ADVERTENCIA: No se pudo eliminar completamente build. Continuando...
    )
)
IF EXIST dist (
    RMDIR /S /Q dist 2>NUL
    IF EXIST dist (
        echo   ADVERTENCIA: No se pudo eliminar completamente dist. Continuando...
    )
)

echo   Compilando backend (sisfac-backend.spec)...
%PYTHON_CMD% -m PyInstaller sisfac-backend.spec
IF ERRORLEVEL 1 (
    echo   ERROR: PyInstaller fallo durante la compilacion
    EXIT /B 1
)

REM Verificar que se generó el ejecutable (en Windows puede ser .exe o sin extensión)
IF EXIST "dist\sisfac-backend.exe" (
    echo   Backend compilado correctamente: backend\dist\sisfac-backend.exe
    SET BACKEND_EXE=dist\sisfac-backend.exe
) ELSE IF EXIST "dist\sisfac-backend" (
    echo   Backend compilado correctamente: backend\dist\sisfac-backend
    SET BACKEND_EXE=dist\sisfac-backend
) ELSE (
    echo.
    echo   ERROR: No se genero el ejecutable en dist\
    echo   Verifica los archivos generados en dist\
    EXIT /B 1
)

CD ..

REM Paso 2: Empaquetar Electron para Windows
echo.
echo [2/2] Empaquetando aplicacion Electron (instalador Windows)...

CD electron
IF ERRORLEVEL 1 (
    echo   ERROR: No se pudo cambiar al directorio electron
    EXIT /B 1
)

REM Verificar Node.js y npm
where node >nul 2>&1
IF ERRORLEVEL 1 (
    echo   ERROR: Node.js no encontrado. Instala Node.js desde https://nodejs.org/
    EXIT /B 1
)

REM Verificar que package.json existe
IF NOT EXIST "package.json" (
    echo   ERROR: No se encontro package.json en el directorio electron
    EXIT /B 1
)

REM Verificar si electron-builder está instalado
IF EXIST "node_modules" (
    IF EXIST "node_modules\electron-builder" (
        echo   Dependencias de Electron ya instaladas.
    ) ELSE (
        echo   electron-builder no encontrado. Instalando dependencias...
        npm install
        IF ERRORLEVEL 1 (
            echo   ERROR: Fallo la instalacion de dependencias de Electron
            EXIT /B 1
        )
    )
) ELSE (
    echo   node_modules no existe. Instalando dependencias de Electron...
    npm install
    IF ERRORLEVEL 1 (
        echo   ERROR: Fallo la instalacion de dependencias
        EXIT /B 1
    )
)

REM Verificar que electron-builder está instalado después de npm install
IF NOT EXIST "node_modules\electron-builder" (
    echo   ERROR: electron-builder no se instalo correctamente
    EXIT /B 1
)

REM Verificar que el backend compilado existe antes de empaquetar
CD ..
IF NOT EXIST "backend\%BACKEND_EXE%" (
    echo   ERROR: El ejecutable del backend no existe: backend\%BACKEND_EXE%
    EXIT /B 1
)
CD electron

echo   Ejecutando electron-builder para Windows...
npm run build:win
IF ERRORLEVEL 1 (
    echo.
    echo   ERROR: Fallo electron-builder (npm run build:win)
    echo   Verifica que todas las dependencias esten instaladas: npm install
    echo   Verifica que el backend se compilo correctamente: backend\dist\
    EXIT /B 1
)

echo.
echo ================================
echo   Empaquetado completado!
echo ================================
echo.
echo Revisa la carpeta: %CD%\dist
IF EXIST "dist\*.exe" (
    echo   Instalador generado correctamente.
    DIR /B dist\*.exe
) ELSE (
    echo   ADVERTENCIA: No se encontro el instalador .exe en dist\
    echo   Verifica los archivos generados en dist\
)

POPD
ENDLOCAL

