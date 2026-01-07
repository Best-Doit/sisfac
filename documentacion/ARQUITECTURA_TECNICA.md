# Arquitectura Técnica - SISFAC

## Documento de Arquitectura del Sistema

**Versión:** 1.0  
**Fecha:** 2024  
**Autor:** Equipo de Desarrollo

---

## Tabla de Contenidos

1. [Visión General de la Arquitectura](#visión-general-de-la-arquitectura)
2. [Arquitectura de Alto Nivel](#arquitectura-de-alto-nivel)
3. [Arquitectura de Capas](#arquitectura-de-capas)
4. [Flujo de Datos](#flujo-de-datos)
5. [Comunicación entre Componentes](#comunicación-entre-componentes)
6. [Gestión de Estado](#gestión-de-estado)
7. [Manejo de Errores](#manejo-de-errores)
8. [Seguridad](#seguridad)
9. [Rendimiento y Optimización](#rendimiento-y-optimización)
10. [Escalabilidad](#escalabilidad)

---

## 1. Visión General de la Arquitectura

SISFAC sigue una arquitectura híbrida que combina:

- **Arquitectura de Capas**: Separación clara de responsabilidades
- **Arquitectura Cliente-Servidor**: Electron (cliente) + Flask/FastAPI (servidor)
- **Arquitectura Modular**: Módulos independientes y reutilizables
- **Patrón MVC/MVP**: Separación de lógica, datos y presentación

### Principios Arquitectónicos

1. **Separación de Responsabilidades**: Cada capa tiene una responsabilidad única
2. **Bajo Acoplamiento**: Módulos independientes con interfaces claras
3. **Alta Cohesión**: Funcionalidades relacionadas agrupadas
4. **Reutilización**: Componentes y servicios reutilizables
5. **Testabilidad**: Código fácil de testear
6. **Mantenibilidad**: Código claro y bien documentado

---

## 2. Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                     │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Electron Application                       │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  Browser Window (Chromium)                    │  │  │
│  │  │  ┌──────────────────────────────────────────┐ │  │  │
│  │  │  │  Frontend Web Application                │ │  │  │
│  │  │  │  - HTML5 (Estructura)                    │ │  │  │
│  │  │  │  - Tailwind CSS (Estilos)                │ │  │  │
│  │  │  │  - Alpine.js (Interactividad)            │ │  │  │
│  │  │  │  - Vanilla JS (Utilidades)               │ │  │  │
│  │  │  │  - Templates Jinja2 (Flask)             │ │  │  │
│  │  │  └──────────────────────────────────────────┘ │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │                                                       │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  Main Process (Node.js)                       │  │  │
│  │  │  - Gestión de ventanas                        │  │  │
│  │  │  - Gestión de procesos                        │  │  │
│  │  │  - Inicio de servidor Python                  │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE APLICACIÓN                        │
│                                                             │
│  ┌──────────────────────┐        ┌──────────────────────┐  │
│  │   Flask Application  │        │  FastAPI Application │  │
│  │                      │        │                      │  │
│  │  - Server-Side       │        │  - REST API          │  │
│  │    Rendering         │        │  - Async Support     │  │
│  │  - Templates Jinja2  │        │  - OpenAPI Docs      │  │
│  │  - Static Files      │        │  - Pydantic Models   │  │
│  │  - Session Mgmt      │        │                      │  │
│  └──────────┬───────────┘        └──────────┬───────────┘  │
│             │                                │              │
│             └────────────┬───────────────────┘              │
│                          │                                  │
│             ┌────────────▼──────────────┐                   │
│             │   Business Logic Layer   │                   │
│             │                          │                   │
│             │  ┌────────────────────┐  │                   │
│             │  │ ClienteService     │  │                   │
│             │  │ ProductoService   │  │                   │
│             │  │ FacturaService    │  │                   │
│             │  │ ReportService     │  │                   │
│             │  └────────────────────┘  │                   │
│             │                          │                   │
│             │  ┌────────────────────┐  │                   │
│             │  │ Validators         │  │                   │
│             │  │ Formatters         │  │                   │
│             │  │ Helpers            │  │                   │
│             │  └────────────────────┘  │                   │
│             └────────────┬──────────────┘                   │
└──────────────────────────┼─────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────┐
│              CAPA DE ACCESO A DATOS                        │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              SQLAlchemy ORM                          │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  Models                                        │  │  │
│  │  │  - Cliente                                     │  │  │
│  │  │  - Producto                                   │  │  │
│  │  │  - Factura                                    │  │  │
│  │  │  - DetalleFactura                             │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │                                                       │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  Database Session Management                  │  │  │
│  │  │  - Connection Pooling                         │  │  │
│  │  │  - Transaction Management                     │  │  │
│  │  │  - Query Optimization                         │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────┐
│                    BASE DE DATOS                           │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              SQLite Database                         │  │
│  │  - sisfac.db (Archivo local)                        │  │
│  │  - ACID Compliance                                  │  │
│  │  - Foreign Key Constraints                         │  │
│  │  - Indexes Optimized                               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Arquitectura de Capas

### 3.1 Capa de Presentación (Frontend)

#### Responsabilidades
- Renderizar la interfaz de usuario
- Capturar interacciones del usuario
- Mostrar datos de manera clara
- Proporcionar feedback visual

#### Componentes Principales

**Electron Main Process**
- Gestión del ciclo de vida de la aplicación
- Inicio y control del servidor Python
- Gestión de ventanas
- Manejo de eventos del sistema

**Electron Renderer Process**
- Renderiza el contenido web
- Ejecuta JavaScript del frontend
- Comunica con el main process cuando es necesario

**Frontend Web (HTML/CSS/JS)**
- **HTML5**: Estructura semántica
- **Tailwind CSS**: Estilos utilitarios
- **Alpine.js**: Reactividad y estado local
- **Vanilla JS**: Funcionalidades adicionales
- **Templates Jinja2**: Renderizado del servidor (Flask)

#### Patrones Utilizados
- **Component Pattern**: Componentes Alpine.js reutilizables
- **Template Pattern**: Templates base con Jinja2
- **Observer Pattern**: Eventos y reactividad de Alpine.js

### 3.2 Capa de Aplicación (Backend)

#### Flask Application

**Responsabilidades:**
- Server-side rendering de páginas
- Manejo de rutas y vistas
- Servir archivos estáticos
- Gestión de sesiones (si aplica)

**Estructura:**
```
app/
├── routes/          # Controladores de rutas
│   ├── clientes.py
│   ├── inventario.py
│   ├── facturas.py
│   └── dashboard.py
├── templates/       # Templates Jinja2
└── static/          # Archivos estáticos
```

#### FastAPI Application

**Responsabilidades:**
- Proporcionar API REST
- Validación de datos con Pydantic
- Documentación automática (OpenAPI)
- Soporte asíncrono

**Estructura:**
```
app/
├── api/
│   ├── v1/
│   │   ├── clientes.py
│   │   ├── productos.py
│   │   └── facturas.py
└── schemas/         # Modelos Pydantic
```

#### Business Logic Layer

**Responsabilidades:**
- Implementar reglas de negocio
- Validaciones complejas
- Cálculos (totales, IVA)
- Generación de números de factura
- Lógica de negocio reutilizable

**Servicios:**
- `ClienteService`: Lógica de clientes
- `ProductoService`: Lógica de productos e inventario
- `FacturaService`: Lógica de facturación
- `ReportService`: Generación de reportes

**Patrones:**
- **Service Layer Pattern**: Encapsula lógica de negocio
- **Strategy Pattern**: Diferentes estrategias de cálculo (opcional)

### 3.3 Capa de Acceso a Datos (DAL)

#### Responsabilidades
- Abstracción de la base de datos
- Mapeo objeto-relacional
- Gestión de transacciones
- Optimización de queries

#### SQLAlchemy ORM

**Modelos:**
- Representan tablas de la base de datos
- Relaciones entre entidades
- Validaciones a nivel de modelo

**Session Management:**
- Pool de conexiones
- Gestión de transacciones
- Context managers para seguridad

**Queries:**
- Queries optimizadas con índices
- Eager loading para relaciones
- Lazy loading cuando es apropiado

### 3.4 Capa de Datos

#### SQLite Database

**Características:**
- Base de datos embebida
- Archivo local (`sisfac.db`)
- ACID compliance
- Sin necesidad de servidor

**Optimizaciones:**
- Índices en campos de búsqueda
- Foreign key constraints
- Check constraints para validación
- Normalización (3NF)

---

## 4. Flujo de Datos

### 4.1 Flujo de Lectura (GET)

```
Usuario → Frontend → Flask/FastAPI → Service → DAL → Database
                ←                    ←         ←      ←
```

1. Usuario interactúa con la UI
2. Frontend hace request HTTP (GET)
3. Flask/FastAPI recibe request
4. Service obtiene datos del DAL
5. DAL ejecuta query en Database
6. Datos fluyen de vuelta por las capas
7. Frontend renderiza los datos

### 4.2 Flujo de Escritura (POST/PUT/DELETE)

```
Usuario → Frontend → Flask/FastAPI → Service → DAL → Database
                ←                    ←         ←      ←
```

1. Usuario completa formulario
2. Frontend valida en cliente
3. Frontend envía datos (POST/PUT)
4. Flask/FastAPI valida datos
5. Service aplica lógica de negocio
6. Service llama al DAL
7. DAL inicia transacción
8. DAL ejecuta operación
9. DAL confirma transacción
10. Service retorna resultado
11. Flask/FastAPI retorna respuesta
12. Frontend muestra confirmación

### 4.3 Flujo de Facturación (Ejemplo Completo)

```
1. Usuario selecciona cliente
   → Frontend: Muestra información del cliente

2. Usuario agrega productos
   → Frontend: Valida stock disponible (AJAX)
   → FastAPI: /api/v1/productos/{id}/stock
   → Service: Verifica stock
   → DAL: Query de stock
   → Database: Retorna stock
   → Frontend: Muestra/oculta producto según stock

3. Usuario especifica cantidades
   → Frontend: Calcula subtotales (JavaScript)
   → Frontend: Calcula totales (JavaScript)

4. Usuario guarda factura
   → Frontend: Valida formulario completo
   → Frontend: POST /api/v1/facturas
   → FastAPI: Valida con Pydantic
   → Service: 
      - Genera número de factura
      - Valida stock para todos los productos
      - Calcula totales
   → DAL: Inicia transacción
   → DAL: INSERT factura
   → DAL: INSERT detalles
   → DAL: UPDATE stock (para cada producto)
   → DAL: COMMIT transacción
   → Service: Retorna factura creada
   → FastAPI: Retorna JSON
   → Frontend: Muestra confirmación
   → Frontend: Redirige a detalle de factura
```

---

## 5. Comunicación entre Componentes

### 5.1 Electron ↔ Flask/FastAPI

**Protocolo:** HTTP (REST)

**En Desarrollo:**
- Flask/FastAPI corre en `localhost:5000`
- Electron abre ventana apuntando a `http://localhost:5000`

**En Producción:**
- Electron inicia servidor Python como proceso hijo
- Servidor se ejecuta en puerto local (ej: 5000)
- Electron carga aplicación desde localhost

**Comunicación:**
```javascript
// Electron Renderer
fetch('http://localhost:5000/api/v1/clientes')
  .then(response => response.json())
  .then(data => {
    // Actualizar UI con Alpine.js
  });
```

### 5.2 Frontend ↔ Backend

#### Flask (Server-Side Rendering)
- Frontend recibe HTML renderizado
- Formularios se envían vía POST tradicional
- Redirecciones después de acciones
- Menos interactividad, más simple

#### FastAPI (API REST)
- Frontend hace requests AJAX/Fetch
- Backend retorna JSON
- Frontend actualiza UI dinámicamente
- Más interactividad, mejor UX

#### Híbrido (Recomendado)
- Flask para páginas principales (SSR)
- FastAPI para operaciones AJAX (API)
- Mejor de ambos mundos

### 5.3 Service ↔ DAL

**Patrón:** Repository Pattern (opcional) o acceso directo

```python
# Service llama al DAL
class FacturaService:
    def __init__(self, db_session):
        self.db = db_session
    
    def crear_factura(self, datos):
        # Lógica de negocio
        # Validaciones
        # Cálculos
        
        # Llamada al DAL
        factura = FacturaModel.create(...)
        return factura
```

### 5.4 DAL ↔ Database

**SQLAlchemy ORM:**
- Abstracción de SQL
- Mapeo objeto-relacional
- Gestión automática de conexiones

```python
# DAL usa SQLAlchemy
session.query(Cliente).filter_by(id=cliente_id).first()
```

---

## 6. Gestión de Estado

### 6.1 Estado del Frontend

#### Alpine.js State
- Estado local por componente
- Reactividad automática
- No requiere gestión global compleja

```javascript
Alpine.data('clientes', () => ({
    clientes: [],
    loading: false,
    
    async cargarClientes() {
        this.loading = true;
        const response = await fetch('/api/v1/clientes');
        this.clientes = await response.json();
        this.loading = false;
    }
}));
```

#### Estado del Servidor (Flask)
- Sesiones si es necesario (opcional)
- Estado en base de datos (persistente)
- No requiere estado global complejo

### 6.2 Estado de la Base de Datos

- Única fuente de verdad
- Estado persistente
- Transacciones para consistencia

### 6.3 Sincronización

- Frontend consulta backend cuando necesita datos
- No hay sincronización bidireccional compleja
- Simplicidad sobre complejidad

---

## 7. Manejo de Errores

### 7.1 Estrategia de Manejo de Errores

#### Frontend
- Validación en cliente (UX rápida)
- Manejo de errores de red
- Mensajes de error amigables
- Feedback visual claro

```javascript
try {
    const response = await fetch('/api/v1/clientes', {
        method: 'POST',
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        const error = await response.json();
        // Mostrar error al usuario
        mostrarError(error.message);
        return;
    }
    
    // Éxito
    mostrarExito('Cliente creado correctamente');
} catch (error) {
    // Error de red
    mostrarError('Error de conexión');
}
```

#### Backend (Flask)
- Manejo de excepciones global
- Logging de errores
- Respuestas HTTP apropiadas
- Mensajes de error claros

```python
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
```

#### Backend (FastAPI)
- Excepciones HTTP estándar
- Validación automática con Pydantic
- Respuestas JSON estructuradas

```python
from fastapi import HTTPException

@app.post("/api/v1/clientes")
async def crear_cliente(cliente: ClienteCreate):
    try:
        # Lógica
        return cliente_creado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

#### DAL
- Manejo de errores de base de datos
- Rollback de transacciones en error
- Logging de errores SQL

```python
try:
    db.session.add(factura)
    db.session.commit()
except SQLAlchemyError as e:
    db.session.rollback()
    logger.error(f"Error al guardar factura: {e}")
    raise
```

### 7.2 Tipos de Errores

1. **Errores de Validación**
   - Input inválido del usuario
   - HTTP 400 (Bad Request)
   - Mensaje específico del error

2. **Errores de Negocio**
   - Regla de negocio violada (ej: stock insuficiente)
   - HTTP 400 o 422
   - Mensaje explicativo

3. **Errores de Recurso No Encontrado**
   - Cliente/producto/factura no existe
   - HTTP 404
   - Mensaje claro

4. **Errores del Servidor**
   - Error interno inesperado
   - HTTP 500
   - Log detallado, mensaje genérico al usuario

5. **Errores de Red**
   - Problemas de conexión
   - Timeout
   - Reintento automático (opcional)

---

## 8. Seguridad

### 8.1 Validación de Inputs

#### Frontend
- Validación en cliente (UX)
- No confiable para seguridad
- Sanitización básica

#### Backend
- Validación obligatoria en servidor
- Sanitización de inputs
- Validación con Pydantic (FastAPI)
- Validación con WTForms (Flask)

### 8.2 Protección SQL Injection

- SQLAlchemy ORM previene inyección SQL
- Parámetros enlazados automáticamente
- No usar SQL crudo con strings

### 8.3 Protección XSS

- Jinja2 escapa automáticamente
- No usar `|safe` a menos que sea necesario
- Validar y sanitizar datos antes de mostrar

### 8.4 CORS (Cross-Origin Resource Sharing)

- En desarrollo: Permitir localhost
- En producción: Restringir a origen específico
- Configurar en Flask/FastAPI

### 8.5 Manejo de Sesiones (Si aplica)

- Tokens seguros
- Expiración de sesiones
- HTTPS en producción (si hay red)

### 8.6 Logging y Auditoría

- Log de operaciones críticas
- No loggear datos sensibles
- Rotación de logs

---

## 9. Rendimiento y Optimización

### 9.1 Optimización de Base de Datos

#### Índices
- Índices en campos de búsqueda frecuente
- Índices en foreign keys
- Índices en campos de filtrado

#### Queries
- Eager loading para relaciones necesarias
- Lazy loading cuando es apropiado
- Evitar N+1 queries
- Usar `select_related` / `joinedload`

#### Paginación
- Paginar listas grandes
- Límite de resultados por página
- Carga bajo demanda

### 9.2 Optimización del Frontend

#### Assets
- Minificar CSS y JS en producción
- Comprimir imágenes
- Cache de assets estáticos

#### Rendering
- Lazy loading de componentes
- Virtual scrolling para listas grandes
- Debounce en búsquedas

#### Alpine.js
- Usar `x-data` eficientemente
- Evitar cálculos pesados en templates
- Cache de datos cuando sea posible

### 9.3 Optimización del Backend

#### Caching
- Cache de consultas frecuentes (opcional)
- Cache de resultados de cálculos
- Redis para cache distribuido (futuro)

#### Async Operations
- FastAPI soporta async
- Operaciones I/O no bloqueantes
- Mejor rendimiento con muchas requests

#### Connection Pooling
- SQLAlchemy maneja pooling automáticamente
- Configurar tamaño del pool según necesidad

### 9.4 Monitoreo

- Logging de operaciones lentas
- Métricas de tiempo de respuesta
- Identificar cuellos de botella

---

## 10. Escalabilidad

### 10.1 Escalabilidad Actual (Fase 1)

- **Datos**: Hasta ~100,000 registros sin problemas
- **Usuarios**: Aplicación de escritorio, un usuario por instancia
- **Rendimiento**: Suficiente para operaciones normales

### 10.2 Escalabilidad Futura

#### Horizontal (Si se migra a web)
- Múltiples instancias de Flask/FastAPI
- Load balancer
- Base de datos compartida (PostgreSQL)

#### Vertical
- Mejor hardware
- Optimizaciones de código
- Mejor uso de recursos

#### Base de Datos
- Migración a PostgreSQL para múltiples usuarios
- Replicación para lectura
- Particionamiento de tablas grandes

### 10.3 Consideraciones de Diseño

- Arquitectura modular facilita escalabilidad
- Separación de concerns permite optimizar por partes
- APIs REST facilitan migración a arquitectura distribuida

---

## 11. Diagramas Adicionales

### 11.1 Diagrama de Secuencia - Crear Factura

```
Usuario    Frontend    Flask/FastAPI    Service    DAL    Database
   |           |            |              |        |         |
   |--click-->|            |              |        |         |
   |           |--POST---->|              |        |         |
   |           |            |--validate-->|        |         |
   |           |            |              |--get-->|         |
   |           |            |              |        |--query->|
   |           |            |              |        |<--data--|
   |           |            |              |<--ok---|         |
   |           |            |              |--calc->|         |
   |           |            |              |--save->|         |
   |           |            |              |        |--trans->|
   |           |            |              |        |--insert>|
   |           |            |              |        |--update>|
   |           |            |              |        |<--ok----|
   |           |            |              |<--id----|         |
   |           |            |<--factura----|        |         |
   |           |<--JSON-----|              |        |         |
   |<--success-|            |              |        |         |
```

### 11.2 Diagrama de Componentes

```
┌─────────────┐
│   Electron  │
└──────┬──────┘
       │
       ├─────────────────┐
       │                 │
┌──────▼──────┐   ┌──────▼──────┐
│   Flask     │   │   FastAPI   │
│  (SSR)      │   │  (REST API) │
└──────┬──────┘   └──────┬──────┘
       │                 │
       └────────┬─────────┘
                │
       ┌────────▼────────┐
       │   Services      │
       └────────┬────────┘
                │
       ┌────────▼────────┐
       │   SQLAlchemy    │
       └────────┬────────┘
                │
       ┌────────▼────────┐
       │    SQLite       │
       └─────────────────┘
```

---

**Fin del Documento de Arquitectura Técnica**

