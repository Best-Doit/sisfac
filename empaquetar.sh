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

# Paso 0: Preservar datos del AppImage anterior (si existe)
echo -e "${YELLOW}💾 Paso 0: Preservando datos del AppImage anterior (si existe)...${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR"
VENV_PATH="$ROOT_DIR/venv"

# Buscar AppImage anterior en el directorio electron/dist
OLD_APPIMAGE=""
if [ -d "$ROOT_DIR/electron/dist" ]; then
    OLD_APPIMAGE=$(find "$ROOT_DIR/electron/dist" -name "SISFAC-*.AppImage" -type f 2>/dev/null | head -1)
fi

if [ -n "$OLD_APPIMAGE" ] && [ -f "$OLD_APPIMAGE" ]; then
    echo "   📦 AppImage anterior encontrado: $(basename "$OLD_APPIMAGE")"
    echo "   🔍 Extrayendo datos del AppImage anterior..."
    
    # Crear directorio temporal para extraer
    TEMP_EXTRACT=$(mktemp -d)
    cd "$TEMP_EXTRACT"
    
    # Extraer AppImage
    "$OLD_APPIMAGE" --appimage-extract >/dev/null 2>&1
    
    if [ -d "squashfs-root" ]; then
        # Buscar base de datos en el AppImage extraído
        # Puede estar en resources/ o en el directorio raíz del AppImage
        DB_SOURCES=(
            "squashfs-root/resources/sisfac.db"
            "squashfs-root/resources/app.asar.unpacked/sisfac.db"
            "squashfs-root/sisfac.db"
        )
        
        BACKUP_SOURCES=(
            "squashfs-root/resources/backups"
            "squashfs-root/resources/app.asar.unpacked/backups"
            "squashfs-root/backups"
        )
        
        # Copiar base de datos si existe
        for db_source in "${DB_SOURCES[@]}"; do
            if [ -f "$db_source" ]; then
                echo "   ✅ Base de datos encontrada en AppImage anterior"
                cp "$db_source" "$ROOT_DIR/sisfac.db"
                echo "   💾 Base de datos copiada a: $ROOT_DIR/sisfac.db"
                break
            fi
        done
        
        # Copiar backups si existen
        for backup_source in "${BACKUP_SOURCES[@]}"; do
            if [ -d "$backup_source" ] && [ "$(ls -A $backup_source 2>/dev/null)" ]; then
                echo "   ✅ Backups encontrados en AppImage anterior"
                mkdir -p "$ROOT_DIR/backups"
                cp -r "$backup_source"/* "$ROOT_DIR/backups/" 2>/dev/null || true
                echo "   💾 Backups copiados a: $ROOT_DIR/backups/"
                break
            fi
        done
        
        # Limpiar
        cd "$ROOT_DIR"
        rm -rf "$TEMP_EXTRACT"
    else
        echo "   ⚠️  No se pudo extraer el AppImage anterior"
        cd "$ROOT_DIR"
        rm -rf "$TEMP_EXTRACT"
    fi
else
    echo "   ℹ️  No se encontró AppImage anterior, se usará la base de datos actual del proyecto"
fi

# Verificar si existe base de datos en el proyecto
if [ -f "$ROOT_DIR/sisfac.db" ]; then
    DB_SIZE=$(du -h "$ROOT_DIR/sisfac.db" | cut -f1)
    echo "   ✅ Base de datos encontrada en proyecto: $DB_SIZE"
    echo "      📍 Ubicación: $ROOT_DIR/sisfac.db"
else
    echo "   ℹ️  No hay base de datos en el proyecto, se creará una nueva al ejecutar"
fi

# Verificar backups
if [ -d "$ROOT_DIR/backups" ] && [ "$(ls -A $ROOT_DIR/backups 2>/dev/null)" ]; then
    BACKUP_COUNT=$(ls -1 "$ROOT_DIR/backups"/*.db 2>/dev/null | wc -l)
    BACKUP_SIZE=$(du -sh "$ROOT_DIR/backups" 2>/dev/null | cut -f1)
    echo "   ✅ Backups encontrados: $BACKUP_COUNT archivo(s) ($BACKUP_SIZE)"
    echo "      📍 Ubicación: $ROOT_DIR/backups/"
else
    echo "   ℹ️  No hay backups en el proyecto"
    # Crear directorio backups vacío para que se incluya en el empaquetado
    mkdir -p "$ROOT_DIR/backups"
fi

echo ""
echo "   📋 Resumen de datos que se incluirán en el nuevo AppImage:"
if [ -f "$ROOT_DIR/sisfac.db" ]; then
    echo "      ✅ Base de datos: sisfac.db"
else
    echo "      ⚠️  Base de datos: No existe (se creará nueva)"
fi
if [ -d "$ROOT_DIR/backups" ]; then
    echo "      ✅ Directorio de backups: backups/"
fi
echo ""

# Paso 1: Recompilar backend con PyInstaller
echo -e "${YELLOW}📦 Paso 1: Recompilando backend con PyInstaller...${NC}"

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
    
    # Verificar que los datos se incluyeron (extraer temporalmente y verificar)
    echo "🔍 Verificando que los datos se incluyeron correctamente..."
    TEMP_VERIFY=$(mktemp -d)
    cd "$TEMP_VERIFY"
    
    "$APPIMAGE_FILE" --appimage-extract >/dev/null 2>&1
    
    if [ -d "squashfs-root" ]; then
        DATA_FOUND=0
        
        # Verificar base de datos
        if [ -f "squashfs-root/resources/sisfac.db" ] || [ -f "squashfs-root/resources/app.asar.unpacked/sisfac.db" ]; then
            echo "   ✅ Base de datos incluida en el AppImage"
            DATA_FOUND=1
        else
            echo "   ⚠️  Base de datos no encontrada en el AppImage (se creará nueva al ejecutar)"
        fi
        
        # Verificar backups
        if [ -d "squashfs-root/resources/backups" ] || [ -d "squashfs-root/resources/app.asar.unpacked/backups" ]; then
            BACKUP_COUNT=$(find squashfs-root/resources -name "*.db" -path "*/backups/*" 2>/dev/null | wc -l)
            if [ "$BACKUP_COUNT" -gt 0 ]; then
                echo "   ✅ Backups incluidos en el AppImage: $BACKUP_COUNT archivo(s)"
                DATA_FOUND=1
            fi
        fi
        
        if [ "$DATA_FOUND" -eq 1 ]; then
            echo "   ✅ Los datos se preservaron correctamente"
        fi
    fi
    
    # Limpiar
    cd "$ROOT_DIR"
    rm -rf "$TEMP_VERIFY"
    
    echo ""
    echo "🚀 Para ejecutar:"
    echo "   chmod +x $APPIMAGE_FILE"
    echo "   ./$APPIMAGE_FILE"
    echo ""
    echo "💡 O usa el script ejecutar_appimage.sh:"
    echo "   ./ejecutar_appimage.sh $APPIMAGE_FILE"
    echo ""
    echo "📝 Nota: Si tenías datos en el AppImage anterior, se han preservado en el nuevo."
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

