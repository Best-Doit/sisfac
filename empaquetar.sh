#!/bin/bash
# Script para empaquetar SISFAC completo
# Incluye: Backend (PyInstaller) + Frontend (Electron)

set -e

echo "🚀 Iniciando empaquetado de SISFAC..."
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paso 1: Recompilar backend con PyInstaller
echo -e "${YELLOW}📦 Paso 1: Recompilando backend con PyInstaller...${NC}"

# Detectar y activar entorno virtual
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR"
VENV_PATH="$ROOT_DIR/venv"

if [ -d "$VENV_PATH" ]; then
    echo "🔧 Activando entorno virtual..."
    source "$VENV_PATH/bin/activate"
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "⚠️  No se encontró venv, usando Python del sistema..."
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
fi

cd backend

# Verificar si PyInstaller está instalado
if ! $PYTHON_CMD -c "import PyInstaller" 2>/dev/null; then
    echo "⚠️  PyInstaller no está instalado. Instalando en el entorno virtual..."
    $PIP_CMD install pyinstaller
fi

# Limpiar compilaciones anteriores
echo "🧹 Limpiando compilaciones anteriores..."
rm -rf build/ dist/

# Compilar con PyInstaller usando el archivo .spec
echo "🔨 Compilando backend..."
$PYTHON_CMD -m PyInstaller sisfac-backend.spec

if [ -f "dist/sisfac-backend" ]; then
    echo -e "${GREEN}✅ Backend compilado correctamente${NC}"
    chmod +x dist/sisfac-backend
else
    echo "❌ Error: No se generó el ejecutable del backend"
    exit 1
fi

cd ..

# Desactivar venv si estaba activado
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate 2>/dev/null || true
fi

# Paso 2: Empaquetar con Electron
echo ""
echo -e "${YELLOW}📦 Paso 2: Empaquetando con Electron...${NC}"
cd electron

# Verificar Node.js y npm
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js no encontrado. Instala Node.js desde https://nodejs.org/"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm no encontrado. Instala npm junto con Node.js"
    exit 1
fi

# Verificar que el backend compilado existe
if [ ! -f "../backend/dist/sisfac-backend" ]; then
    echo "❌ Error: El ejecutable del backend no existe: ../backend/dist/sisfac-backend"
    echo "   Asegúrate de que el Paso 1 se completó correctamente"
    exit 1
fi

# Verificar que el archivo .spec existe
if [ ! -f "../backend/sisfac-backend.spec" ]; then
    echo "⚠️  Advertencia: No se encontró sisfac-backend.spec"
fi

# Verificar archivos necesarios
if [ ! -f "main.js" ]; then
    echo "❌ Error: No se encontró main.js en el directorio electron"
    exit 1
fi

if [ ! -f "package.json" ]; then
    echo "❌ Error: No se encontró package.json en el directorio electron"
    exit 1
fi

# Verificar si electron-builder está instalado o si node_modules no existe
if [ ! -d "node_modules" ] || ! npm list electron-builder >/dev/null 2>&1; then
    echo "⚠️  Instalando dependencias de Electron..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Error: Falló la instalación de dependencias de Electron"
        exit 1
    fi
fi

# Verificar que el icono existe (opcional, pero recomendado)
if [ ! -f "build/icon.png" ]; then
    echo "⚠️  Advertencia: No se encontró build/icon.png"
    echo "   El AppImage se creará sin icono personalizado"
    # Crear directorio build si no existe
    mkdir -p build
    
    # Intentar crear un icono placeholder simple si ImageMagick está disponible
    if command -v convert &> /dev/null; then
        echo "   Creando icono placeholder..."
        convert -size 512x512 xc:blue -pointsize 72 -fill white -gravity center -annotate +0+0 "SISFAC" build/icon.png 2>/dev/null || true
    fi
fi

# Limpiar compilaciones anteriores de Electron
echo "🧹 Limpiando compilaciones anteriores de Electron..."
rm -rf dist/linux-unpacked 2>/dev/null || true

# Empaquetar AppImage
echo "🔨 Generando AppImage..."
echo "   Esto puede tardar varios minutos..."

# Desactivar set -e temporalmente para capturar el error
set +e
npm run dist 2>&1 | tee /tmp/electron-builder.log
BUILD_EXIT_CODE=$?
set -e

if [ $BUILD_EXIT_CODE -ne 0 ]; then
    echo ""
    echo "❌ Error durante la creación del AppImage"
    echo ""
    echo "📋 Últimas líneas del log:"
    tail -30 /tmp/electron-builder.log
    echo ""
    echo "💡 Posibles soluciones:"
    echo "   1. Verifica que el backend esté compilado: ls -la ../backend/dist/"
    echo "   2. Verifica que todas las dependencias estén instaladas: npm install"
    echo "   3. Revisa el log completo: cat /tmp/electron-builder.log"
    echo "   4. Intenta limpiar y reinstalar: rm -rf node_modules && npm install"
    exit 1
fi

# Buscar el AppImage generado (puede tener diferentes nombres)
APPIMAGE_FILE=""
if [ -f "dist/SISFAC-1.0.0.AppImage" ]; then
    APPIMAGE_FILE="dist/SISFAC-1.0.0.AppImage"
elif [ -f "dist/SISFAC-1.0.0-x86_64.AppImage" ]; then
    APPIMAGE_FILE="dist/SISFAC-1.0.0-x86_64.AppImage"
else
    # Buscar cualquier AppImage en dist
    APPIMAGE_FILE=$(find dist -name "*.AppImage" -type f 2>/dev/null | head -1)
fi

if [ -n "$APPIMAGE_FILE" ] && [ -f "$APPIMAGE_FILE" ]; then
    # Hacer ejecutable
    chmod +x "$APPIMAGE_FILE"
    
    echo ""
    echo -e "${GREEN}✅ ¡Empaquetado completado exitosamente!${NC}"
    echo ""
    echo "📦 Archivo generado:"
    echo "   $(pwd)/$APPIMAGE_FILE"
    echo ""
    echo "📊 Tamaño del archivo:"
    ls -lh "$APPIMAGE_FILE" | awk '{print "   " $5}'
    echo ""
    echo "🚀 Para ejecutar:"
    echo "   chmod +x $APPIMAGE_FILE"
    echo "   ./$APPIMAGE_FILE"
    echo ""
    echo "💡 O usa el script ejecutar_appimage.sh:"
    echo "   ./ejecutar_appimage.sh $APPIMAGE_FILE"
else
    echo ""
    echo "❌ Error: No se generó el AppImage"
    echo ""
    echo "📋 Contenido del directorio dist:"
    ls -la dist/ 2>/dev/null || echo "   El directorio dist no existe"
    echo ""
    echo "💡 Revisa el log completo:"
    echo "   cat /tmp/electron-builder.log"
    exit 1
fi

cd ..

echo ""
echo -e "${GREEN}✨ Proceso completado${NC}"

