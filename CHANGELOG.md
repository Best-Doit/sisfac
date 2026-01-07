# Changelog - SISFAC

Registro de cambios y mejoras del sistema de facturación.

## [Versión Actual] - 2024

### 🎯 Cambios Principales

#### Sistema de Facturación
- **Eliminación de estados de factura**: Las facturas ya no tienen estados (Pendiente/Pagada/Anulada). El sistema funciona como respaldo virtual de facturas físicas con pago instantáneo.
- **Simplificación del formulario de facturación**:
  - Eliminado campo "Fecha de Vencimiento"
  - Eliminado campo "IVA" (siempre en 0)
  - Eliminado campo "Notas"
  - Eliminado checkbox "Actualizar stock" (siempre se actualiza automáticamente)
- **Rediseño de la tabla de facturación**:
  - Tabla más compacta con mejor uso del espacio
  - Una sola columna de precio con botón desplegable azul
  - Precio mostrado como texto al lado del botón
  - Tabla ocupa toda la pantalla disponible con scroll automático
  - Tamaño de texto aumentado para mejor legibilidad

#### Sistema de Precios
- **Unificación a dos precios**: El sistema ahora maneja solo dos precios alternativos (P1 y P2) además del precio principal.
  - Eliminado precio_3 de la base de datos
  - Migración automática ejecutada
  - Menú desplegable muestra: P1, P2 y Principal
  - Por defecto se selecciona P1 (el más alto)

#### Validaciones y Mejoras de UX
- **Validación de stock**: No se permite agregar productos con stock 0 al carrito
  - Botón deshabilitado cuando stock = 0
  - Validación en la tabla de factura para no exceder stock disponible
  - Indicadores visuales (opacidad reducida para productos sin stock)
- **Búsqueda predictiva**: Implementada en módulos de Clientes y Facturas
  - Autocompletado con sugerencias
  - Búsqueda en tiempo real
- **Sidebar colapsable**: 
  - Estado persistente durante la navegación
  - Sin parpadeos al cambiar de página
  - Diseño responsive

#### Módulo de Ajustes
- **Nuevo módulo de ajustes** (`/ajustes`):
  - **Crear backup**: Genera copias de seguridad automáticas con timestamp
  - **Restaurar backup**: Permite restaurar desde archivo .db
  - **Lista de backups**: Muestra todos los backups disponibles con fecha y tamaño
  - **Descargar backups**: Descarga individual de cada backup
  - **Borrar datos**: Elimina todos los datos del sistema con confirmación doble
    - Crea backup automático antes de borrar
    - Manejo correcto de foreign keys
    - Validación de confirmación

#### Módulo de Clientes
- **Simplificación**: Solo dos campos requeridos
  - Nombre
  - Cédula de Identidad
- **Historial de facturas**: Vista detallada del historial de facturas por cliente

#### Módulo de Inventario
- **Eliminación de categorías**: Campo de categoría removido
- **Importación desde Excel**: 
  - Plantilla descargable con campos predefinidos
  - Soporte para múltiples precios (Precio de Venta 1, Precio de Venta 2)
  - Mapeo correcto de columnas
- **Búsqueda normal**: Sin autocompletado (búsqueda tradicional)

#### Módulo de Facturación
- **Flujo mejorado "Facturar"**:
  - Lista de productos ordenada por stock (mayor a menor)
  - Selección de productos en carrito lateral
  - Tabla de factura manual con todas las columnas visibles
  - Validación de stock en tiempo real
  - Precio por defecto: P1 (el más alto)
- **Eliminación de botón "Nueva Factura"**: Solo disponible el flujo "Facturar"

### 🔧 Mejoras Técnicas

#### Base de Datos
- Migración de precios: Eliminada columna `precio_3`
- Modelo actualizado: Solo `precio_unitario`, `precio_1`, `precio_2`
- Foreign keys manejadas correctamente en operaciones de borrado

#### Frontend
- Alpine.js mejorado para mejor rendimiento
- CSS optimizado para evitar parpadeos
- Mejor manejo de estados con localStorage
- Diseño responsive mejorado

#### Backend
- Rutas optimizadas
- Mejor manejo de errores
- Validaciones mejoradas
- Scripts de migración para cambios de esquema

### 📋 Estructura de Archivos Actualizada

```
SISFAC/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── ajustes.py      # NUEVO: Módulo de ajustes y backups
│   │   │   ├── clientes.py      # Actualizado: Solo nombre y CI
│   │   │   ├── inventario.py   # Actualizado: Sin categorías, 2 precios
│   │   │   ├── facturas.py     # Actualizado: Sin estados, sin IVA
│   │   │   └── talonarios.py
│   │   └── templates/
│   │       ├── ajustes/        # NUEVO: Templates de ajustes
│   │       └── facturas/
│   │           └── facturar.html  # Rediseñado completamente
├── scripts/
│   ├── migrate_precios_unificar.py  # NUEVO: Migración de precios
│   └── migrate_db.py
└── backups/                    # NUEVO: Directorio de backups
```

### 🐛 Correcciones

- Corregido problema de parpadeo del sidebar al navegar
- Corregido overflow en tablas de facturación
- Corregida función de borrar datos (manejo de foreign keys)
- Corregida validación de stock en carrito
- Corregido z-index del menú desplegable de precios

### 📝 Notas de Migración

Si actualizas desde una versión anterior:

1. **Ejecutar migración de precios**:
   ```bash
   python3 scripts/migrate_precios_unificar.py
   ```

2. **Verificar backups**: El sistema crea backups automáticos, pero se recomienda hacer uno manual antes de actualizar.

3. **Datos existentes**: 
   - Los productos con `precio_3` perderán ese precio (se conservan precio_1 y precio_2)
   - Las facturas existentes mantendrán sus datos, pero el campo estado ya no se usa

### 🎨 Mejoras de UI/UX

- Diseño más limpio y minimalista
- Mejor uso del espacio en pantalla
- Colores más consistentes (azul para acciones principales)
- Iconos y botones sin emojis innecesarios
- Mejor feedback visual en todas las acciones

---

**Última actualización**: 2024

