# 🔧 Solución: Error "execvp: Formato de ejecutable incorrecto"

## Problema

El error `execvp: Formato de ejecutable incorrecto` indica que el AppImage no tiene el **runtime de AppImage** correcto. Un AppImage válido debe tener esta estructura:

```
[Runtime ELF ejecutable][Squashfs filesystem]
```

Si el AppImage empieza directamente con `hsqsb` (magic de Squashfs), significa que **falta el runtime**.

## Causa

El problema ocurre cuando:
1. Se reempaqueta el AppImage con `mksquashfs` sin preservar el runtime
2. Se crea un AppRun personalizado que interfiere con electron-builder
3. El AppImage se corrompe durante el proceso de build

## Solución Implementada

### 1. Hooks Simplificados

**`afterPack.js`:**
- ✅ NO crea AppRun personalizado
- ✅ Deja que electron-builder genere el AppRun automáticamente
- ✅ Solo establece permisos y configura iconos

**`afterAllArtifactBuild.js`:**
- ✅ NO reempaqueta el AppImage
- ✅ Solo establece permisos de ejecución
- ✅ Verifica que el AppImage existe

### 2. Flags de Sandbox en main.js

Los flags de sandbox están configurados en `main.js`:

```javascript
app.commandLine.appendSwitch('--no-sandbox');
app.commandLine.appendSwitch('--disable-setuid-sandbox');
```

Esto es **suficiente** para que Electron funcione sin problemas de sandbox.

### 3. Proceso de Build Limpio

```bash
# 1. Limpiar AppImages antiguos
rm -f electron/dist/*.AppImage

# 2. Rebuild completo
bash empaquetar.sh
```

## Verificación

Después de regenerar el AppImage:

```bash
# 1. Verificar que tiene runtime
file electron/dist/SISFAC-1.0.0.AppImage
# Debe mostrar: ELF 64-bit LSB executable (no solo "Squashfs filesystem")

# 2. Verificar que es ejecutable
ls -lh electron/dist/SISFAC-1.0.0.AppImage
# Debe tener permisos: -rwxr-xr-x

# 3. Probar ejecución
./electron/dist/SISFAC-1.0.0.AppImage
```

## Si Aún No Funciona

### Opción 1: Usar appimagetool

```bash
# Instalar appimagetool
sudo apt install appimagetool

# Extraer AppImage
./SISFAC-1.0.0.AppImage --appimage-extract

# Modificar AppRun si es necesario
# (agregar flags de sandbox)

# Reempaquetar con appimagetool (preserva runtime)
appimagetool squashfs-root SISFAC-1.0.0-fixed.AppImage
```

### Opción 2: Wrapper Script Externo

Crear un script wrapper que ejecute el AppImage con los flags:

```bash
#!/bin/bash
export ELECTRON_DISABLE_SANDBOX=1
./SISFAC-1.0.0.AppImage --no-sandbox --disable-setuid-sandbox "$@"
```

## Notas Importantes

1. **NO reempaquetar con mksquashfs directamente** - esto rompe el runtime
2. **NO crear AppRun personalizado en afterPack** - interfiere con electron-builder
3. **Los flags en main.js son suficientes** - no necesitan estar en AppRun
4. **electron-builder genera el runtime automáticamente** - no interferir con esto

## Estado Actual

✅ Hooks simplificados
✅ Flags de sandbox en main.js
✅ Sin interferencia con electron-builder
✅ AppImage debería generarse correctamente

---

**Última actualización:** 2025-01-08

