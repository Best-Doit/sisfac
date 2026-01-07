# Flujos Funcionales desde el Código

Este documento describe los principales flujos funcionales del sistema SISFAC y cómo se implementan en el código (rutas, modelos y vistas).

## 1. Gestión de Clientes

### 1.1. Crear Cliente
1. Usuario navega a `Clientes` → `Nuevo Cliente`.
2. Vista: `backend/app/templates/clientes/form.html`.
3. Ruta: `clientes.nuevo` (`backend/app/routes/clientes.py`):
   - GET: muestra el formulario vacío.
   - POST:
     - Lee datos del formulario (`nombre`, `ruc_ci`, `direccion`, `telefono`, `email`).
     - Crea instancia de `Cliente` y la guarda (`db.session.add` + `commit`).
     - Lanza mensaje `flash('Cliente creado correctamente', 'success')`.
     - Redirige al listado de clientes.

### 1.2. Editar Cliente
1. Desde el listado de clientes, el usuario selecciona “Editar”.
2. Ruta: `clientes.editar(id)`:
   - GET:
     - Busca el cliente por `id` o devuelve 404.
     - Renderiza el mismo formulario, pero rellenando los campos con los datos actuales.
   - POST:
     - Actualiza los campos y realiza `commit`.
     - Mensaje flash de éxito y redirección al listado.

### 1.3. Eliminar Cliente
1. En el listado, el usuario pulsa "Eliminar".
2. El formulario usa `onsubmit="return confirmDelete(this, '¿Está seguro de eliminar este cliente?');"`:
   - Se abre el diálogo de confirmación global.
   - Si el usuario confirma, se envía el `POST`.
3. Ruta: `clientes.eliminar(id)`:
   - Si el cliente tiene facturas asociadas (`cliente.facturas`), muestra mensaje de error y no elimina.
   - En caso contrario, marca `cliente.activo = False` y guarda.

### 1.4. Importar Clientes desde Excel
1. Menú `Clientes` → `Importar Excel`.
2. Vista: `clientes/importar.html`:
   - Instrucciones claras sobre el formato requerido.
   - Botón "Descargar Plantilla" que genera un archivo Excel con:
     - Columnas: "Nombre" (obligatorio), "CI" (opcional).
     - Ejemplos de datos incluidos.
   - Formulario para subir archivo `.xlsx`/`.xls`.
   - Nota informativa: Si un cliente ya existe (por nombre o CI), se actualizará.
3. Ruta: `clientes.importar` (POST):
   - Valida que el archivo exista y tenga extensión correcta.
   - Usa `openpyxl` para leer el archivo.
   - Busca la fila de encabezados (busca "nombre" en las primeras 20 filas).
   - Mapea columnas de forma flexible:
     - "Nombre": busca variaciones como "nombre", "nombre de cliente", "producto".
     - "CI": busca "cedula", "ci", "cédula", "ruc", "ruc/ci".
   - Procesa cada fila:
     - Si el cliente existe por CI, lo actualiza.
     - Si no existe por CI pero existe por nombre, lo actualiza.
     - Si no existe, crea un nuevo cliente.
   - Limpia el CI (solo caracteres alfanuméricos) para evitar problemas.
   - Hace `commit` al final.
   - Muestra resumen: cantidad de clientes importados, actualizados y errores (si los hay).

## 2. Gestión de Inventario

### 2.1. Crear/Editar Producto
1. Menú `Inventario` → `Nuevo Producto` o “Editar”.
2. Vista: `inventario/form.html`.
3. Ruta: `inventario.nuevo` / `inventario.editar(id)`:
   - Manejan campos de producto:
     - Código, nombre, descripción, precio principal, precios alternativos, stock y categoría.
   - A la creación:
     - Se guarda un nuevo `Producto`.
   - A la edición:
     - Se actualiza el producto existente.

### 2.2. Eliminar Producto
1. En el listado (`inventario/list.html`), el usuario pulsa “Eliminar”.
2. Formulario con `onsubmit="return confirmDelete(this, '¿Está seguro de eliminar este producto?');"`.
3. Ruta: `inventario.eliminar(id)`:
   - Si el producto tiene `detalles` (facturas asociadas), muestra mensaje de error.
   - En caso contrario, marca `activo = False`.

### 2.3. Importar Productos desde Excel
1. Menú `Inventario` → `Importar Excel`.
2. Vista: `inventario/importar.html`:
   - Instrucciones sobre el formato requerido.
   - Botón "Descargar Plantilla" que genera un archivo Excel con:
     - Columnas: Nombre de Producto, Código, Precio de Compra, Precio de Venta 1, Precio de Venta 2, Saldo para Facturar, Cantidad Facturada.
     - Ejemplos de datos incluidos.
   - Formulario para subir archivo `.xlsx`/`.xls`.
3. Ruta: `inventario.importar` (POST):
   - Valida que el archivo exista y tenga la extensión correcta.
   - Usa `openpyxl` para abrir el libro y localizar columnas de forma flexible:
     - **Nombre**: busca "nombre", "nombre de producto", "producto".
     - **Código**: busca "codigo", "código".
     - **Precio de Compra**: busca "precio de compra", "precio compra".
     - **Precio de Venta 1**: busca "precio de venta 1", "precio venta 1", "p1", "precio 1".
     - **Precio de Venta 2**: busca "precio de venta 2", "precio venta 2", "p2", "precio 2".
     - **Stock**: prioriza "saldo para facturar" sobre "cantidad" o "stock".
     - **Cantidad Facturada**: busca "cantidad facturada".
     - Nota: Se eliminó el soporte para P3 (precio_3).
   - Recorre filas:
     - Si existe un producto con ese código, lo actualiza.
     - Si no existe, crea uno nuevo.
     - Asigna precios: si hay precio_1 o precio_2, los usa; si no, usa precio_unitario.
   - Hace `commit` al final.
   - Muestra un resumen de productos creados/actualizados y posibles errores.

### 2.4. Descargar Plantilla de Importación
1. Menú `Inventario` → `Plantilla Excel` o desde la página de importar.
2. Ruta: `inventario.descargar_plantilla`:
   - Genera un archivo Excel con `openpyxl`.
   - Incluye encabezados formateados (fondo azul, texto blanco, centrado).
   - Columnas: Nombre de Producto, Código, Precio de Compra, Precio de Venta 1, Precio de Venta 2, Saldo para Facturar, Cantidad Facturada.
   - Incluye 3 filas de ejemplo.
   - Ajusta el ancho de las columnas automáticamente.
   - Descarga el archivo como `plantilla_importacion_productos.xlsx`.

## 3. Facturación

### 3.1. Flujo Clásico (`/facturas/nueva`)

1. Menú `Facturas` → `Nueva`.
2. Vista: `facturas/form.html`:
   - Usa Alpine.js (`facturaForm()`) para manejar:
     - Búsqueda y selección de productos (carrito).
     - Paso intermedio con datos de cliente, talonario y fechas.
     - Tabla final con cantidades y precios.
3. Backend: `facturas.nueva` (`routes/facturas.py`):
   - POST:
     - Lee datos del formulario:
       - Cliente, número de factura, fechas, talonario, IVA, notas.
       - Arrays `producto_id[]`, `cantidad[]`, `precio_unitario[]`.
     - Verifica que el número de factura sea único.
     - Crea `Factura` y hace `flush()` para obtener `id`.
     - Recorre cada producto:
       - Convierte cantidad a entero.
       - Crea `DetalleFactura` con cantidad y subtotal (cantidad × precio).
       - Si se marcó `actualizar_stock`, descuenta del `Producto.stock`.
     - Calcula subtotal, IVA y total, actualiza la factura y hace `commit()`.

### 3.2. Flujo Guiado "Facturar" (`/facturar`)

1. Menú lateral `Facturar`.
2. Vista: `facturas/facturar.html`:
   - **Paso 1: Selección de Productos**
     - Lista los productos ordenados por stock (más stock primero).
     - Búsqueda simple por código o nombre (sin sugerencias predictivas).
     - Permite agregar productos al carrito.
     - Panel lateral muestra productos seleccionados con cantidad.
     - Botón "Continuar a Tabla de Factura" solo habilitado si hay productos en el carrito.
   
   - **Paso 2: Tabla de Factura e Información**
     - **Información de Factura** (4 campos en una fila):
       - Número de Factura (obligatorio, puede generarse automáticamente desde talonario)
       - Talonario (opcional)
       - Cliente (obligatorio)
       - Fecha Emisión (obligatorio)
       - Nota: Se eliminaron campos innecesarios (fecha vencimiento, IVA, notas)
     
     - **Tabla de Factura** (optimizada para pantalla completa):
       - Ocupa todo el espacio disponible sin scroll en la pantalla principal.
       - Solo la tabla tiene scroll interno cuando hay muchos productos.
       - Columnas: Código, Descripción, Cantidad, Precio, Subtotal, Stock
       - **Control de Cantidad**:
         - Botones `−` (izquierda) y `+` (derecha) alrededor del input.
         - Input de tipo number sin flechitas (spinners ocultos con CSS).
         - Validación automática: no permite exceder stock disponible.
         - Funciones `incrementarCantidad()` y `decrementarCantidad()` en Alpine.js.
       
       - **Selección de Precio**:
         - Botón dropdown con texto "P1", "P2" o "Principal".
         - Dropdown posicionado con `position: fixed` para evitar cortes por overflow.
         - Opciones: P1 (precio más alto, por defecto), P2, Principal.
         - Muestra el precio seleccionado como texto al lado del botón.
         - Nota: Solo se usan P1 y P2 (se eliminó P3).
       
       - **Totales**: Se calculan automáticamente y se muestran en el footer de la tabla.
     
     - **Botones de Acción** (siempre visibles en la parte inferior):
       - "Volver" (azul): Regresa al paso 1.
       - "Guardar Factura" (verde): Guarda la factura y redirige al detalle.
   
   - Alpine.js (`facturarForm()`):
     - Gestiona el estado de pasos, carrito, tabla y calcula totales reactivos.
     - Usa `window.notify` para avisos de UX (stock insuficiente, etc.).
     - Validación de stock antes de agregar productos al carrito.
     - Cálculo automático de subtotales por fila y total general.

3. Backend: `facturas.facturar`:
   - POST:
     - Lee datos del formulario (cliente, número de factura, talonario, fecha emisión).
     - IVA siempre en 0, notas siempre vacías.
     - Actualización de stock siempre activada.
     - Verifica que el número de factura sea único.
     - Crea `Factura` con estado "PAGADA" por defecto (se eliminó "PENDIENTE").
     - Crea `DetalleFactura` para cada producto.
     - Descuenta stock automáticamente.
     - Calcula totales (subtotal, IVA=0, total).
   - Al finalizar:
     - Redirige a `facturas.detalle` para mostrar la factura creada.

### 3.3. Historial de Facturas

1. Menú lateral `Historial Facturas`.
2. Vista: `facturas/list.html`:
   - Formulario superior de filtros:
     - Búsqueda predictiva por número de factura (con sugerencias).
     - Filtros por rango de fechas (desde/hasta).
   - Tabla con resultados:
     - Columnas: Número Factura, Cliente, Fecha, Total, Acciones.
     - Indicador visual para facturas anuladas (fondo gris, badge "ANULADA").
     - Acciones: "Ver Detalle" y "Anular" (solo si no está anulada).
   - Sin scroll en la pantalla principal, solo la tabla tiene scroll interno si es necesario.
3. Backend: `facturas.listar`:
   - Construye una query sobre `Factura` aplicando los filtros recibidos por querystring.
   - Ordena por `fecha_emision` descendente.

### 3.4. Anular Factura

1. Desde el listado de facturas o el detalle de factura.
2. Vista: Botón "Anular" visible solo si la factura no está anulada.
3. Confirmación: Diálogo de confirmación antes de anular.
4. Backend: `facturas.anular(id)` (`routes/facturas.py`):
   - Verifica que la factura no esté ya anulada.
   - **Revierte el stock**: Para cada detalle de la factura, suma la cantidad al stock del producto.
   - Cambia el estado de la factura a `'ANULADA'`.
   - Guarda los cambios en la base de datos.
   - Muestra mensaje de éxito: "Factura {numero} anulada correctamente. El stock ha sido revertido."
   - Redirige al detalle de la factura.
5. Visualización:
   - Facturas anuladas se muestran con fondo gris y opacidad reducida.
   - Badge rojo "ANULADA" en la lista y en el detalle.
   - El botón "Anular" desaparece una vez anulada la factura.

## 4. Talonarios y Numeración

### 4.1. Gestión de Talonarios

1. Menú `Talonarios`.
2. Vistas:
   - `talonarios/list.html`: tabla de talonarios.
   - `talonarios/form.html`: formulario de alta/edición.
3. Backend: `talonarios.*` (`routes/talonarios.py`):
   - Alta/edición/eliminación (borrado lógico con `activo=False`).

### 4.2. Obtención de Número de Factura

- Lógica principal en `Talonario.obtener_siguiente_numero()` (`models.py`):
  - Busca facturas cuya `numero_factura` coincida con el prefijo del talonario.
  - Extrae la parte numérica y la compara con el rango definido (`numero_inicio` a `numero_fin`).
  - Devuelve el primer número disponible formateado (ej. `FAC-0001`).

> Nota: la asignación exacta de número para una factura concreta puede depender de cómo se combine este método con la UI y validaciones en `facturas.py`.

## 5. Notificaciones y Confirmaciones

### 5.1. Mensajes Flash del Servidor

- Cualquier ruta puede llamar a `flash('mensaje', 'categoria')`.
- En `base.html`, estos mensajes se convierten automáticamente en toasts visuales:
  - Componente Alpine `notificationCenter()`.
  - Auto-cierre a los pocos segundos.
  - Botón de cierre manual.

### 5.2. Notificaciones desde JavaScript

- Función global: `window.notify(message, type)`:
  - `type` puede ser `success`, `error`, `warning` o `info`.
  - Se usa en `facturas/form.html` y `facturas/facturar.html` para avisos de UX (p.ej. “Debes agregar al menos un producto”).

### 5.3. Confirmaciones de Acciones Peligrosas

- Formularios de eliminación (`clientes`, `inventario`, `talonarios`) usan:
  - `onsubmit="return confirmDelete(this, '¿Está seguro de eliminar ...?');"`
- `confirmDelete` está definido en `base.html` como parte de `confirmDialog()`:
  - Abre un modal con mensaje personalizado.
  - Si el usuario confirma, se ejecuta `form.submit()`.
  - Si cancela, simplemente se cierra el modal.

Estos mecanismos permiten al usuario tener feedback visual claro y confirman acciones críticas sin depender de `alert()`/`confirm()` del navegador.

## 6. Optimizaciones de UI/UX

### 6.1. Layout sin Scroll en Pantalla Principal

- **Objetivo**: Eliminar el scroll vertical de la pantalla principal, usando solo scroll interno en contenedores específicos.
- **Implementación**:
  - `base.html`: El `main` tiene `overflow-hidden` en lugar de `overflow-y-auto`.
  - Cada pantalla ajusta su contenido con `max-height: calc(100vh - 200px)` y `overflow-y: auto` solo en contenedores internos (tablas, listas).
  - La tabla de facturación usa flexbox (`flex-1`, `min-h-0`) para ocupar todo el espacio disponible.
- **Pantallas afectadas**:
  - Listado de inventario, clientes, facturas, talonarios: tablas con scroll interno.
  - Dashboard, ajustes, importar: contenedores con scroll interno.
  - Facturación: tabla con scroll interno, botones siempre visibles.

### 6.2. Tabla de Facturación Optimizada

- **Layout**:
  - Ocupa todo el espacio disponible sin desplazar los botones.
  - Usa flexbox vertical: información de factura (flex-shrink-0) → tabla (flex-1) → botones (flex-shrink-0).
  - Altura calculada dinámicamente: `calc(100vh - 100px)` para el contenedor principal.
- **Controles de Cantidad**:
  - Botones `−` (izquierda) y `+` (derecha) alrededor del input.
  - Input de tipo number con spinners ocultos (CSS: `-webkit-appearance: none`, `-moz-appearance: textfield`).
  - Validación automática de stock.
- **Dropdown de Precios**:
  - Posicionado con `position: fixed` para evitar cortes por overflow.
  - Cálculo dinámico de posición (arriba o abajo según espacio disponible).
  - Z-index alto (99999) para aparecer sobre todos los elementos.

### 6.3. Eliminación de Campos Innecesarios

- **Facturación**:
  - Eliminado: fecha de vencimiento, IVA (siempre 0), notas, checkbox "actualizar stock" (siempre activo).
  - Estados: Solo "PAGADA" y "ANULADA" (eliminado "PENDIENTE").
- **Productos**:
  - Eliminado: categoría (campo y referencias en UI y backend).
  - Precios: Solo Principal, P1 y P2 (eliminado P3).
- **Inventario**:
  - Búsqueda simple sin sugerencias predictivas (solo filtrado en la lista).

### 6.4. Mejoras en Búsquedas

- **Búsqueda Predictiva**:
  - Implementada en: clientes, facturas (historial).
  - No implementada en: inventario (búsqueda simple), facturación (búsqueda simple).
- **Implementación**:
  - Endpoints API: `/clientes/api/buscar`, `/facturas/api/buscar`.
  - Frontend: Alpine.js con `@input`, `@focus`, `@blur` para mostrar/ocultar sugerencias.
  - Dropdown de sugerencias con z-index alto y posicionamiento absoluto.

