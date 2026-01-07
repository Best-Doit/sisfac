@echo off
REM Script TODO-EN-UNO para Windows
REM - Instala Python (verifica)
REM - Instala Node.js y Electron (si no están)
REM - Prepara entorno completo

SETLOCAL ENABLEDELAYEDEXPANSION

echo.
echo ================================
echo   Preparar TODO SISFAC (Windows)
echo   Python + Node.js + Electron
echo ================================
echo.

SET ROOT_DIR=%~dp0..
PUSHD "%ROOT_DIR%"

REM Paso 1: Python
echo [1/3] Preparando Python y dependencias...
echo   Instalando Python y todas las dependencias del proyecto...
CALL "%~dp0preparar_entorno_windows.bat"
IF ERRORLEVEL 1 (
    echo   ERROR: Fallo la preparacion de Python.
    EXIT /B 1
)
echo   Python y dependencias instaladas correctamente.

REM Paso 2: Node.js y Electron
echo.
echo [2/3] Preparando Node.js y Electron...
echo   Instalando Node.js (si no esta) y Electron en el proyecto...
CALL "%~dp0instalar_nodejs_electron_windows.bat"
IF ERRORLEVEL 1 (
    echo   ERROR: Fallo la instalacion de Node.js/Electron.
    EXIT /B 1
)
echo   Node.js y Electron instalados correctamente.

REM Paso 3: Verificación final
echo.
echo [3/3] Verificacion final...
echo.

REM Verificar Python en venv
IF EXIST "venv\Scripts\activate.bat" (
    echo Verificando Python en entorno virtual...
    CALL venv\Scripts\activate.bat
    IF NOT ERRORLEVEL 1 (
        REM Intentar múltiples formas de ejecutar Python
        SET PYTHON_VERIFY_CMD=
        python --version >nul 2>&1
        IF NOT ERRORLEVEL 1 (
            SET PYTHON_VERIFY_CMD=python
        ) ELSE (
            py --version >nul 2>&1
            IF NOT ERRORLEVEL 1 (
                SET PYTHON_VERIFY_CMD=py
            ) ELSE (
                py -3 --version >nul 2>&1
                IF NOT ERRORLEVEL 1 (
                    SET PYTHON_VERIFY_CMD=py -3
                )
            )
        )
        
        IF DEFINED PYTHON_VERIFY_CMD (
            !PYTHON_VERIFY_CMD! --version 2>NUL
            !PYTHON_VERIFY_CMD! -c "import flask; print('Flask:', flask.__version__)" 2>NUL || echo   Flask: No encontrado
            !PYTHON_VERIFY_CMD! -c "import PyInstaller; print('PyInstaller: OK')" 2>NUL || echo   PyInstaller: No encontrado
        ) ELSE (
            echo   ADVERTENCIA: No se pudo verificar Python en el entorno virtual.
        )
        CALL venv\Scripts\deactivate.bat 2>NUL
    ) ELSE (
        echo   ADVERTENCIA: No se pudo activar el entorno virtual para verificar.
    )
) ELSE (
    echo   ADVERTENCIA: Entorno virtual no encontrado.
    echo   Ejecuta primero: scripts\preparar_entorno_windows.bat
)

echo.
echo Verificando Node.js:
where node >nul 2>&1
IF NOT ERRORLEVEL 1 (
    node --version
) ELSE (
    echo   Node.js no encontrado en PATH
)

echo.
echo Verificando Electron:
IF EXIST "electron" (
    CD electron
    IF NOT ERRORLEVEL 1 (
        IF EXIST "node_modules" (
            npm list electron --depth=0 2>NUL || echo   Electron: No encontrado en node_modules
            npm list electron-builder --depth=0 2>NUL || echo   electron-builder: No encontrado en node_modules
        ) ELSE (
            echo   node_modules no existe. Ejecuta: npm install
        )
        CD ..
    ) ELSE (
        echo   ERROR: No se pudo cambiar al directorio electron
        EXIT /B 1
    )
) ELSE (
    echo   ADVERTENCIA: Directorio electron no encontrado.
)

echo.
echo ================================
echo   TODO LISTO!
echo ================================
echo.
echo Puedes:
echo   1. Iniciar la aplicacion:
echo      venv\Scripts\activate
echo      cd backend
echo      python run.py
echo.
echo   2. Empaquetar la aplicacion:
echo      scripts\empaquetar_windows.bat
echo.

POPD
ENDLOCAL

