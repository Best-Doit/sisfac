#!/bin/bash

# Script de inicio para SISFAC

echo "🚀 Iniciando SISFAC..."
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip --quiet

# Verificar si las dependencias están instaladas
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error: Falló la instalación de dependencias"
        exit 1
    fi
fi

# Cambiar al directorio backend
cd backend

# Iniciar la aplicación
echo ""
echo "✅ Iniciando servidor Flask..."
echo "🌐 Abre tu navegador en: http://localhost:5000"
echo "📝 Presiona Ctrl+C para detener el servidor"
echo ""
python run.py

