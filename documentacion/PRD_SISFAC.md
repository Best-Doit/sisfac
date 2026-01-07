# PRD - Sistema de Facturación (SISFAC)

## Documento de Requisitos del Producto

**Versión:** 1.0  
**Fecha:** 2024  
**Autor:** Equipo de Desarrollo  
**Estado:** En Desarrollo

---

## Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Objetivos del Proyecto](#objetivos-del-proyecto)
3. [Alcance del Proyecto](#alcance-del-proyecto)
4. [Stakeholders](#stakeholders)
5. [Requisitos Funcionales](#requisitos-funcionales)
6. [Requisitos No Funcionales](#requisitos-no-funcionales)
7. [Arquitectura Técnica](#arquitectura-técnica)
8. [Diseño de Base de Datos](#diseño-de-base-de-datos)
9. [APIs y Endpoints](#apis-y-endpoints)
10. [Diseño de Interfaz de Usuario](#diseño-de-interfaz-de-usuario)
11. [Casos de Uso](#casos-de-uso)
12. [Plan de Desarrollo](#plan-de-desarrollo)
13. [Criterios de Aceptación](#criterios-de-aceptación)
14. [Riesgos y Mitigaciones](#riesgos-y-mitigaciones)

---

## 1. Visión General

### 1.1 Descripción del Producto

SISFAC es un sistema de facturación completo diseñado para pequeñas y medianas empresas que necesitan gestionar sus operaciones de facturación, inventario y clientes de manera eficiente. El sistema está diseñado como una aplicación de escritorio multiplataforma que combina la potencia de Python en el backend con tecnologías web modernas en el frontend.

### 1.2 Propósito del Documento

Este documento define los requisitos funcionales y no funcionales, la arquitectura técnica, el diseño de la interfaz de usuario y todos los aspectos necesarios para el desarrollo del sistema SISFAC.

### 1.3 Definiciones y Acrónimos

- **SISFAC**: Sistema de Facturación
- **PRD**: Product Requirements Document
- **API**: Application Programming Interface
- **REST**: Representational State Transfer
- **CRUD**: Create, Read, Update, Delete
- **UI/UX**: User Interface/User Experience
- **SQLite**: Base de datos relacional embebida
- **IVU/IVA**: Impuesto sobre Ventas/Valor Añadido

---

## 2. Objetivos del Proyecto

### 2.1 Objetivos Principales

1. **Automatización de Facturación**
   - Generar facturas de manera rápida y eficiente
   - Calcular automáticamente totales, subtotales e impuestos
   - Generar números de factura secuenciales

2. **Gestión de Inventario**
   - Control de stock en tiempo real
   - Alertas de productos con stock bajo
   - Gestión de productos con categorías

3. **Gestión de Clientes**
   - Base de datos centralizada de clientes
   - Historial completo de transacciones por cliente
   - Información de contacto organizada

4. **Historial y Reportes**
   - Registro detallado de todas las facturas
   - Búsqueda y filtrado avanzado
   - Exportación de datos

### 2.2 Objetivos Secundarios

- Interfaz de usuario moderna e intuitiva
- Aplicación multiplataforma (Windows, Linux, macOS)
- Rendimiento óptimo en equipos de gama media
- Fácil instalación y uso
- Sistema robusto y confiable

---

## 3. Alcance del Proyecto

### 3.1 Incluido en el Alcance

✅ **Módulo de Clientes**
- CRUD completo de clientes
- Búsqueda y filtrado
- Validación de datos

✅ **Módulo de Inventario**
- CRUD completo de productos
- Control de stock
- Categorización de productos
- Alertas de stock bajo

✅ **Módulo de Facturación**
- Creación de facturas
- Múltiples productos por factura
- Cálculo automático de totales
- Estados de factura (Pendiente, Pagada, Anulada)

✅ **Módulo de Historial**
- Listado completo de facturas
- Búsqueda por múltiples criterios
- Vista detallada de facturas
- Filtros por fecha, cliente, estado

✅ **Funcionalidades Adicionales**
- Exportación a PDF
- Exportación a Excel/CSV
- Búsqueda global
- Dashboard con resumen

### 3.2 Excluido del Alcance (Fase 1)

❌ Sistema multi-usuario con roles
❌ Sincronización en la nube
❌ Integración con sistemas contables externos
❌ Punto de venta (POS) físico
❌ Gestión de proveedores
❌ Reportes financieros avanzados
❌ Sistema de impresión de tickets físicos
❌ Integración con impresoras fiscales

---

## 4. Stakeholders

### 4.1 Usuarios Principales

- **Administradores de Negocio**: Gestión completa del sistema
- **Personal de Ventas**: Creación de facturas y consulta de clientes
- **Personal de Almacén**: Gestión de inventario

### 4.2 Equipo de Desarrollo

- Desarrolladores Backend (Python/Flask/FastAPI)
- Desarrolladores Frontend (Tailwind/Alpine.js)
- Diseñadores UI/UX
- QA/Testing

---

## 5. Requisitos Funcionales

### 5.1 Módulo de Clientes

#### RF-001: Gestión de Clientes
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir crear, leer, actualizar y eliminar clientes.

**Detalles:**
- **Crear Cliente**
  - Campos requeridos: Nombre
  - Campos opcionales: RUC/CI, Dirección, Teléfono, Email
  - Validación de formato de email
  - Validación de RUC/CI único (opcional)
  - Timestamp automático de registro

- **Listar Clientes**
  - Tabla con todos los clientes
  - Ordenamiento por nombre
  - Paginación (si hay muchos registros)
  - Indicador de total de clientes

- **Editar Cliente**
  - Edición de todos los campos
  - Mantener historial de facturas asociadas
  - Validación de datos actualizados

- **Eliminar Cliente**
  - Confirmación antes de eliminar
  - Verificar si tiene facturas asociadas
  - Si tiene facturas: desactivar en lugar de eliminar (soft delete)

#### RF-002: Búsqueda de Clientes
**Prioridad:** Media  
**Descripción:** El sistema debe permitir buscar clientes por múltiples criterios.

**Detalles:**
- Búsqueda por nombre (búsqueda parcial)
- Búsqueda por RUC/CI
- Búsqueda por teléfono
- Búsqueda en tiempo real (mientras se escribe)
- Resultados destacados con coincidencias

#### RF-003: Vista Detallada de Cliente
**Prioridad:** Media  
**Descripción:** Mostrar información completa del cliente y su historial.

**Detalles:**
- Información completa del cliente
- Lista de facturas asociadas
- Total facturado al cliente
- Estadísticas básicas (número de facturas, última factura)

### 5.2 Módulo de Inventario

#### RF-004: Gestión de Productos
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir gestionar productos del inventario.

**Detalles:**
- **Crear Producto**
  - Campos requeridos: Código (único), Nombre, Precio Unitario
  - Campos opcionales: Descripción, Categoría, Stock inicial
  - Validación de código único
  - Validación de precio positivo
  - Validación de stock no negativo

- **Listar Productos**
  - Tabla con todos los productos
  - Mostrar: Código, Nombre, Precio, Stock, Categoría
  - Indicador visual de stock bajo
  - Ordenamiento por nombre o código
  - Filtro por categoría

- **Editar Producto**
  - Edición de todos los campos excepto código
  - Actualización de stock manual
  - Historial de cambios (opcional)

- **Eliminar Producto**
  - Confirmación antes de eliminar
  - Verificar si está en facturas
  - Si está en facturas: desactivar (soft delete)

#### RF-005: Control de Stock
**Prioridad:** Alta  
**Descripción:** El sistema debe controlar el stock de productos automáticamente.

**Detalles:**
- Reducción automática de stock al facturar
- Validación de stock disponible antes de facturar
- Alertas cuando el stock es bajo (umbral configurable, default: 10)
- Indicador visual de stock bajo en la lista
- Actualización manual de stock permitida

#### RF-006: Categorización de Productos
**Prioridad:** Baja  
**Descripción:** Los productos pueden organizarse por categorías.

**Detalles:**
- Campo de categoría libre (texto)
- Filtrado por categoría
- Estadísticas por categoría (opcional)

#### RF-007: Búsqueda de Productos
**Prioridad:** Media  
**Descripción:** Búsqueda rápida de productos.

**Detalles:**
- Búsqueda por código (exacta)
- Búsqueda por nombre (parcial)
- Búsqueda en tiempo real
- Resultados destacados

### 5.3 Módulo de Facturación

#### RF-008: Creación de Facturas
**Prioridad:** Crítica  
**Descripción:** El sistema debe permitir crear facturas completas.

**Detalles:**
- **Selección de Cliente**
  - Búsqueda y selección de cliente existente
  - Opción de crear cliente rápido (modal)
  - Información del cliente visible

- **Agregar Productos**
  - Búsqueda de productos
  - Agregar múltiples productos
  - Especificar cantidad para cada producto
  - Validar stock disponible
  - Mostrar precio unitario y subtotal por línea
  - Permitir eliminar productos de la factura
  - Permitir editar cantidad

- **Cálculo Automático**
  - Subtotal (suma de líneas)
  - IVA (configurable, default: 0% o 21%)
  - Total (subtotal + IVA)
  - Actualización en tiempo real

- **Información de Factura**
  - Número de factura automático (secuencial)
  - Fecha de emisión (automática, editable)
  - Fecha de vencimiento (opcional)
  - Estado inicial: "PENDIENTE"
  - Notas/observaciones (opcional)

- **Guardar Factura**
  - Validación de datos completos
  - Reducción automática de stock
  - Generación de número único
  - Guardado en base de datos
  - Confirmación de éxito

#### RF-009: Numeración de Facturas
**Prioridad:** Alta  
**Descripción:** Sistema de numeración automática y secuencial.

**Detalles:**
- Formato: FAC-0001, FAC-0002, etc.
- Numeración secuencial sin saltos
- No permitir duplicados
- Configuración de prefijo (opcional)

#### RF-010: Estados de Factura
**Prioridad:** Media  
**Descripción:** Las facturas pueden tener diferentes estados.

**Detalles:**
- **PENDIENTE**: Factura creada, no pagada
- **PAGADA**: Factura pagada
- **ANULADA**: Factura cancelada
- Cambio de estado con confirmación
- Si se anula: reversar stock (opcional)

#### RF-011: Validaciones de Facturación
**Prioridad:** Alta  
**Descripción:** Validaciones antes de crear factura.

**Detalles:**
- Cliente seleccionado (requerido)
- Al menos un producto (requerido)
- Stock suficiente para todos los productos
- Cantidades mayores a cero
- Precios válidos

### 5.4 Módulo de Historial

#### RF-012: Listado de Facturas
**Prioridad:** Alta  
**Descripción:** Mostrar todas las facturas con información relevante.

**Detalles:**
- Tabla con columnas: Número, Fecha, Cliente, Total, Estado
- Ordenamiento por fecha (más recientes primero)
- Paginación (si hay muchas facturas)
- Indicador visual del estado (colores)
- Acción rápida: Ver detalle

#### RF-013: Búsqueda y Filtros
**Prioridad:** Alta  
**Descripción:** Búsqueda avanzada de facturas.

**Detalles:**
- Búsqueda por número de factura
- Búsqueda por nombre de cliente
- Filtro por rango de fechas
- Filtro por estado
- Filtro por cliente específico
- Combinación de múltiples filtros
- Botón de limpiar filtros

#### RF-014: Vista Detallada de Factura
**Prioridad:** Alta  
**Descripción:** Mostrar información completa de una factura.

**Detalles:**
- **Información de Cabecera**
  - Número de factura
  - Fechas (emisión, vencimiento)
  - Estado
  - Información del cliente completa

- **Detalle de Productos**
  - Tabla con todos los productos
  - Columnas: Código, Nombre, Cantidad, Precio Unitario, Subtotal
  - Totales: Subtotal, IVA, Total

- **Acciones**
  - Cambiar estado
  - Exportar a PDF
  - Imprimir
  - Anular (si está pendiente)

#### RF-015: Exportación de Datos
**Prioridad:** Media  
**Descripción:** Exportar facturas y datos a diferentes formatos.

**Detalles:**
- **Exportar a PDF**
  - Formato profesional de factura
  - Logo de empresa (opcional)
  - Información completa
  - Diseño imprimible

- **Exportar a Excel/CSV**
  - Listado de facturas
  - Datos tabulares
  - Útil para análisis

- **Exportar Historial Completo**
  - Todas las facturas en un período
  - Formato CSV o Excel

### 5.5 Funcionalidades Generales

#### RF-016: Dashboard
**Prioridad:** Media  
**Descripción:** Pantalla de inicio con resumen de información.

**Detalles:**
- Total de clientes
- Total de productos
- Total de facturas
- Facturas del mes
- Ingresos del mes
- Productos con stock bajo
- Gráfico de facturas por mes (opcional)

#### RF-017: Búsqueda Global
**Prioridad:** Baja  
**Descripción:** Búsqueda unificada en todo el sistema.

**Detalles:**
- Búsqueda en clientes, productos y facturas
- Resultados categorizados
- Navegación rápida a resultados

#### RF-018: Configuración
**Prioridad:** Baja  
**Descripción:** Configuraciones básicas del sistema.

**Detalles:**
- Porcentaje de IVA por defecto
- Prefijo de número de factura
- Umbral de stock bajo
- Información de empresa (nombre, dirección, teléfono)
- Formato de fecha

---

## 6. Requisitos No Funcionales

### 6.1 Rendimiento

- **RNF-001**: La aplicación debe iniciar en menos de 3 segundos
- **RNF-002**: Las operaciones CRUD deben completarse en menos de 1 segundo
- **RNF-003**: Las búsquedas deben mostrar resultados en menos de 500ms
- **RNF-004**: La aplicación debe manejar al menos 10,000 registros sin degradación notable
- **RNF-005**: El consumo de memoria no debe exceder 500MB en uso normal

### 6.2 Usabilidad

- **RNF-006**: La interfaz debe ser intuitiva sin necesidad de capacitación extensa
- **RNF-007**: Todas las acciones deben tener feedback visual inmediato
- **RNF-008**: Mensajes de error deben ser claros y accionables
- **RNF-009**: La navegación debe ser consistente en toda la aplicación
- **RNF-010**: Debe haber confirmaciones para acciones destructivas

### 6.3 Confiabilidad

- **RNF-011**: El sistema debe tener un tiempo de actividad del 99.5%
- **RNF-012**: Los datos deben guardarse automáticamente
- **RNF-013**: Debe haber validación de integridad de datos
- **RNF-014**: El sistema debe manejar errores gracefully sin crashear
- **RNF-015**: Debe haber sistema de backup automático (opcional)

### 6.4 Seguridad

- **RNF-016**: Validación de todos los inputs del usuario
- **RNF-017**: Protección contra inyección SQL
- **RNF-018**: Sanitización de datos antes de mostrar
- **RNF-019**: Manejo seguro de sesiones (si aplica)
- **RNF-020**: Los datos sensibles no deben estar en logs

### 6.5 Compatibilidad

- **RNF-021**: Debe funcionar en Windows 10/11
- **RNF-022**: Debe funcionar en Linux (Ubuntu 20.04+)
- **RNF-023**: Debe funcionar en macOS 11+
- **RNF-024**: Debe funcionar en sistemas de 64 bits
- **RNF-025**: Compatible con Python 3.9+

### 6.6 Mantenibilidad

- **RNF-026**: Código bien documentado y comentado
- **RNF-027**: Arquitectura modular y extensible
- **RNF-028**: Separación clara de responsabilidades
- **RNF-029**: Uso de estándares de código (PEP 8 para Python)
- **RNF-030**: Tests unitarios para lógica crítica

### 6.7 Portabilidad

- **RNF-031**: Empaquetado como ejecutable independiente
- **RNF-032**: Instalación simple (instalador o ejecutable)
- **RNF-033**: No requiere instalación de Python en el sistema
- **RNF-034**: Base de datos portable (archivo SQLite)

---

## 7. Arquitectura Técnica

### 7.1 Stack Tecnológico

#### Frontend
- **Tailwind CSS 3.x**: Framework de utilidades CSS para diseño moderno
- **Alpine.js 3.x**: Framework JavaScript ligero para interactividad
- **HTML5**: Estructura semántica
- **Vanilla JavaScript**: Para funcionalidades adicionales

#### Backend
- **Flask 2.x**: Framework web para servir páginas y manejar rutas
- **FastAPI**: Framework para APIs REST de alto rendimiento
- **SQLAlchemy 2.x**: ORM para manejo de base de datos
- **SQLite**: Base de datos relacional embebida

#### Empaquetado
- **Electron**: Framework para empaquetar aplicación web como escritorio
- **electron-builder**: Herramienta para crear instaladores

#### Utilidades
- **ReportLab / WeasyPrint**: Generación de PDFs
- **openpyxl**: Exportación a Excel
- **python-dateutil**: Manejo de fechas
- **Pydantic**: Validación de datos (con FastAPI)

### 7.2 Arquitectura de Capas

```
┌─────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                 │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Electron (Contenedor)                            │  │
│  │  ┌─────────────────────────────────────────────┐ │  │
│  │  │  Frontend Web (HTML/CSS/JS)                 │ │  │
│  │  │  - Tailwind CSS (Estilos)                   │ │  │
│  │  │  - Alpine.js (Interactividad)               │ │  │
│  │  │  - Templates Jinja2 (Flask)                │ │  │
│  │  └─────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        ↕ HTTP/REST
┌─────────────────────────────────────────────────────────┐
│                  CAPA DE APLICACIÓN                      │
│  ┌──────────────────┐        ┌──────────────────┐      │
│  │  Flask           │        │  FastAPI         │      │
│  │  (Server-Side    │        │  (API REST)      │      │
│  │   Rendering)     │        │                  │      │
│  └──────────────────┘        └──────────────────┘      │
│         │                           │                   │
│         └───────────┬───────────────┘                   │
│                     │                                   │
│         ┌───────────▼───────────┐                       │
│         │  Servicios de Negocio │                       │
│         │  - ClienteService     │                       │
│         │  - ProductoService    │                       │
│         │  - FacturaService     │                       │
│         └───────────┬───────────┘                       │
└─────────────────────┼───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              CAPA DE ACCESO A DATOS                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │  SQLAlchemy ORM                                   │  │
│  │  - Modelos de Datos                               │  │
│  │  - Queries y Transacciones                       │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                  BASE DE DATOS                           │
│  ┌───────────────────────────────────────────────────┐  │
│  │  SQLite (Archivo: sisfac.db)                     │  │
│  │  - Tablas Normalizadas                           │  │
│  │  - Índices Optimizados                           │  │
│  │  - Integridad Referencial                        │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 7.3 Flujo de Comunicación

#### Modo Desarrollo
1. Electron inicia y abre ventana
2. Flask/FastAPI se ejecuta en proceso separado (localhost:5000)
3. Frontend hace requests HTTP a Flask/FastAPI
4. Flask renderiza templates o FastAPI devuelve JSON

#### Modo Producción
1. Electron empaqueta Flask/FastAPI como proceso hijo
2. Servidor se inicia automáticamente en puerto local
3. Electron carga la aplicación desde localhost
4. Comunicación vía HTTP interno

### 7.4 Estructura de Directorios

```
SISFAC/
├── frontend/                    # Frontend Electron
│   ├── src/
│   │   ├── index.html          # Punto de entrada HTML
│   │   ├── main.js             # Proceso principal Electron
│   │   ├── renderer.js         # Proceso renderer Electron
│   │   ├── styles/
│   │   │   └── tailwind.css    # CSS compilado
│   │   └── js/
│   │       ├── components/     # Componentes Alpine.js
│   │       └── utils/          # Utilidades JS
│   ├── package.json
│   ├── tailwind.config.js
│   └── electron-builder.yml
│
├── backend/                     # Backend Python
│   ├── app/
│   │   ├── __init__.py         # Factory Flask
│   │   ├── config.py           # Configuraciones
│   │   │
│   │   ├── models/             # Modelos SQLAlchemy
│   │   │   ├── __init__.py
│   │   │   ├── cliente.py
│   │   │   ├── producto.py
│   │   │   └── factura.py
│   │   │
│   │   ├── routes/             # Rutas Flask
│   │   │   ├── __init__.py
│   │   │   ├── clientes.py
│   │   │   ├── inventario.py
│   │   │   ├── facturas.py
│   │   │   └── dashboard.py
│   │   │
│   │   ├── api/                # Endpoints FastAPI
│   │   │   ├── __init__.py
│   │   │   ├── clientes.py
│   │   │   ├── productos.py
│   │   │   └── facturas.py
│   │   │
│   │   ├── services/           # Lógica de Negocio
│   │   │   ├── __init__.py
│   │   │   ├── cliente_service.py
│   │   │   ├── producto_service.py
│   │   │   └── factura_service.py
│   │   │
│   │   ├── database/           # Acceso a Datos
│   │   │   ├── __init__.py
│   │   │   ├── db.py          # Conexión SQLAlchemy
│   │   │   └── migrations/    # Migraciones (opcional)
│   │   │
│   │   ├── utils/             # Utilidades
│   │   │   ├── validators.py
│   │   │   ├── formatters.py
│   │   │   └── helpers.py
│   │   │
│   │   ├── static/            # Archivos estáticos
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── images/
│   │   │
│   │   └── templates/      # Templates Jinja2
│   │       ├── base.html
│   │       ├── components/
│   │       ├── clientes/
│   │       ├── inventario/
│   │       └── facturas/
│   │
│   ├── requirements.txt
│   └── run.py                 # Punto de entrada
│
├── documentacion/             # Documentación
│   ├── PRD_SISFAC.md         # Este documento
│   ├── arquitectura.md       # Detalles arquitectónicos
│   └── guia_usuario.md       # Manual de usuario
│
├── tests/                     # Tests
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/                   # Scripts de utilidad
│   ├── build.py              # Script de build
│   └── setup.py              # Setup inicial
│
├── .gitignore
├── README.md
└── LICENSE
```

### 7.5 Patrones de Diseño

#### Backend
- **Factory Pattern**: Para inicialización de Flask
- **Repository Pattern**: Para acceso a datos (opcional)
- **Service Layer**: Para lógica de negocio
- **Dependency Injection**: Para servicios

#### Frontend
- **Component Pattern**: Componentes Alpine.js reutilizables
- **Template Pattern**: Templates Jinja2 base
- **Observer Pattern**: Eventos Alpine.js

---

## 8. Diseño de Base de Datos

### 8.1 Modelo Entidad-Relación

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  CLIENTES   │         │   FACTURAS   │         │  PRODUCTOS  │
├─────────────┤         ├──────────────┤         ├─────────────┤
│ id (PK)     │◄──┐     │ id (PK)      │     ┌──►│ id (PK)     │
│ nombre      │   │     │ numero_fact  │     │   │ codigo (UK) │
│ ruc_ci      │   │     │ cliente_id   │─────┘   │ nombre      │
│ direccion   │   │     │ fecha_emision│         │ precio_unit │
│ telefono    │   │     │ fecha_venc   │         │ stock       │
│ email       │   │     │ subtotal     │         │ categoria   │
│ fecha_reg   │   │     │ iva          │         │ descripcion │
└─────────────┘   │     │ total        │         │ fecha_reg   │
                  │     │ estado       │         └─────────────┘
                  │     │ notas        │                │
                  │     └──────────────┘                │
                  │              │                       │
                  │              │                       │
                  │     ┌────────▼──────────┐           │
                  │     │ DETALLE_FACTURA   │           │
                  │     ├───────────────────┤           │
                  │     │ id (PK)           │           │
                  │     │ factura_id (FK)   │           │
                  │     │ producto_id (FK)  │───────────┘
                  │     │ cantidad          │
                  │     │ precio_unitario   │
                  │     │ subtotal          │
                  │     └───────────────────┘
                  │
                  └────── Relación 1:N
```

### 8.2 Esquema de Tablas

#### Tabla: clientes
```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    ruc_ci TEXT,
    direccion TEXT,
    telefono TEXT,
    email TEXT,
    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
    activo INTEGER DEFAULT 1
);

CREATE INDEX idx_clientes_nombre ON clientes(nombre);
CREATE INDEX idx_clientes_ruc ON clientes(ruc_ci);
```

#### Tabla: productos
```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio_unitario REAL NOT NULL CHECK(precio_unitario >= 0),
    stock INTEGER DEFAULT 0 CHECK(stock >= 0),
    categoria TEXT,
    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
    activo INTEGER DEFAULT 1
);

CREATE INDEX idx_productos_codigo ON productos(codigo);
CREATE INDEX idx_productos_nombre ON productos(nombre);
CREATE INDEX idx_productos_categoria ON productos(categoria);
```

#### Tabla: facturas
```sql
CREATE TABLE facturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_factura TEXT UNIQUE NOT NULL,
    cliente_id INTEGER NOT NULL,
    fecha_emision TEXT NOT NULL,
    fecha_vencimiento TEXT,
    subtotal REAL NOT NULL CHECK(subtotal >= 0),
    iva REAL DEFAULT 0 CHECK(iva >= 0),
    total REAL NOT NULL CHECK(total >= 0),
    estado TEXT DEFAULT 'PENDIENTE' CHECK(estado IN ('PENDIENTE', 'PAGADA', 'ANULADA')),
    notas TEXT,
    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE INDEX idx_facturas_numero ON facturas(numero_factura);
CREATE INDEX idx_facturas_cliente ON facturas(cliente_id);
CREATE INDEX idx_facturas_fecha ON facturas(fecha_emision);
CREATE INDEX idx_facturas_estado ON facturas(estado);
```

#### Tabla: detalle_factura
```sql
CREATE TABLE detalle_factura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    factura_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    precio_unitario REAL NOT NULL CHECK(precio_unitario >= 0),
    subtotal REAL NOT NULL CHECK(subtotal >= 0),
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE INDEX idx_detalle_factura ON detalle_factura(factura_id);
CREATE INDEX idx_detalle_producto ON detalle_factura(producto_id);
```

### 8.3 Relaciones

- **clientes → facturas**: 1 a N (un cliente puede tener muchas facturas)
- **facturas → detalle_factura**: 1 a N (una factura tiene muchos detalles)
- **productos → detalle_factura**: 1 a N (un producto puede estar en muchos detalles)

### 8.4 Integridad Referencial

- Claves foráneas con restricciones
- ON DELETE CASCADE para detalles de factura
- Validaciones CHECK para valores positivos
- Unicidad en códigos y números de factura

### 8.5 Índices

- Índices en campos de búsqueda frecuente
- Índices en claves foráneas
- Índices en campos de filtrado (fecha, estado)

---

## 9. APIs y Endpoints

### 9.1 Flask Routes (Server-Side Rendering)

#### Clientes
- `GET /clientes` - Lista de clientes (página)
- `GET /clientes/nuevo` - Formulario nuevo cliente
- `POST /clientes` - Crear cliente
- `GET /clientes/<id>` - Ver detalle cliente
- `GET /clientes/<id>/editar` - Formulario editar
- `PUT /clientes/<id>` - Actualizar cliente
- `DELETE /clientes/<id>` - Eliminar cliente
- `GET /clientes/buscar?q=<query>` - Búsqueda

#### Inventario
- `GET /inventario` - Lista de productos
- `GET /inventario/nuevo` - Formulario nuevo producto
- `POST /inventario` - Crear producto
- `GET /inventario/<id>` - Ver detalle producto
- `GET /inventario/<id>/editar` - Formulario editar
- `PUT /inventario/<id>` - Actualizar producto
- `DELETE /inventario/<id>` - Eliminar producto
- `GET /inventario/buscar?q=<query>` - Búsqueda

#### Facturas
- `GET /facturas` - Lista de facturas
- `GET /facturas/nueva` - Formulario nueva factura
- `POST /facturas` - Crear factura
- `GET /facturas/<id>` - Ver detalle factura
- `PUT /facturas/<id>/estado` - Cambiar estado
- `DELETE /facturas/<id>` - Anular factura
- `GET /facturas/exportar/<id>/pdf` - Exportar PDF
- `GET /facturas/buscar?q=<query>&fecha_desde=&fecha_hasta=&estado=` - Búsqueda avanzada

#### Dashboard
- `GET /` - Dashboard principal

### 9.2 FastAPI Endpoints (REST API)

#### Base URL: `/api/v1`

#### Clientes API
```python
GET    /api/v1/clientes              # Listar clientes
POST   /api/v1/clientes              # Crear cliente
GET    /api/v1/clientes/{id}          # Obtener cliente
PUT    /api/v1/clientes/{id}          # Actualizar cliente
DELETE /api/v1/clientes/{id}          # Eliminar cliente
GET    /api/v1/clientes/buscar?q=     # Búsqueda
```

#### Productos API
```python
GET    /api/v1/productos              # Listar productos
POST   /api/v1/productos              # Crear producto
GET    /api/v1/productos/{id}         # Obtener producto
PUT    /api/v1/productos/{id}         # Actualizar producto
DELETE /api/v1/productos/{id}         # Eliminar producto
GET    /api/v1/productos/buscar?q=    # Búsqueda
GET    /api/v1/productos/stock-bajo   # Productos con stock bajo
```

#### Facturas API
```python
GET    /api/v1/facturas               # Listar facturas
POST   /api/v1/facturas               # Crear factura
GET    /api/v1/facturas/{id}          # Obtener factura completa
PUT    /api/v1/facturas/{id}/estado   # Cambiar estado
DELETE /api/v1/facturas/{id}          # Anular factura
GET    /api/v1/facturas/buscar        # Búsqueda avanzada
GET    /api/v1/facturas/{id}/pdf      # Generar PDF
```

#### Dashboard API
```python
GET    /api/v1/dashboard/stats         # Estadísticas generales
GET    /api/v1/dashboard/ventas-mes   # Ventas del mes
```

### 9.3 Esquemas de Datos (Pydantic)

#### Cliente
```python
class ClienteBase(BaseModel):
    nombre: str
    ruc_ci: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    fecha_registro: datetime
    
    class Config:
        from_attributes = True
```

#### Producto
```python
class ProductoBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    precio_unitario: float
    stock: int = 0
    categoria: Optional[str] = None

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    fecha_registro: datetime
    
    class Config:
        from_attributes = True
```

#### Factura
```python
class DetalleFacturaBase(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

class FacturaBase(BaseModel):
    cliente_id: int
    fecha_emision: date
    fecha_vencimiento: Optional[date] = None
    iva: float = 0.0
    notas: Optional[str] = None
    detalles: List[DetalleFacturaBase]

class FacturaCreate(FacturaBase):
    pass

class Factura(FacturaBase):
    id: int
    numero_factura: str
    subtotal: float
    total: float
    estado: str
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True
```

---

## 10. Diseño de Interfaz de Usuario

### 10.1 Principios de Diseño

- **Moderno y Limpio**: Diseño minimalista con Tailwind CSS
- **Consistente**: Mismos patrones en toda la aplicación
- **Responsive**: Adaptable a diferentes tamaños de ventana
- **Accesible**: Contraste adecuado, navegación por teclado
- **Feedback Visual**: Estados claros (hover, active, disabled)

### 10.2 Sistema de Colores

#### Colores Principales
- **Primary**: `blue-600` (#2563EB) - Botones principales, enlaces
- **Primary Dark**: `blue-700` (#1D4ED8) - Hover de botones
- **Success**: `green-500` (#10B981) - Éxito, confirmaciones
- **Danger**: `red-500` (#EF4444) - Errores, eliminar
- **Warning**: `yellow-500` (#F59E0B) - Advertencias
- **Info**: `blue-500` (#3B82F6) - Información

#### Colores Neutros
- **Background**: `gray-50` (#F9FAFB) - Fondo principal
- **Surface**: `white` (#FFFFFF) - Cards, modales
- **Border**: `gray-200` (#E5E7EB) - Bordes
- **Text Primary**: `gray-900` (#111827) - Texto principal
- **Text Secondary**: `gray-600` (#4B5563) - Texto secundario

### 10.3 Componentes de UI

#### Navbar
- Logo/Nombre de la aplicación a la izquierda
- Menú de navegación (Clientes, Inventario, Facturas, Dashboard)
- Búsqueda global (opcional)
- Información del usuario (si aplica)

#### Sidebar (Opcional)
- Navegación lateral colapsable
- Iconos + texto
- Estado activo destacado

#### Cards
- Sombra sutil (`shadow-md`)
- Bordes redondeados (`rounded-lg`)
- Padding adecuado
- Hover effect sutil

#### Tablas
- Filas alternadas (`even:bg-gray-50`)
- Hover en filas (`hover:bg-blue-50`)
- Headers con fondo (`bg-gray-100`)
- Acciones en última columna

#### Formularios
- Labels claros
- Inputs con bordes y focus states
- Validación visual (rojo para errores)
- Botones de acción claros

#### Modales
- Overlay oscuro semitransparente
- Modal centrado con sombra
- Botón de cerrar visible
- Animación de entrada/salida

#### Botones
- **Primary**: Azul, para acciones principales
- **Secondary**: Gris, para acciones secundarias
- **Danger**: Rojo, para eliminar
- Estados: normal, hover, active, disabled

#### Badges
- Estados de factura con colores
- Stock bajo con color de advertencia
- Pequeños y discretos

### 10.4 Layouts por Módulo

#### Dashboard
- Grid de cards con estadísticas
- Gráfico de ventas (opcional)
- Lista de facturas recientes
- Productos con stock bajo

#### Clientes
- Tabla principal con todos los clientes
- Botón "Agregar Cliente" prominente
- Búsqueda en tiempo real
- Acciones por fila (editar, eliminar)

#### Inventario
- Grid o tabla de productos
- Filtros por categoría
- Búsqueda rápida
- Indicadores visuales de stock

#### Facturas
- Lista de facturas con filtros
- Formulario de nueva factura (modal o página completa)
- Vista detallada de factura
- Acciones: ver, editar estado, exportar

### 10.5 Responsive Design

- Breakpoints de Tailwind:
  - `sm`: 640px
  - `md`: 768px
  - `lg`: 1024px
  - `xl`: 1280px

- Adaptaciones:
  - Tablas con scroll horizontal en móvil
  - Sidebar colapsable en pantallas pequeñas
  - Grids que se convierten en columnas

### 10.6 Iconos

- Usar Heroicons o similar
- Consistentes en tamaño
- Colores según contexto

---

## 11. Casos de Uso

### CU-001: Crear Cliente

**Actor**: Usuario del sistema  
**Precondiciones**: Usuario autenticado (si aplica)  
**Flujo Principal**:
1. Usuario navega a módulo Clientes
2. Hace clic en "Agregar Cliente"
3. Completa formulario (mínimo: nombre)
4. Hace clic en "Guardar"
5. Sistema valida datos
6. Sistema guarda cliente
7. Sistema muestra mensaje de éxito
8. Sistema redirige a lista de clientes

**Flujos Alternativos**:
- 5a. Datos inválidos: Sistema muestra errores, usuario corrige
- 5b. Email inválido: Sistema muestra error específico

**Postcondiciones**: Cliente creado en base de datos

---

### CU-002: Crear Factura

**Actor**: Usuario del sistema  
**Precondiciones**: 
- Existe al menos un cliente
- Existe al menos un producto con stock

**Flujo Principal**:
1. Usuario navega a módulo Facturas
2. Hace clic en "Nueva Factura"
3. Selecciona cliente (búsqueda o lista)
4. Agrega productos (búsqueda, selecciona, especifica cantidad)
5. Sistema valida stock disponible
6. Sistema calcula totales automáticamente
7. Usuario revisa información
8. Usuario hace clic en "Guardar Factura"
9. Sistema genera número de factura
10. Sistema guarda factura y detalles
11. Sistema reduce stock de productos
12. Sistema muestra confirmación
13. Sistema redirige a detalle de factura

**Flujos Alternativos**:
- 5a. Stock insuficiente: Sistema muestra error, usuario ajusta cantidad
- 5b. Cliente no seleccionado: Sistema muestra error
- 5c. Sin productos: Sistema muestra error

**Postcondiciones**: 
- Factura creada
- Stock actualizado
- Historial actualizado

---

### CU-003: Buscar Factura

**Actor**: Usuario del sistema  
**Precondiciones**: Existen facturas en el sistema  
**Flujo Principal**:
1. Usuario navega a módulo Facturas
2. Usa filtros de búsqueda (fecha, cliente, estado)
3. Sistema muestra resultados filtrados
4. Usuario hace clic en una factura
5. Sistema muestra detalle completo

**Flujos Alternativos**:
- 2a. Sin resultados: Sistema muestra mensaje "No se encontraron facturas"
- 4a. Usuario exporta a PDF: Sistema genera y descarga PDF

---

### CU-004: Gestionar Inventario

**Actor**: Usuario del sistema  
**Precondiciones**: -  
**Flujo Principal**:
1. Usuario navega a módulo Inventario
2. Ve lista de productos
3. Opciones:
   - Agregar producto nuevo
   - Editar producto existente
   - Ver productos con stock bajo
   - Buscar producto

**Flujos Alternativos**:
- 3a. Stock bajo detectado: Sistema muestra alerta visual
- 3b. Editar stock: Usuario actualiza stock manualmente

---

## 12. Plan de Desarrollo

### 12.1 Fases del Proyecto

#### Fase 1: Setup y Base (Semana 1-2)
- Configuración del proyecto
- Estructura de directorios
- Configuración de Flask y FastAPI
- Setup de SQLite y SQLAlchemy
- Configuración de Tailwind CSS
- Setup de Electron
- Templates base

#### Fase 2: Módulo de Clientes (Semana 3)
- Modelo de datos Cliente
- CRUD completo
- Búsqueda
- UI con Tailwind y Alpine.js
- Validaciones

#### Fase 3: Módulo de Inventario (Semana 4)
- Modelo de datos Producto
- CRUD completo
- Control de stock
- Alertas de stock bajo
- UI completa

#### Fase 4: Módulo de Facturación (Semana 5-6)
- Modelos Factura y DetalleFactura
- Creación de facturas
- Cálculo automático
- Validaciones complejas
- UI de facturación

#### Fase 5: Módulo de Historial (Semana 7)
- Listado de facturas
- Búsqueda y filtros
- Vista detallada
- Exportación a PDF

#### Fase 6: Funcionalidades Adicionales (Semana 8)
- Dashboard
- Exportación a Excel
- Configuraciones
- Mejoras de UI/UX

#### Fase 7: Testing y Optimización (Semana 9)
- Tests unitarios
- Tests de integración
- Optimización de queries
- Corrección de bugs

#### Fase 8: Empaquetado y Distribución (Semana 10)
- Configuración de electron-builder
- Creación de instaladores
- Testing en diferentes plataformas
- Documentación final

### 12.2 Hitos

- **Hito 1**: Base del proyecto funcionando
- **Hito 2**: Módulo de Clientes completo
- **Hito 3**: Módulo de Inventario completo
- **Hito 4**: Módulo de Facturación completo
- **Hito 5**: Sistema funcional end-to-end
- **Hito 6**: Aplicación empaquetada y lista

### 12.3 Dependencias entre Tareas

- Módulo de Facturación depende de Clientes e Inventario
- Historial depende de Facturación
- Dashboard depende de todos los módulos
- Empaquetado depende de todo el sistema

---

## 13. Criterios de Aceptación

### 13.1 Funcionalidad

- ✅ Todos los módulos CRUD funcionan correctamente
- ✅ Las facturas se crean con todos los datos requeridos
- ✅ El stock se actualiza automáticamente al facturar
- ✅ Las búsquedas funcionan en todos los módulos
- ✅ Los filtros de historial funcionan correctamente
- ✅ La exportación a PDF genera documentos válidos
- ✅ Las validaciones previenen datos inválidos

### 13.2 Rendimiento

- ✅ La aplicación inicia en menos de 3 segundos
- ✅ Las operaciones CRUD completan en menos de 1 segundo
- ✅ Las búsquedas muestran resultados en menos de 500ms
- ✅ No hay lag perceptible en la UI

### 13.3 Usabilidad

- ✅ La interfaz es intuitiva sin capacitación
- ✅ Los mensajes de error son claros
- ✅ Las confirmaciones aparecen para acciones destructivas
- ✅ La navegación es consistente

### 13.4 Compatibilidad

- ✅ Funciona en Windows 10/11
- ✅ Funciona en Linux (Ubuntu 20.04+)
- ✅ Funciona en macOS 11+
- ✅ Los instaladores funcionan correctamente

### 13.5 Calidad de Código

- ✅ Código sigue estándares (PEP 8)
- ✅ Código documentado
- ✅ Arquitectura modular
- ✅ Sin código duplicado crítico

---

## 14. Riesgos y Mitigaciones

### 14.1 Riesgos Técnicos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Problemas de empaquetado Electron | Media | Alto | Probar empaquetado temprano, documentar proceso |
| Rendimiento con muchos datos | Baja | Medio | Implementar paginación, optimizar queries |
| Compatibilidad entre Flask y FastAPI | Baja | Medio | Separar claramente, usar diferentes puertos |
| Problemas de sincronización Flask-Electron | Media | Medio | Usar comunicación HTTP estándar, manejar errores |

### 14.2 Riesgos de Desarrollo

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Retrasos en desarrollo | Media | Medio | Buffer de tiempo, priorizar features críticas |
| Cambios de requisitos | Baja | Medio | Documentar bien, revisar con stakeholders |
| Problemas de integración | Media | Alto | Integración continua, tests tempranos |

### 14.3 Riesgos de Usuario

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Curva de aprendizaje | Baja | Bajo | UI intuitiva, documentación clara |
| Pérdida de datos | Baja | Crítico | Validaciones, backups, confirmaciones |

---

## 15. Glosario

- **CRUD**: Create, Read, Update, Delete - Operaciones básicas de datos
- **ORM**: Object-Relational Mapping - Mapeo objeto-relacional
- **API REST**: Interfaz de programación que sigue principios REST
- **Soft Delete**: Eliminación lógica (marcar como inactivo en lugar de borrar)
- **IVA/IVU**: Impuesto sobre el valor añadido/agregado
- **Stock**: Inventario disponible de productos
- **Factura**: Documento que registra una venta
- **Cliente**: Persona o entidad que realiza compras
- **Producto**: Artículo o servicio que se vende

---

## 16. Anexos

### Anexo A: Referencias Técnicas
- Documentación Flask: https://flask.palletsprojects.com/
- Documentación FastAPI: https://fastapi.tiangolo.com/
- Documentación Tailwind CSS: https://tailwindcss.com/
- Documentación Alpine.js: https://alpinejs.dev/
- Documentación Electron: https://www.electronjs.org/
- Documentación SQLAlchemy: https://www.sqlalchemy.org/

### Anexo B: Herramientas de Desarrollo
- Git para control de versiones
- VS Code como IDE recomendado
- Postman/Thunder Client para testing de APIs
- SQLite Browser para inspección de BD

---

**Fin del Documento PRD**

---

*Este documento es un documento vivo y puede ser actualizado según evolucione el proyecto.*

