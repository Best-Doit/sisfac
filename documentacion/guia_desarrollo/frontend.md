# Frontend - Templates, Layout y Componentes

La interfaz de SISFAC está basada en templates Jinja2 renderizados por Flask, Tailwind CSS para estilos y Alpine.js para la interactividad.

## 1. Layout Principal

- Archivo: `backend/app/templates/base.html`

Responsabilidades:
- Estructura básica HTML (`<head>`, `<body>`).
- Carga de Tailwind vía CDN.
- Carga de Alpine.js vía CDN.
- Sidebar lateral con navegación:
  - Dashboard
  - Clientes
  - Inventario
  - Facturar
  - Historial de facturas
  - Talonarios
- Barra superior para vista móvil (botón de menú).
- Contenedor `<main>` donde se inyectan los bloques `{% block content %}` de cada vista.

Componentes JS relevantes:
- Estado de sidebar:
  - Usa `x-data` en `<body>` para controlar colapso/expansión y almacenamiento en `localStorage`.
- Sistema global de notificaciones (toasts):
  - Definido como función `notificationCenter()` en un `<script>` del `<head>`.
  - Se instancia al final del `<body>`:
    ```html
    <div x-data="notificationCenter()" 
         x-init='init({{ get_flashed_messages(with_categories=true)|tojson|safe }})'>
      ...
    </div>
    ```
  - Integra con Flask `flash()` y expone `window.notify(message, type)` para lanzar toasts desde cualquier JS.
- Diálogo global de confirmación:
  - Definido como función `confirmDialog()` en el `<head>`.
  - Se instancia al final del `<body>` con un modal estilizado (overlay + tarjetas Tailwind).
  - Expone:
    - `window.openConfirmModal(message, onConfirm)`
    - `window.confirmDelete(form, message)` → usado en formularios de “Eliminar”.

## 2. Dashboard

- Archivo: `backend/app/templates/index.html`
- Extiende `base.html`.
- Muestra tarjetas con métricas (`stats` calculadas en `routes/main.py`):
  - Total de clientes, productos, facturas, facturas pendientes y productos con stock bajo.
- Incluye sección de “Acciones rápidas” con botones:
  - Nuevo Cliente, Nuevo Producto, Nueva Factura.

## 3. Módulo de Clientes

### 3.1. Listado
- Archivo: `backend/app/templates/clientes/list.html`
- Tabla con:
  - ID, nombre, RUC/CI, teléfono, email.
- Acciones:
  - Historial de facturas del cliente.
  - Editar.
  - Eliminar (formulario con `onsubmit="return confirmDelete(this, '...')"` para usar el modal global).

### 3.2. Formulario
- Archivo: `backend/app/templates/clientes/form.html`
- Formulario simple (sin Alpine intensivo) para alta/edición de clientes.
- Reutiliza el mismo template para crear y editar (si se pasa `cliente` en el contexto).

### 3.3. Historial
- Archivo: `backend/app/templates/clientes/historial.html`
- Muestra datos básicos del cliente y el listado de sus facturas.

## 4. Módulo de Inventario

### 4.1. Listado
- Archivo: `backend/app/templates/inventario/list.html`
- Tabla con:
  - Código, nombre, precios (principal y opcionales P1-P3), stock y categoría.
- Destaca productos con stock bajo (colores rojos).
- Acciones:
  - Editar.
  - Eliminar (usa `confirmDelete` para el modal de confirmación).

### 4.2. Formulario
- Archivo: `backend/app/templates/inventario/form.html`
- Formulario para crear/editar productos.
- Maneja:
  - Código, nombre, descripción, precio principal y precios alternativos, stock, categoría.

### 4.3. Importar Excel
- Archivo: `backend/app/templates/inventario/importar.html`
- Formulario para subir un archivo Excel (integrado con la ruta `inventario.importar`).
- Explica formato esperado (columnas como Nombre/Producto, Código, Precio, Stock, etc.).

## 5. Módulo de Facturación

### 5.1. Listado
- Archivo: `backend/app/templates/facturas/list.html`
- Tabla con facturas:
  - Número, cliente, fecha, total, estado.
- Filtros (en el formulario superior):
  - Texto (número).
  - Estado.
  - Fechas desde/hasta.
- Enlaces al detalle de cada factura.

### 5.2. Formulario clásico (`/facturas/nueva`)
- Archivo: `backend/app/templates/facturas/form.html`
- Flujo por pasos, usando Alpine.js:
  - Selección de productos (similar a un carrito).
  - Captura de datos de factura (cliente, talonario, fechas, IVA, stock).
  - Tabla final con productos, cantidades, precios y totales.
- Funciones JS (dentro de `facturaForm()`):
  - `filtrarProducto(...)`: filtro en vivo por código/nombre.
  - `agregarAlCarrito(...)`: añade producto al carrito (usa `window.notify` si el producto ya está).
  - `eliminarDelCarrito(index)`: quita un producto.
  - `irATablaFactura()`: copia los ítems del carrito a la tabla de factura (valida que haya al menos uno; si no, `window.notify`).
  - `actualizarPrecio(index)`, `calcularFila(index)`, getters `subtotal`, `ivaMonto`, `total`.

### 5.3. Flujo guiado “Facturar” (`/facturar`)
- Archivo: `backend/app/templates/facturas/facturar.html`
- Interfaz más avanzada y amigable:
  - Paso 1: Selección de productos (lista ordenada por stock, con buscador).
  - Paso 2: Datos de cliente/talonario/fechas/IVA y tabla de factura.
- Usa un componente Alpine `facturarForm()`:
  - Maneja el estado de pasos (`paso`), búsqueda, carrito y tabla.
  - En `irATablaFactura()` valida que el carrito no esté vacío y muestra notificación en caso contrario.
  - Actualiza totales en tiempo real.

### 5.4. Detalle de factura
- Archivo: `backend/app/templates/facturas/detalle.html`
- Muestra:
  - Datos del cliente y de la factura (número, fechas, estado, notas).
  - Tabla con los productos, cantidades, precios y subtotales.
  - Totales de factura (subtotal, IVA, total).

## 6. Módulo de Talonarios

### 6.1. Listado
- Archivo: `backend/app/templates/talonarios/list.html`
- Tabla con:
  - Nombre, prefijo, rango, total de facturas posibles.
- Acción:
  - Editar.
  - Eliminar (usa `confirmDelete`).

### 6.2. Formulario
- Archivo: `backend/app/templates/talonarios/form.html`
- Formulario para alta/edición de talonarios:
  - Nombre, prefijo, número de inicio, número de fin.

## 7. Estilos y Responsividad

- Tailwind CSS se usa en todo el proyecto:
  - Clases utilitarias para tipografía, colores, spacing, grid/flex, etc.
  - Layout responsive con `grid`, `flex`, breakpoints `md`, `lg`, etc.
- El diseño está pensado para:
  - Usarse en escritorio a pantalla completa (vía Electron) o en navegador.
  - Verse correctamente en pantallas pequeñas gracias a la barra superior móvil y sidebar ocultable.

