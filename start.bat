@echo off
REM Script de inicio para SISFAC en Windows

echo.
echo 🚀 Iniciando SISFAC...
echo.

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Error: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
)

REM Activar entorno virtual
echo 🔌 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo 📦 Actualizando pip...
python -m pip install --upgrade pip --quiet

REM Verificar si las dependencias están instaladas
python -c "import flask" 2>nul
if errorlevel 1 (
    echo 📦 Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error: Falló la instalación de dependencias
        pause
        exit /b 1
    )
)

REM Cambiar al directorio backend
cd backend

REM Iniciar la aplicación
echo.
echo ✅ Iniciando servidor Flask...
echo 🌐 Abre tu navegador en: http://localhost:5000
echo 📝 Presiona Ctrl+C para detener el servidor
echo.
python run.py
