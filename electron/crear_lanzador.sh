#!/bin/bash
# Script para crear un lanzador .desktop para el AppImage

APPIMAGE_PATH="$1"
DESKTOP_FILE="$HOME/.local/share/applications/SISFAC.desktop"

if [ -z "$APPIMAGE_PATH" ]; then
    APPIMAGE_PATH="$(pwd)/dist/SISFAC-1.0.0.AppImage"
fi

if [ ! -f "$APPIMAGE_PATH" ]; then
    echo "Error: No se encontró el AppImage en: $APPIMAGE_PATH"
    echo "Uso: $0 [ruta_al_AppImage]"
    exit 1
fi

# Obtener la ruta absoluta
APPIMAGE_PATH=$(readlink -f "$APPIMAGE_PATH")

# Crear directorio si no existe
mkdir -p "$HOME/.local/share/applications"

# Crear archivo .desktop
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=SISFAC
Comment=Sistema de Facturación con Inventario y Clientes
Exec=env ELECTRON_DISABLE_SANDBOX=1 "$APPIMAGE_PATH" --no-sandbox --disable-setuid-sandbox
Icon=application-x-executable
Terminal=false
Categories=Office;Finance;
MimeType=
StartupNotify=true
EOF

# Hacer ejecutable
chmod +x "$DESKTOP_FILE"

echo "✅ Lanzador creado en: $DESKTOP_FILE"
echo ""
echo "Ahora puedes:"
echo "1. Buscar 'SISFAC' en el menú de aplicaciones"
echo "2. Hacer doble clic en el archivo .desktop"
echo "3. Arrastrarlo al escritorio o al dock"
echo ""
echo "Para actualizar el caché de aplicaciones:"
echo "  update-desktop-database ~/.local/share/applications/"

