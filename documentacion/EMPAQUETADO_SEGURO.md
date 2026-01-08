# 🔒 Guía de Empaquetado Seguro - SISFAC

## ⚠️ IMPORTANTE: Protección de Datos de Producción

Este documento explica cómo el sistema garantiza que **los datos de producción nunca se toquen** durante el empaquetado y actualización.

## 📍 Ubicación de Datos

### En Producción (AppImage ejecutándose)
- **Base de datos**: `~/.sisfac/sisfac.db`
- **Backups**: `~/.sisfac/backups/`
- **Nunca se tocan** durante actualizaciones

### En Desarrollo
- **Base de datos**: `./sisfac.db` (raíz del proyecto)
- **Backups**: `./backups/` (raíz del proyecto)

## 🔄 Flujo de Actualización Seguro

### 1. Empaquetado (`empaquetar.sh`)
- ✅ Solo incluye **código** en el AppImage
- ✅ Puede incluir base de datos inicial/vacía (opcional)
- ❌ **NO copia** datos del AppImage anterior
- ❌ **NO toca** datos en `~/.sisfac/`

### 2. Ejecución del Nuevo AppImage
- ✅ Busca datos en `~/.sisfac/sisfac.db` (producción)
- ✅ Si existe, **usa esos datos** (no los sobrescribe)
- ✅ Si no existe, copia base de datos inicial del AppImage (solo primera vez)
- ✅ Los datos de producción **nunca se modifican**

### 3. Configuración (`backend/app/config.py`)
```python
# Solo copia desde recursos si NO existe en producción
if resources_db and os.path.exists(resources_db) and not os.path.exists(db_path):
    # Primera ejecución: copiar datos iniciales
    shutil.copy2(resources_db, db_path)
# Si db_path ya existe, NO hace nada (protege datos de producción)
```

## ✅ Garantías de Seguridad

1. **Los datos en `~/.sisfac/` nunca se tocan**
2. **El script de empaquetado NO copia datos del AppImage anterior**
3. **Solo se copian datos iniciales si es la primera ejecución**
4. **Las actualizaciones solo cambian código, no datos**

## 📋 Checklist de Empaquetado

Antes de empaquetar:

- [ ] Verificar que `~/.sisfac/` contiene los datos de producción
- [ ] Asegurarse de que `./sisfac.db` en el proyecto es solo para desarrollo
- [ ] No incluir datos de producción en el proyecto
- [ ] Ejecutar `./empaquetar.sh` (no toca datos de producción)

## 🚨 Advertencias

- ⚠️ **NO** copiar datos de `~/.sisfac/` al proyecto antes de empaquetar
- ⚠️ **NO** modificar el script para extraer datos del AppImage anterior
- ⚠️ **NO** incluir datos de producción en el repositorio

## 🔍 Verificación

Después de empaquetar, verificar:

```bash
# 1. Verificar que el AppImage se creó
ls -lh electron/dist/SISFAC-*.AppImage

# 2. Verificar que los datos de producción siguen intactos
ls -lh ~/.sisfac/sisfac.db

# 3. Ejecutar el nuevo AppImage (debe usar datos existentes)
./electron/dist/SISFAC-1.0.0.AppImage
```

## 📝 Notas

- El AppImage puede incluir una base de datos inicial/vacía
- Esta base de datos inicial solo se usa si no existe `~/.sisfac/sisfac.db`
- Una vez que existe `~/.sisfac/sisfac.db`, esa es la que se usa siempre
- Los backups también están en `~/.sisfac/backups/` y no se tocan

