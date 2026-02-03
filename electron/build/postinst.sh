#!/bin/bash
# Script postinst para actualizar el archivo .desktop y crear enlace simbólico después de la instalación
# SOLUCIÓN DEFINITIVA: Usar wrapper script para forzar flags de sandbox

set -e

DESKTOP_FILE="/usr/share/applications/sisfac-desktop.desktop"
EXECUTABLE="/opt/SISFAC/sisfac-desktop"
WRAPPER="/opt/SISFAC/sisfac-wrapper.sh"
SYMLINK="/usr/bin/sisfac-desktop"
BACKEND="/opt/SISFAC/resources/backend/sisfac-backend"
ICON_SRC="/opt/SISFAC/resources/icon.png"
ICON_DIR="/usr/share/icons/hicolor/512x512/apps"
ICON_TARGET="${ICON_DIR}/sisfac-desktop.png"

# Establecer permisos del backend (requiere root, por eso está aquí)
if [ -f "$BACKEND" ]; then
    chmod +x "$BACKEND"
    echo "✅ Permisos del backend establecidos: $BACKEND"
fi

# Instalar icono en el tema hicolor para que el menú lo detecte
if [ -f "$ICON_SRC" ]; then
    mkdir -p "$ICON_DIR"
    cp -f "$ICON_SRC" "$ICON_TARGET"
    chmod 644 "$ICON_TARGET"
    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
        gtk-update-icon-cache -f /usr/share/icons/hicolor >/dev/null 2>&1 || true
    fi
    echo "✅ Icono instalado: $ICON_TARGET"
fi

# Crear wrapper script SIEMPRE (sobrescribe si existe para asegurar que esté actualizado)
if [ -f "$EXECUTABLE" ]; then
    cat > "$WRAPPER" << 'EOF'
#!/bin/bash
# Wrapper script para SISFAC Desktop
# FORZAR flags de sandbox ANTES de que Electron inicie
export ELECTRON_DISABLE_SANDBOX=1
exec /opt/SISFAC/sisfac-desktop --no-sandbox --disable-setuid-sandbox --disable-zygote "$@"
EOF
    chmod +x "$WRAPPER"
    echo "✅ Script wrapper creado/actualizado: $WRAPPER"
fi

# Crear/actualizar enlace simbólico al wrapper (NO al ejecutable directo)
if [ -f "$WRAPPER" ]; then
    # Eliminar enlace existente si apunta al ejecutable directo
    if [ -L "$SYMLINK" ]; then
        CURRENT_TARGET=$(readlink "$SYMLINK")
        if [ "$CURRENT_TARGET" != "$WRAPPER" ] && [ "$CURRENT_TARGET" != "/opt/SISFAC/sisfac-wrapper.sh" ]; then
            rm -f "$SYMLINK"
            echo "⚠️  Eliminado enlace antiguo que apuntaba a: $CURRENT_TARGET"
        fi
    fi
    
    # Crear enlace al wrapper si no existe o está roto
    if [ ! -L "$SYMLINK" ] || [ ! -e "$SYMLINK" ]; then
        # Usar update-alternatives si está disponible, sino crear enlace directo
        if command -v update-alternatives >/dev/null 2>&1; then
            update-alternatives --install "$SYMLINK" sisfac-desktop "$WRAPPER" 100 2>/dev/null || {
                # Si falla, crear enlace directo
                ln -sf "$WRAPPER" "$SYMLINK"
            }
        else
            ln -sf "$WRAPPER" "$SYMLINK"
        fi
        echo "✅ Enlace simbólico creado: $SYMLINK -> $WRAPPER"
    else
        echo "✅ Enlace simbólico ya existe y apunta correctamente al wrapper"
    fi
fi

# Actualizar archivo .desktop para usar el wrapper (más limpio que pasar flags directamente)
if [ -f "$DESKTOP_FILE" ]; then
    # Usar el wrapper en lugar del ejecutable directo con flags
    sed -i 's|^Exec=.*|Exec=/opt/SISFAC/sisfac-wrapper.sh %U|' "$DESKTOP_FILE"
    
    # Actualizar la base de datos de aplicaciones
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
    
    echo "✅ Archivo .desktop actualizado para usar wrapper"
fi

exit 0
