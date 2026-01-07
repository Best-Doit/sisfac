# Diseño de API - SISFAC

## Documento de Especificación de APIs

**Versión:** 1.0  
**Fecha:** 2024  
**Autor:** Equipo de Desarrollo

---

## Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Convenciones de API](#convenciones-de-api)
3. [Autenticación y Autorización](#autenticación-y-autorización)
4. [Formato de Respuestas](#formato-de-respuestas)
5. [Manejo de Errores](#manejo-de-errores)
6. [Endpoints de Clientes](#endpoints-de-clientes)
7. [Endpoints de Productos](#endpoints-de-productos)
8. [Endpoints de Facturas](#endpoints-de-facturas)
9. [Endpoints de Dashboard](#endpoints-de-dashboard)
10. [Ejemplos de Uso](#ejemplos-de-uso)

---

## 1. Visión General

SISFAC utiliza dos tipos de APIs:

1. **Flask Routes**: Para server-side rendering (SSR)
   - Retornan HTML renderizado
   - Formularios tradicionales
   - Redirecciones

2. **FastAPI REST API**: Para operaciones AJAX
   - Retornan JSON
   - Operaciones asíncronas
   - Documentación automática (OpenAPI)

Este documento se enfoca en la **API REST de FastAPI**.

### Base URL

- **Desarrollo**: `http://localhost:5000/api/v1`
- **Producción**: `http://localhost:5000/api/v1` (interno)

### Versión

- Versión actual: `v1`
- Todas las URLs incluyen `/api/v1`

---

## 2. Convenciones de API

### 2.1 Métodos HTTP

- **GET**: Obtener recursos
- **POST**: Crear nuevos recursos
- **PUT**: Actualizar recursos completos
- **PATCH**: Actualizar recursos parciales
- **DELETE**: Eliminar recursos

### 2.2 Códigos de Estado HTTP

- **200 OK**: Operación exitosa
- **201 Created**: Recurso creado exitosamente
- **400 Bad Request**: Solicitud inválida
- **404 Not Found**: Recurso no encontrado
- **422 Unprocessable Entity**: Error de validación
- **500 Internal Server Error**: Error del servidor

### 2.3 Naming Conventions

- URLs en minúsculas
- Separación con guiones: `/api/v1/productos`
- Plural para colecciones: `/clientes`, `/productos`
- Singular para recursos específicos: `/clientes/{id}`

### 2.4 Paginación

Para endpoints que retornan listas:

```
GET /api/v1/clientes?page=1&limit=20
```

**Parámetros:**
- `page`: Número de página (default: 1)
- `limit`: Elementos por página (default: 20, max: 100)

**Respuesta:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

### 2.5 Filtrado y Búsqueda

**Búsqueda:**
```
GET /api/v1/clientes?q=nombre
```

**Filtros:**
```
GET /api/v1/facturas?estado=PENDIENTE&fecha_desde=2024-01-01
```

---

## 3. Autenticación y Autorización

### 3.1 Estado Actual (Fase 1)

- **Sin autenticación**: Aplicación de escritorio local
- Todos los endpoints son accesibles
- No hay usuarios múltiples

### 3.2 Futuro (Si se requiere)

- API Keys para integraciones
- JWT tokens para autenticación
- Roles y permisos

---

## 4. Formato de Respuestas

### 4.1 Respuesta Exitosa - Recurso Único

```json
{
  "success": true,
  "data": {
    "id": 1,
    "nombre": "Juan Pérez",
    "ruc_ci": "12345678",
    "direccion": "Calle Principal 123",
    "telefono": "0987654321",
    "email": "juan@example.com",
    "fecha_registro": "2024-01-15T10:30:00"
  }
}
```

### 4.2 Respuesta Exitosa - Lista

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "Juan Pérez",
      ...
    },
    {
      "id": 2,
      "nombre": "María García",
      ...
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  }
}
```

### 4.3 Respuesta de Error

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Error de validación",
    "details": {
      "nombre": ["Este campo es requerido"],
      "email": ["Formato de email inválido"]
    }
  }
}
```

---

## 5. Manejo de Errores

### 5.1 Códigos de Error

- **VALIDATION_ERROR**: Error de validación de datos
- **NOT_FOUND**: Recurso no encontrado
- **BUSINESS_RULE_VIOLATION**: Violación de regla de negocio
- **INSUFFICIENT_STOCK**: Stock insuficiente
- **DUPLICATE_ENTRY**: Entrada duplicada
- **INTERNAL_ERROR**: Error interno del servidor

### 5.2 Ejemplos de Errores

**400 Bad Request - Validación:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Datos inválidos",
    "details": {
      "precio_unitario": ["Debe ser mayor a 0"]
    }
  }
}
```

**404 Not Found:**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Cliente no encontrado"
  }
}
```

**422 Unprocessable Entity - Regla de Negocio:**
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "Stock insuficiente para el producto 'Laptop'",
    "details": {
      "producto_id": 5,
      "stock_disponible": 3,
      "cantidad_solicitada": 5
    }
  }
}
```

---

## 6. Endpoints de Clientes

### 6.1 Listar Clientes

**GET** `/api/v1/clientes`

**Query Parameters:**
- `q` (string, optional): Búsqueda por nombre, RUC/CI o teléfono
- `page` (int, optional): Número de página (default: 1)
- `limit` (int, optional): Elementos por página (default: 20)

**Respuesta 200:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "Juan Pérez",
      "ruc_ci": "12345678",
      "direccion": "Calle Principal 123",
      "telefono": "0987654321",
      "email": "juan@example.com",
      "fecha_registro": "2024-01-15T10:30:00",
      "activo": true
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 1,
    "pages": 1
  }
}
```

### 6.2 Obtener Cliente

**GET** `/api/v1/clientes/{id}`

**Parámetros de Ruta:**
- `id` (int): ID del cliente

**Respuesta 200:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "nombre": "Juan Pérez",
    "ruc_ci": "12345678",
    "direccion": "Calle Principal 123",
    "telefono": "0987654321",
    "email": "juan@example.com",
    "fecha_registro": "2024-01-15T10:30:00",
    "activo": true,
    "total_facturado": 150000.00,
    "total_facturas": 5
  }
}
```

**Respuesta 404:**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Cliente no encontrado"
  }
}
```

### 6.3 Crear Cliente

**POST** `/api/v1/clientes`

**Body (JSON):**
```json
{
  "nombre": "Juan Pérez",
  "ruc_ci": "12345678",
  "direccion": "Calle Principal 123",
  "telefono": "0987654321",
  "email": "juan@example.com"
}
```

**Campos:**
- `nombre` (string, required): Nombre del cliente
- `ruc_ci` (string, optional): RUC o CI
- `direccion` (string, optional): Dirección
- `telefono` (string, optional): Teléfono
- `email` (string, optional): Email (debe ser válido)

**Respuesta 201:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "nombre": "Juan Pérez",
    "ruc_ci": "12345678",
    "direccion": "Calle Principal 123",
    "telefono": "0987654321",
    "email": "juan@example.com",
    "fecha_registro": "2024-01-15T10:30:00",
    "activo": true
  }
}
```

**Respuesta 400:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Error de validación",
    "details": {
      "nombre": ["Este campo es requerido"],
      "email": ["Formato de email inválido"]
    }
  }
}
```

### 6.4 Actualizar Cliente

**PUT** `/api/v1/clientes/{id}`

**Parámetros de Ruta:**
- `id` (int): ID del cliente

**Body (JSON):** Mismo formato que crear

**Respuesta 200:** Cliente actualizado

**Respuesta 404:** Cliente no encontrado

### 6.5 Eliminar Cliente

**DELETE** `/api/v1/clientes/{id}`

**Parámetros de Ruta:**
- `id` (int): ID del cliente

**Respuesta 200:**
```json
{
  "success": true,
  "message": "Cliente eliminado correctamente"
}
```

**Respuesta 400:** Si el cliente tiene facturas asociadas
```json
{
  "success": false,
  "error": {
    "code": "BUSINESS_RULE_VIOLATION",
    "message": "No se puede eliminar un cliente con facturas asociadas"
  }
}
```

### 6.6 Buscar Clientes

**GET** `/api/v1/clientes/buscar?q={query}`

**Query Parameters:**
- `q` (string, required): Término de búsqueda

**Respuesta 200:** Lista de clientes que coinciden

---

## 7. Endpoints de Productos

### 7.1 Listar Productos

**GET** `/api/v1/productos`

**Query Parameters:**
- `q` (string, optional): Búsqueda por código o nombre
- `categoria` (string, optional): Filtrar por categoría
- `stock_bajo` (boolean, optional): Solo productos con stock bajo
- `page` (int, optional): Número de página
- `limit` (int, optional): Elementos por página

**Respuesta 200:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "codigo": "PROD-001",
      "nombre": "Laptop Dell",
      "descripcion": "Laptop Dell Inspiron 15",
      "precio_unitario": 1500.00,
      "stock": 10,
      "categoria": "Electrónica",
      "fecha_registro": "2024-01-15T10:30:00",
      "activo": true
    }
  ],
  "pagination": {...}
}
```

### 7.2 Obtener Producto

**GET** `/api/v1/productos/{id}`

**Respuesta 200:** Producto completo

### 7.3 Crear Producto

**POST** `/api/v1/productos`

**Body (JSON):**
```json
{
  "codigo": "PROD-001",
  "nombre": "Laptop Dell",
  "descripcion": "Laptop Dell Inspiron 15",
  "precio_unitario": 1500.00,
  "stock": 10,
  "categoria": "Electrónica"
}
```

**Campos:**
- `codigo` (string, required): Código único del producto
- `nombre` (string, required): Nombre del producto
- `descripcion` (string, optional): Descripción
- `precio_unitario` (float, required): Precio (debe ser >= 0)
- `stock` (int, optional): Stock inicial (default: 0, debe ser >= 0)
- `categoria` (string, optional): Categoría

**Respuesta 201:** Producto creado

**Respuesta 400:** Si el código ya existe
```json
{
  "success": false,
  "error": {
    "code": "DUPLICATE_ENTRY",
    "message": "El código 'PROD-001' ya existe"
  }
}
```

### 7.4 Actualizar Producto

**PUT** `/api/v1/productos/{id}`

**Body (JSON):** Mismo formato que crear (codigo no se puede cambiar)

**Respuesta 200:** Producto actualizado

### 7.5 Eliminar Producto

**DELETE** `/api/v1/productos/{id}`

**Respuesta 200:** Producto eliminado

**Respuesta 400:** Si el producto está en facturas

### 7.6 Productos con Stock Bajo

**GET** `/api/v1/productos/stock-bajo?umbral=10`

**Query Parameters:**
- `umbral` (int, optional): Umbral de stock bajo (default: 10)

**Respuesta 200:** Lista de productos con stock bajo

### 7.7 Verificar Stock

**GET** `/api/v1/productos/{id}/stock`

**Respuesta 200:**
```json
{
  "success": true,
  "data": {
    "producto_id": 1,
    "codigo": "PROD-001",
    "nombre": "Laptop Dell",
    "stock_disponible": 10,
    "stock_bajo": false
  }
}
```

---

## 8. Endpoints de Facturas

### 8.1 Listar Facturas

**GET** `/api/v1/facturas`

**Query Parameters:**
- `q` (string, optional): Búsqueda por número de factura o cliente
- `cliente_id` (int, optional): Filtrar por cliente
- `estado` (string, optional): Filtrar por estado (PENDIENTE, PAGADA, ANULADA)
- `fecha_desde` (date, optional): Fecha desde (YYYY-MM-DD)
- `fecha_hasta` (date, optional): Fecha hasta (YYYY-MM-DD)
- `page` (int, optional): Número de página
- `limit` (int, optional): Elementos por página

**Respuesta 200:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "numero_factura": "FAC-0001",
      "cliente_id": 1,
      "cliente_nombre": "Juan Pérez",
      "fecha_emision": "2024-01-15",
      "fecha_vencimiento": null,
      "subtotal": 1500.00,
      "iva": 315.00,
      "total": 1815.00,
      "estado": "PENDIENTE",
      "notas": null,
      "fecha_creacion": "2024-01-15T10:30:00"
    }
  ],
  "pagination": {...}
}
```

### 8.2 Obtener Factura Completa

**GET** `/api/v1/facturas/{id}`

**Respuesta 200:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "numero_factura": "FAC-0001",
    "cliente": {
      "id": 1,
      "nombre": "Juan Pérez",
      "ruc_ci": "12345678",
      "direccion": "Calle Principal 123",
      "telefono": "0987654321",
      "email": "juan@example.com"
    },
    "fecha_emision": "2024-01-15",
    "fecha_vencimiento": null,
    "subtotal": 1500.00,
    "iva": 315.00,
    "total": 1815.00,
    "estado": "PENDIENTE",
    "notas": null,
    "fecha_creacion": "2024-01-15T10:30:00",
    "detalles": [
      {
        "id": 1,
        "producto_id": 1,
        "producto_codigo": "PROD-001",
        "producto_nombre": "Laptop Dell",
        "cantidad": 1,
        "precio_unitario": 1500.00,
        "subtotal": 1500.00
      }
    ]
  }
}
```

### 8.3 Crear Factura

**POST** `/api/v1/facturas`

**Body (JSON):**
```json
{
  "cliente_id": 1,
  "fecha_emision": "2024-01-15",
  "fecha_vencimiento": "2024-02-15",
  "iva": 21.0,
  "notas": "Factura de prueba",
  "detalles": [
    {
      "producto_id": 1,
      "cantidad": 1,
      "precio_unitario": 1500.00
    },
    {
      "producto_id": 2,
      "cantidad": 2,
      "precio_unitario": 100.00
    }
  ]
}
```

**Campos:**
- `cliente_id` (int, required): ID del cliente
- `fecha_emision` (date, required): Fecha de emisión (YYYY-MM-DD)
- `fecha_vencimiento` (date, optional): Fecha de vencimiento
- `iva` (float, optional): Porcentaje de IVA (default: 0 o configurado)
- `notas` (string, optional): Notas u observaciones
- `detalles` (array, required): Array de productos
  - `producto_id` (int, required): ID del producto
  - `cantidad` (int, required): Cantidad (debe ser > 0)
  - `precio_unitario` (float, required): Precio unitario

**Validaciones:**
- Cliente debe existir
- Todos los productos deben existir
- Stock suficiente para todos los productos
- Cantidades > 0
- Precios >= 0

**Respuesta 201:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "numero_factura": "FAC-0001",
    ...
  }
}
```

**Respuesta 422 - Stock Insuficiente:**
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "Stock insuficiente",
    "details": {
      "producto_id": 1,
      "producto_nombre": "Laptop Dell",
      "stock_disponible": 0,
      "cantidad_solicitada": 1
    }
  }
}
```

### 8.4 Cambiar Estado de Factura

**PATCH** `/api/v1/facturas/{id}/estado`

**Body (JSON):**
```json
{
  "estado": "PAGADA"
}
```

**Estados válidos:**
- `PENDIENTE`
- `PAGADA`
- `ANULADA`

**Respuesta 200:** Factura actualizada

**Respuesta 400:** Estado inválido o transición no permitida

### 8.5 Anular Factura

**DELETE** `/api/v1/facturas/{id}`

**Nota:** En realidad cambia el estado a ANULADA, no elimina físicamente

**Query Parameters:**
- `reversar_stock` (boolean, optional): Si se debe reversar el stock (default: false)

**Respuesta 200:**
```json
{
  "success": true,
  "message": "Factura anulada correctamente"
}
```

### 8.6 Exportar Factura a PDF

**GET** `/api/v1/facturas/{id}/pdf`

**Respuesta 200:** Archivo PDF (Content-Type: application/pdf)

**Headers:**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="FAC-0001.pdf"
```

### 8.7 Buscar Facturas

**GET** `/api/v1/facturas/buscar`

**Query Parameters:** Mismos que listar facturas

**Respuesta 200:** Lista de facturas filtradas

---

## 9. Endpoints de Dashboard

### 9.1 Estadísticas Generales

**GET** `/api/v1/dashboard/stats`

**Respuesta 200:**
```json
{
  "success": true,
  "data": {
    "total_clientes": 150,
    "total_productos": 500,
    "total_facturas": 1200,
    "facturas_pendientes": 45,
    "productos_stock_bajo": 12,
    "ingresos_mes_actual": 50000.00,
    "ingresos_mes_anterior": 45000.00
  }
}
```

### 9.2 Ventas del Mes

**GET** `/api/v1/dashboard/ventas-mes?mes=2024-01`

**Query Parameters:**
- `mes` (string, optional): Mes en formato YYYY-MM (default: mes actual)

**Respuesta 200:**
```json
{
  "success": true,
  "data": {
    "mes": "2024-01",
    "total_facturas": 50,
    "total_ingresos": 50000.00,
    "facturas_por_dia": [
      {"fecha": "2024-01-01", "cantidad": 5, "total": 5000.00},
      {"fecha": "2024-01-02", "cantidad": 3, "total": 3000.00},
      ...
    ]
  }
}
```

---

## 10. Ejemplos de Uso

### 10.1 Crear Cliente (JavaScript)

```javascript
async function crearCliente(datos) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/clientes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('Cliente creado:', result.data);
            return result.data;
        } else {
            console.error('Error:', result.error);
            throw new Error(result.error.message);
        }
    } catch (error) {
        console.error('Error de red:', error);
        throw error;
    }
}

// Uso
crearCliente({
    nombre: "Juan Pérez",
    ruc_ci: "12345678",
    email: "juan@example.com"
});
```

### 10.2 Crear Factura (JavaScript)

```javascript
async function crearFactura(datos) {
    const response = await fetch('http://localhost:5000/api/v1/facturas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cliente_id: 1,
            fecha_emision: "2024-01-15",
            iva: 21.0,
            detalles: [
                {
                    producto_id: 1,
                    cantidad: 2,
                    precio_unitario: 1500.00
                }
            ]
        })
    });
    
    const result = await response.json();
    return result;
}
```

### 10.3 Listar Productos con Filtros (JavaScript)

```javascript
async function listarProductos(filtros = {}) {
    const params = new URLSearchParams();
    
    if (filtros.q) params.append('q', filtros.q);
    if (filtros.categoria) params.append('categoria', filtros.categoria);
    if (filtros.stock_bajo) params.append('stock_bajo', 'true');
    if (filtros.page) params.append('page', filtros.page);
    
    const response = await fetch(
        `http://localhost:5000/api/v1/productos?${params.toString()}`
    );
    
    const result = await response.json();
    return result;
}

// Uso
listarProductos({
    q: 'laptop',
    categoria: 'Electrónica',
    stock_bajo: true,
    page: 1
});
```

### 10.4 Exportar PDF (JavaScript)

```javascript
async function exportarPDF(facturaId) {
    const response = await fetch(
        `http://localhost:5000/api/v1/facturas/${facturaId}/pdf`
    );
    
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `FAC-${facturaId}.pdf`;
    a.click();
}
```

---

## 11. Documentación OpenAPI

FastAPI genera automáticamente documentación OpenAPI (Swagger) en:

- **Swagger UI**: `http://localhost:5000/docs`
- **ReDoc**: `http://localhost:5000/redoc`
- **OpenAPI JSON**: `http://localhost:5000/openapi.json`

---

**Fin del Documento de Diseño de API**

