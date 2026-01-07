#!/bin/bash
# Script wrapper para ejecutar el AppImage con sandbox deshabilitado

APPIMAGE_PATH="$1"

if [ -z "$APPIMAGE_PATH" ]; then
    APPIMAGE_PATH="./dist/SISFAC-1.0.0.AppImage"
fi

if [ ! -f "$APPIMAGE_PATH" ]; then
    echo "Error: No se encontró el AppImage en: $APPIMAGE_PATH"
    exit 1
fi

# Deshabilitar sandbox
export ELECTRON_DISABLE_SANDBOX=1

# Ejecutar el AppImage con flags adicionales
exec "$APPIMAGE_PATH" --no-sandbox --disable-setuid-sandbox "$@"

