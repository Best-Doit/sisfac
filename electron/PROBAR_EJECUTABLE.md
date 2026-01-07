# 🧪 Probar el Ejecutable Independiente

## ✅ Ejecutable Creado

El ejecutable independiente se encuentra en:
```
electron/dist/SISFAC-1.0.0.AppImage
```

**Tamaño**: ~123 MB (incluye Electron + Python empaquetado + Backend Flask)

## 🚀 Cómo Ejecutar

### Opción 1: Ejecución Directa
```bash
cd electron/dist
chmod +x SISFAC-1.0.0.AppImage
./SISFAC-1.0.0.AppImage
```

### Opción 2: Desde Cualquier Ubicación
```bash
./electron/dist/SISFAC-1.0.0.AppImage
```

### Opción 3: Hacer Ejecutable Globalmente
```bash
sudo mv electron/dist/SISFAC-1.0.0.AppImage /usr/local/bin/sisfac
sudo chmod +x /usr/local/bin/sisfac
sisfac
```

## ✅ Verificación de Independencia

El ejecutable **NO requiere**:
- ❌ Python instalado en el sistema
- ❌ Dependencias Python instaladas
- ❌ Node.js instalado
- ❌ NPM instalado

**Todo está incluido** dentro del AppImage.

## 🔍 Verificar Contenido

Para verificar que el backend está incluido:

```bash
# Extraer el AppImage temporalmente
./dist/SISFAC-1.0.0.AppImage --appimage-extract

# Verificar que el ejecutable del backend existe
ls -lh squashfs-root/resources/backend/dist/sisfac-backend

# Limpiar
rm -rf squashfs-root
```

## 📝 Notas

1. **Primera ejecución**: Puede tardar 2-5 segundos en iniciar
2. **Base de datos**: Se creará automáticamente si no existe
3. **Puerto**: La aplicación usa el puerto 5000 (http://127.0.0.1:5000)
4. **Cerrar**: Cierra la ventana para detener la aplicación

## 🐛 Solución de Problemas

### Error: "Permission denied"
```bash
chmod +x SISFAC-1.0.0.AppImage
```

### Error: "Cannot execute binary file"
- Verifica que estés en un sistema Linux 64-bit
- El AppImage es solo para Linux x64

### La aplicación no inicia
- Verifica los logs en la terminal donde ejecutaste el AppImage
- Asegúrate de que el puerto 5000 no esté en uso

## 📦 Distribución

Para distribuir la aplicación:
1. Copia el archivo `SISFAC-1.0.0.AppImage` a cualquier sistema Linux
2. Hazlo ejecutable: `chmod +x SISFAC-1.0.0.AppImage`
3. Ejecútalo directamente

**No requiere instalación ni dependencias adicionales.**

