# Cambios Recientes y Mejoras - SISFAC

**Última actualización**: Febrero 2026  
**Versión**: 5.6.0

Este documento describe los cambios, mejoras y nuevas funcionalidades implementadas recientemente en el sistema SISFAC.

---

## 📋 Tabla de Contenidos

1. [Funcionalidad de Anulación de Facturas](#funcionalidad-de-anulación-de-facturas)
2. [Mejoras en la Tabla de Facturación](#mejoras-en-la-tabla-de-facturación)
3. [Optimizaciones de Layout](#optimizaciones-de-layout)
4. [Importación de Clientes desde Excel](#importación-de-clientes-desde-excel)
5. [Simplificación de Campos](#simplificación-de-campos)
6. [Mejoras en Búsquedas](#mejoras-en-búsquedas)
7. [Sistema de Numeración de Facturas (n+1)](#sistema-de-numeración-de-facturas-n1)
8. [Mejoras de UI/UX Adicionales](#mejoras-de-uiux-adicionales)

---

## 1. Funcionalidad de Anulación de Facturas

### Descripción
Se implementó la capacidad de anular facturas, permitiendo revertir el stock de productos y marcar la factura como anulada.

### Características
- **Reversión automática de stock**: Al anular una factura, todos los productos incluidos en ella recuperan su stock.
- **Validación**: No se puede anular una factura que ya está anulada.
- **Confirmación**: Diálogo de confirmación antes de anular.
- **Indicadores visuales**: Facturas anuladas se muestran con fondo gris, opacidad reducida y badge "ANULADA".

### Implementación
- **Ruta**: `POST /facturas/<id>/anular`
- **Ubicación**: `backend/app/routes/facturas.py`
- **Lógica**:
  1. Verifica que la factura no esté ya anulada.
  2. Para cada detalle de la factura, suma la cantidad al stock del producto.
  3. Cambia el estado de la factura a `'ANULADA'`.
  4. Guarda los cambios y muestra mensaje de éxito.

### Interfaz
- Botón "Anular" visible en:
  - Listado de facturas (solo si no está anulada).
  - Detalle de factura (solo si no está anulada).
- Badge "ANULADA" o "FACTURA ANULADA" en listado y detalle.

---

## 2. Mejoras en la Tabla de Facturación

### 2.1. Control de Cantidad Mejorado

**Antes**: Input de tipo number con flechitas arriba/abajo.  
**Ahora**: Botones `−` (izquierda) y `+` (derecha) alrededor del input.

#### Características
- Botones con estilo consistente (gris con hover).
- Input sin flechitas (spinners ocultos con CSS).
- Validación automática: no permite exceder stock disponible.
- Funciones `incrementarCantidad()` y `decrementarCantidad()` en Alpine.js.

#### Implementación CSS
```css
/* En base.html */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
input[type="number"] {
    -moz-appearance: textfield;
}
```

### 2.2. Dropdown de Precios Mejorado

**Problema anterior**: El dropdown se cortaba cuando estaba dentro de un contenedor con `overflow-auto`.  
**Solución**: Posicionamiento con `position: fixed` y cálculo dinámico de posición.

#### Características
- Posicionado relativo al viewport, no al contenedor.
- Cálculo automático: se muestra arriba o abajo según el espacio disponible.
- Z-index alto (99999) para aparecer sobre todos los elementos.
- Opciones: P1 (por defecto, precio más alto), P2, Principal.

#### Implementación
- Alpine.js con función `positionDropdown()` que calcula la posición del botón.
- Usa `getBoundingClientRect()` para obtener coordenadas.
- Verifica espacio disponible arriba y abajo.

### 2.3. Layout Optimizado

- **Estructura flexbox vertical**:
  - Información de factura: `flex-shrink-0` (altura fija).
  - Tabla: `flex-1` (ocupa espacio restante).
  - Botones: `flex-shrink-0` (siempre visibles).
- **Altura dinámica**: `calc(100vh - 100px)` para el contenedor principal.
- **Scroll interno**: Solo la tabla tiene scroll cuando hay muchos productos.
- **Espaciado optimizado**: Reducción de paddings y márgenes para maximizar espacio.

---

## 3. Optimizaciones de Layout

### 3.1. Eliminación de Scroll en Pantalla Principal

**Objetivo**: Eliminar el scroll vertical de la pantalla principal, usando solo scroll interno en contenedores específicos.

#### Cambios en `base.html`
- `main` cambió de `overflow-y-auto` a `overflow-hidden`.
- Cada pantalla ajusta su contenido con scroll interno.

#### Pantallas Afectadas
- **Listados** (inventario, clientes, facturas, talonarios):
  - Tablas con `max-height: calc(100vh - 280px)` y `overflow-y: auto`.
- **Dashboard, Ajustes, Importar**:
  - Contenedores con `max-height: calc(100vh - 200px)` y `overflow-y: auto`.
- **Facturación**:
  - Tabla con scroll interno, botones siempre visibles.

### 3.2. Espaciado Optimizado

- Reducción de paddings: `p-3 md:p-6` → `p-2 md:p-3`.
- Reducción de márgenes: `mb-6` → `mb-3`, `mb-4` → `mb-2`.
- Tamaños de texto: `text-xl` → `text-lg`, `text-sm` → `text-xs` en labels.
- Gaps reducidos: `gap-4` → `gap-2`.

---

## 4. Importación de Clientes desde Excel

### Descripción
Nueva funcionalidad para importar clientes masivamente desde archivos Excel, similar a la importación de productos.

### Características
- **Plantilla descargable**: Botón "Descargar Plantilla" genera un Excel con formato correcto.
- **Columnas requeridas**:
  - **Nombre** (obligatorio): Nombre completo del cliente.
  - **CI** (opcional): Número de cédula de identidad.
- **Detección flexible**: Reconoce variaciones como "Cédula", "Cédula de Identidad", "RUC", "RUC/CI".
- **Actualización inteligente**: Si un cliente ya existe (por nombre o CI), se actualiza en lugar de crear duplicado.

### Implementación
- **Ruta**: `GET /clientes/importar` (formulario), `POST /clientes/importar` (procesar).
- **Ruta de plantilla**: `GET /clientes/descargar-plantilla`.
- **Ubicación**: `backend/app/routes/clientes.py`.
- **Lógica**:
  1. Busca la fila de encabezados (primeras 20 filas).
  2. Mapea columnas de forma flexible.
  3. Procesa cada fila:
     - Busca cliente existente por CI primero, luego por nombre.
     - Si existe, actualiza; si no, crea nuevo.
  4. Limpia el CI (solo caracteres alfanuméricos).
  5. Muestra resumen de importados, actualizados y errores.

### Interfaz
- Página dedicada: `clientes/importar.html`.
- Instrucciones claras y ejemplo de formato.
- Botón para descargar plantilla.
- Formulario de carga de archivo.

---

## 5. Simplificación de Campos

### 5.1. Facturación

#### Campos Eliminados
- ❌ Fecha de vencimiento
- ❌ IVA (siempre 0, no se muestra)
- ❌ Notas/observaciones
- ❌ Checkbox "Actualizar stock" (siempre activo)

#### Estados Simplificados
- **Antes**: PENDIENTE, PAGADA, ANULADA
- **Ahora**: PAGADA, ANULADA
- **Razón**: Las facturas son físicas y el pago es instantáneo, no hay estado pendiente.

### 5.2. Productos

#### Campos Eliminados
- ❌ Categoría (campo y todas las referencias en UI y backend)

#### Sistema de Precios Unificado
- **Antes**: Precio Principal, P1, P2, P3 (4 niveles)
- **Ahora**: Solo P1 y P2 (P1 es el principal y más alto)
- **Cambios implementados**:
  - P1 es obligatorio y debe ser el precio más alto
  - P2 es opcional y debe ser menor o igual que P1
  - Validación: P2 no puede ser mayor que P1
  - Por defecto se usa P1 en todas las operaciones
  - En formularios: solo campos P1 (obligatorio) y P2 (opcional)
  - En tabla de inventario: solo se muestra P1
  - En facturación: dropdown con P1 (por defecto) y P2
- **Compatibilidad**: `precio_unitario` se mantiene igual a P1 para compatibilidad con datos existentes

### 5.3. Interfaz de Facturación

#### Layout de Información
- **Antes**: Campos distribuidos en múltiples filas.
- **Ahora**: 4 campos en una sola fila:
  1. Número de Factura
  2. Talonario
  3. Cliente
  4. Fecha Emisión

---

## 6. Mejoras en Búsquedas

### 6.1. Búsqueda Predictiva Automática (Sin Ventanas Emergentes)

**Cambio importante**: Se eliminaron las ventanas emergentes (dropdowns) de búsqueda predictiva y se implementó filtrado automático directo en las tablas.

#### Implementación Actual
- ✅ **Clientes**: Filtrado automático mientras escribes (por nombre o CI).
- ✅ **Inventario**: Filtrado automático mientras escribes (por código o nombre).
- ✅ **Facturas (Historial)**: Búsqueda con sugerencias por número de factura (mantiene dropdown).

#### Características
- **Sin necesidad de clic**: La tabla se filtra automáticamente mientras escribes.
- **Sin ventanas emergentes**: No hay dropdowns que se superpongan.
- **Filtrado instantáneo**: Oculta/muestra filas en tiempo real.
- **Mensaje de "No resultados"**: Se muestra automáticamente cuando no hay coincidencias.

#### Implementación Técnica
- JavaScript vanilla con `addEventListener('input')`.
- Filtrado del lado del cliente usando atributos `data-*` en las filas.
- Comparación case-insensitive (sin distinción de mayúsculas/minúsculas).
- Sin llamadas al servidor durante la búsqueda.

### 6.2. Endpoints API (Mantenidos para Facturas)

- `/facturas/api/buscar?q=<termino>`: Retorna hasta 10 facturas que coincidan (solo para historial de facturas).

---

## 7. Sistema de Numeración de Facturas (n+1)

### Descripción
Mejora en el sistema de generación automática de números de factura desde talonarios.

### Características
- **Sugerencia sin incrementar**: Al cargar la página, se sugiere el siguiente número sin incrementarlo.
- **Incremento al crear**: El número solo se incrementa cuando realmente se crea la factura.
- **Actualización dinámica**: Al cambiar el talonario, el número sugerido se actualiza automáticamente.
- **Validación**: No permite crear facturas si el talonario ha alcanzado su límite.

### Implementación
- **Método nuevo**: `Talonario.sugerir_siguiente_numero()` - Solo muestra el número sin incrementarlo.
- **Método existente**: `Talonario.obtener_siguiente_numero()` - Incrementa el contador al crear factura.
- **Frontend**: Función `actualizarNumeroFactura()` en Alpine.js que actualiza el número al cambiar talonario.

### Archivos Modificados
- `backend/app/models.py`: Agregado método `sugerir_siguiente_numero()`.
- `backend/app/routes/facturas.py`: Lógica para sugerir número sin incrementar.
- `backend/app/templates/facturas/facturar.html`: Actualización dinámica del número de factura.

---

## 8. Mejoras de UI/UX Adicionales

### 8.1. Botón de Redes Sociales
- **Agregado**: Botón "Sígueme en TikTok" en el sidebar.
- **Ubicación**: Parte inferior del sidebar, antes del footer.
- **Diseño**: Gradiente rosa-púrpura característico de TikTok.
- **Funcionalidad**: Enlace externo que se abre en nueva pestaña.
- **Responsive**: Se adapta al estado colapsado del sidebar.

### 8.2. Corrección del Footer
- **Problema**: Footer se desplazaba incorrectamente.
- **Solución**: Ajustes en flexbox con `flex-shrink-0`, `min-h-0` y `mt-auto`.
- **Resultado**: Footer siempre visible en la parte inferior sin desplazarse.

### 8.3. Simplificación de Tabla de Inventario
- **Antes**: Mostraba "P1: Bs. XX.XX" y "P2: Bs. XX.XX" (si existía).
- **Ahora**: Solo muestra "Bs. XX.XX" (precio P1).
- **Razón**: Simplificar la visualización, ya que P1 es el precio principal.

### 8.4. Corrección de Agregar Productos al Carrito
- **Problema**: Error al agregar productos cuando `precio_2` era `None`.
- **Solución**: Manejo correcto de valores `null` y validación de tipos.
- **Resultado**: Los productos se agregan correctamente independientemente de tener P2 o no.

---

## 📝 Notas Técnicas

### Archivos Modificados Recientemente

#### Backend
- `backend/app/routes/facturas.py`: 
  - Ruta de anulación, eliminación de campos innecesarios.
  - Lógica mejorada para sugerir número de factura sin incrementar.
- `backend/app/routes/clientes.py`: Importación desde Excel.
- `backend/app/routes/inventario.py`: 
  - Mejoras en importación, eliminación de categoría.
  - Validación de que P1 ≥ P2.
  - Exportación actualizada (solo P1 y P2).
- `backend/app/models.py`: 
  - Eliminación de campo categoría, ajustes en estados.
  - Método `sugerir_siguiente_numero()` en Talonario.

#### Frontend
- `backend/app/templates/facturas/facturar.html`: 
  - Mejoras en tabla, controles, layout.
  - Corrección de función `agregarAlCarrito()`.
  - Actualización dinámica de número de factura.
- `backend/app/templates/facturas/list.html`: Botón de anular, indicadores visuales.
- `backend/app/templates/facturas/detalle.html`: Botón de anular, badge de estado.
- `backend/app/templates/base.html`: 
  - Estilos para ocultar spinners, overflow-hidden.
  - Botón de TikTok en sidebar.
  - Corrección del footer.
- `backend/app/templates/clientes/list.html`: 
  - Búsqueda predictiva automática (sin dropdown).
  - Filtrado directo en tabla.
- `backend/app/templates/clientes/importar.html`: Nueva página de importación.
- `backend/app/templates/inventario/list.html`: 
  - Búsqueda predictiva automática (sin dropdown).
  - Solo muestra precio P1 en tabla.
- `backend/app/templates/inventario/form.html`: 
  - Solo campos P1 (obligatorio) y P2 (opcional).
  - Validación de que P1 ≥ P2.
- `backend/app/templates/inventario/importar.html`: 
  - Instrucciones actualizadas para P1 y P2.
  - Ejemplo de tabla actualizado.

### Consideraciones de Compatibilidad

- Las facturas existentes con estado "PENDIENTE" seguirán funcionando, pero no se pueden crear nuevas.
- Los productos con `precio_unitario` seguirán funcionando, pero el sistema ahora usa `precio_1` como principal.
- Los productos con `precio_3` seguirán funcionando, pero no se mostrará en la UI (se recomienda migrar a P1/P2).
- Los productos con categoría seguirán funcionando, pero el campo no se mostrará en la UI.
- Al importar productos desde Excel, si solo se proporciona un precio, se asignará a P1.

---

## 🔄 Próximas Mejoras Sugeridas

- [ ] Exportación de facturas a PDF.
- [ ] Reportes de ventas por período.
- [ ] Búsqueda avanzada con múltiples filtros.
- [ ] Historial de cambios en productos y clientes.
- [ ] Notificaciones de stock bajo más visibles.

---

**Documentación relacionada**:
- [Flujos Funcionales](./guia_desarrollo/flujos.md)
- [PRD - Requisitos del Producto](./PRD_SISFAC.md)
- [Arquitectura Técnica](./ARQUITECTURA_TECNICA.md)
