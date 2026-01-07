# Backend (Flask) - Estructura y Módulos

Este documento describe la estructura del backend, los módulos principales y sus responsabilidades.

## 1. App Factory y Configuración

- `backend/app/__init__.py`
  - `db = SQLAlchemy()`: instancia global del ORM.
  - `create_app()`: función factory que:
    - Crea la instancia de `Flask`.
    - Configura `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI` (SQLite `sisfac.db`) y desactiva `SQLALCHEMY_TRACK_MODIFICATIONS`.
    - Inicializa la base de datos (`db.init_app(app)`).
    - Registra los blueprints:
      - `main` (dashboard)
      - `clientes`
      - `inventario`
      - `facturas`
      - `talonarios`
    - Expone una ruta directa `/facturar` que delega en `facturas.facturar`.
    - Ejecuta `db.create_all()` al arrancar (útil en desarrollo).

- `backend/run.py`
  - Crea la app con `create_app()` y la arranca en modo desarrollo (`debug=True`).

## 2. Modelos de Datos

- Archivo: `backend/app/models.py`

### 2.1. `Cliente`
- Tabla: `clientes`
- Campos principales:
  - `id`, `nombre`, `ruc_ci`, `direccion`, `telefono`, `email`
  - `fecha_registro` (alta) y `activo` (borrado lógico)
- Relaciones:
  - `facturas`: relación 1-N con `Factura`.
- Métodos:
  - `to_dict()`: serialización básica para APIs/búsquedas.

### 2.2. `Producto`
- Tabla: `productos`
- Campos principales:
  - `id`, `codigo` (único), `nombre`, `descripcion`
  - `precio_unitario` (precio principal)
  - `precio_1`, `precio_2`, `precio_3` (niveles de precio opcionales)
  - `stock`, `categoria`, `fecha_registro`, `activo`
- Métodos:
  - `to_dict()`: para APIs/autocompletado.
  - `obtener_precio(nivel=1)`: devuelve el precio según nivel 1/2/3 o el principal.

### 2.3. `Factura`
- Tabla: `facturas`
- Campos:
  - `id`, `numero_factura` (único)
  - `cliente_id` (FK a `Cliente`), `talonario_id` (FK a `Talonario`)
  - `fecha_emision`, `fecha_vencimiento`
  - `subtotal`, `iva`, `total`
  - `estado` (ej. `PENDIENTE`), `notas`
  - `fecha_creacion`, `fecha_edicion`
- Relaciones:
  - `detalles`: lista de `DetalleFactura` (cascade `all, delete-orphan`).
  - `talonario`: referencia al `Talonario` asociado.
- Métodos:
  - `to_dict()`: vista resumida de la factura (datos de cliente y montos).

### 2.4. `DetalleFactura`
- Tabla: `detalle_factura`
- Campos:
  - `id`, `factura_id`, `producto_id`
  - `cantidad` (entera), `precio_unitario`, `subtotal`
- Relaciones:
  - `producto`: referencia a `Producto` (backref `detalles`).
- Métodos:
  - `to_dict()`: datos útiles para vistas/API (nombre, código, cantidad, precios).

### 2.5. `Talonario`
- Tabla: `talonarios`
- Campos:
  - `id`, `nombre`
  - `numero_inicio`, `numero_fin`
  - `prefijo` (ej. `FAC`)
  - `activo`, `fecha_creacion`
- Métodos:
  - `to_dict()`: serialización básica.
  - `obtener_siguiente_numero()`: calcula el siguiente número disponible dentro del rango, según facturas existentes (prefijo + rango).

## 3. Rutas (Blueprints)

Todas se encuentran en `backend/app/routes/`.

### 3.1. `main.py` (Dashboard)
- Blueprint: `main`, ruta base `/`.
- Vista:
  - `index()`: calcula estadísticas:
    - `total_clientes` activos.
    - `total_productos` activos.
    - `total_facturas`.
    - `facturas_pendientes`.
    - `productos_stock_bajo` (stock < 10).
  - Renderiza `templates/index.html`.

### 3.2. `clientes.py`
- Blueprint: `clientes`, prefijo `/clientes`.

Funciones principales:
- `listar()` (`GET /clientes/`):
  - Filtros por texto (`q`) en nombre, RUC/CI y teléfono.
  - Muestra tabla con clientes activos.
- `nuevo()` (`GET/POST /clientes/nuevo`):
  - GET: muestra formulario de alta.
  - POST: crea un nuevo `Cliente`, guarda y redirige al listado.
- `editar(id)` (`GET/POST /clientes/<id>/editar`):
  - GET: carga datos del cliente y muestra formulario.
  - POST: actualiza campos básicos y guarda.
- `eliminar(id)` (`POST /clientes/<id>/eliminar`):
  - Si el cliente tiene facturas asociadas, no lo elimina (muestra mensaje).
  - En caso contrario, marca `activo=False`.
- `historial(id)` (`GET /clientes/<id>/historial`):
  - Lista facturas asociadas a un cliente en orden descendente por fecha.
- `api_buscar()` (`GET /clientes/api/buscar`):
  - Devuelve un JSON con clientes activos filtrados por nombre (para autocompletado).

### 3.3. `inventario.py`
- Blueprint: `inventario`, prefijo `/inventario`.

Funciones principales:
- `listar()` (`GET /inventario/`):
  - Filtros por texto (`q`) y categoría.
  - Muestra productos activos, resaltando stock bajo.
- `nuevo()` (`GET/POST /inventario/nuevo`):
  - Alta de nuevos productos con múltiples precios y stock inicial.
- `editar(id)` (`GET/POST /inventario/<id>/editar`):
  - Edición de datos de producto (precios, stock, categoría, descripción).
- `eliminar(id)` (`POST /inventario/<id>/eliminar`):
  - Si el producto tiene detalles de factura, no permite eliminar (solo marcar inactivo).
- `api_buscar()` (`GET /inventario/api/buscar`):
  - Búsqueda rápida de productos por nombre/código.
- `api_stock(id)` (`GET /inventario/api/<id>/stock`):
  - Devuelve JSON con stock disponible y si es considerado “bajo”.
- `importar()` (`GET/POST /inventario/importar`):
  - GET: muestra formulario para subir archivo Excel.
  - POST:
    - Valida el archivo (extensión `.xlsx`/`.xls`).
    - Lo guarda temporalmente.
    - Usa `openpyxl` para leer columnas (nombre, código, precio, stock, categoría, descripción).
    - Crea o actualiza productos según código/nombre.
    - Muestra resumen de productos creados/actualizados y posibles errores.

### 3.4. `facturas.py`
- Blueprint: `facturas`, prefijo `/facturas`.

Funciones principales:
- `listar()` (`GET /facturas/`):
  - Filtros por texto (`q` en número), `estado`, `fecha_desde`, `fecha_hasta`.
  - Lista facturas ordenadas por fecha de emisión.

- `nueva()` (`GET/POST /facturas/nueva`):
  - Flujo clásico para crear facturas con formulario en pasos.
  - POST:
    - Recibe datos de cliente, talonario, fechas, IVA, notas y bandera `actualizar_stock`.
    - Valida que el número de factura no exista.
    - Crea `Factura`, luego detalles (`DetalleFactura`) y opcionalmente actualiza `Producto.stock`.
    - Calcula `subtotal`, `iva` y `total`.

- `facturar()` (`GET/POST /facturas/facturar`):
  - Flujo guiado “rápido” usando un carrito de productos (Alpine.js).
  - GET:
    - Envía productos (ordenados por stock) y clientes/talonarios a la vista `facturas/facturar.html`.
  - POST:
    - Misma lógica general que `nueva()`, pero los productos se cargan desde el carrito (arrays `producto_id[]`, `cantidad[]`, `precio_unitario[]`).
    - Las cantidades se tratan como enteros, coherentes con el stock.

- `api_productos()` (`GET /facturas/api/productos`):
  - Devuelve JSON de productos activos, usado para autocompletado o selección de productos en facturación.

> Nota: en el html hay vistas complementarias (`list.html`, `form.html`, `facturar.html`, `detalle.html`) que se explican en `frontend.md`.

### 3.5. `talonarios.py`
- Blueprint: `talonarios`, prefijo `/talonarios`.

Funciones principales:
- `listar()` (`GET /talonarios/`):
  - Muestra todos los talonarios activos.
- `nuevo()` (`GET/POST /talonarios/nuevo`):
  - Alta de talonario: nombre, rango (inicio/fin) y prefijo.
- `editar(id)` (`GET/POST /talonarios/<id>/editar`):
  - Modificación de datos básicos y rango.
- `eliminar(id)` (`POST /talonarios/<id>/eliminar`):
  - Marca el talonario como inactivo (`activo=False`).

## 4. Flujos Técnicos Clave

Los flujos detallados (crear factura, importar productos, gestionar stock, etc.) están desarrollados con más detalle en `flujos.md`.

