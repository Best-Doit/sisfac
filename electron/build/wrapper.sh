#!/bin/bash
# Wrapper script para SISFAC Desktop
# Asegura que las flags de sandbox se apliquen correctamente

export ELECTRON_DISABLE_SANDBOX=1

# Obtener el directorio donde está el ejecutable real
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXECUTABLE="$SCRIPT_DIR/sisfac-desktop"

# Si no encontramos el ejecutable en el mismo directorio, usar la ruta de instalación
if [ ! -f "$EXECUTABLE" ]; then
    EXECUTABLE="/opt/SISFAC/sisfac-desktop"
fi

# Ejecutar el ejecutable con flags de sandbox deshabilitadas
exec "$EXECUTABLE" --no-sandbox --disable-setuid-sandbox --disable-zygote "$@"
