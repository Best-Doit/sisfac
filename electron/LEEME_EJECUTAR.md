# 🚀 Cómo Ejecutar el AppImage

## ✅ Solución Rápida (Recomendada)

El AppImage funciona correctamente, pero necesita ejecutarse con flags especiales para deshabilitar el sandbox.

### Opción 1: Usar el Script Wrapper (Más Fácil)

```bash
cd electron
./ejecutar_appimage.sh ./dist/SISFAC-1.0.0.AppImage
```

Este script configura automáticamente las variables de entorno necesarias.

### Opción 2: Ejecutar Manualmente con Variables de Entorno

```bash
cd electron/dist
export ELECTRON_DISABLE_SANDBOX=1
./SISFAC-1.0.0.AppImage --no-sandbox --disable-setuid-sandbox
```

### Opción 3: Una Línea

```bash
ELECTRON_DISABLE_SANDBOX=1 ./electron/dist/SISFAC-1.0.0.AppImage --no-sandbox --disable-setuid-sandbox
```

## 📝 Notas

- El AppImage **funciona correctamente** cuando se ejecuta con estas opciones
- El backend Flask se inicia automáticamente
- La aplicación se abre en http://127.0.0.1:5000
- **No requiere Python ni dependencias instaladas** - todo está incluido

## 🔧 Para Hacer el AppImage Ejecutable Directamente

Si quieres que el AppImage funcione sin el script wrapper, necesitas:

1. Instalar `appimagetool`:
   ```bash
   sudo apt install appimagetool
   ```

2. Modificar y re-empacar:
   ```bash
   cd electron
   ./build/fixAppImage.sh ./dist/SISFAC-1.0.0.AppImage
   appimagetool squashfs-root ./dist/SISFAC-1.0.0-fixed.AppImage
   ```

Pero **la solución más práctica es usar el script wrapper** que ya está incluido.

## ✅ Verificación

Para verificar que funciona:

```bash
cd electron
./ejecutar_appimage.sh ./dist/SISFAC-1.0.0.AppImage
```

Luego abre tu navegador en: http://127.0.0.1:5000

