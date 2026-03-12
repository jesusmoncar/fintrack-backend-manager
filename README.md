![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

# Gestor de Inversiones

Sistema web para gestionar, analizar y proyectar inversiones en criptomonedas y metales preciosos. Desarrollado con Flask y MySQL.

---

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Arrancar el proyecto](#arrancar-el-proyecto)
- [Arquitectura](#arquitectura)
- [Módulos y especificaciones técnicas](#módulos-y-especificaciones-técnicas)
- [Base de datos](#base-de-datos)
- [APIs externas](#apis-externas)
- [Solución de problemas](#solución-de-problemas)

---

## Requisitos

| Herramienta | Versión mínima |
|-------------|----------------|
| Python      | 3.8+           |
| Docker      | 20.10+         |
| Docker Compose | v2+         |

> No se necesita MySQL instalado localmente. Docker lo gestiona.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd gestor_inversiones
```

### 2. Crear el entorno virtual e instalar dependencias

```bash
python3 -m venv venv
source venv/bin/activate       # macOS/Linux
# venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia el archivo de ejemplo y edítalo:

```bash
cp .env.example .env
```

Edita `.env` con tus valores:

```env
FLASK_ENV=development
FLASK_PORT=5001

SECRET_KEY=cambia-esto-por-una-clave-segura

DB_HOST=localhost
DB_PORT=3307
DB_USER=root
DB_PASSWORD=root
DB_NAME=gestor_inversiones
```

> El puerto `3307` evita conflictos con instalaciones locales de MySQL.

---

## Arrancar el proyecto

### Paso 1 — Levantar la base de datos (Docker)

```bash
docker compose up -d
```

La primera vez inicializa la base de datos automáticamente desde `database.sql`.

### Paso 2 — Arrancar Flask

```bash
source venv/bin/activate
python run.py
```

La aplicación estará disponible en: **http://localhost:5001**

### Parar todo

```bash
# Parar Flask: Ctrl+C en la terminal

# Parar base de datos
docker compose down
```

> Los datos persisten en el volumen Docker `mysql_data`. Para borrar los datos: `docker compose down -v`

---

## Configuración

El fichero `config.py` gestiona tres entornos mediante la variable `FLASK_ENV`:

| Entorno       | `FLASK_ENV`   | Debug | Descripción                        |
|---------------|---------------|-------|------------------------------------|
| Desarrollo    | `development` | Sí    | Por defecto. Recarga automática.   |
| Producción    | `production`  | No    | Requiere `SECRET_KEY` en `.env`.   |
| Testing       | `testing`     | Sí    | Usa BBDD `gestor_inversiones_test`.|

---

## Arquitectura

El proyecto sigue una arquitectura en capas (Clean Architecture simplificada):

```
gestor_inversiones/
├── run.py                  # Punto de entrada
├── config.py               # Configuración por entornos
├── docker-compose.yml      # Infraestructura (MySQL)
├── database.sql            # Esquema de la base de datos
├── requirements.txt        # Dependencias Python
└── app/
    ├── __init__.py         # Flask Application Factory
    ├── models/             # Modelos de dominio (POJOs)
    │   ├── inversion.py
    │   └── historial.py
    ├── routes/             # Controladores HTTP (Blueprints)
    │   ├── main.py         # Dashboard principal
    │   ├── inversiones.py  # CRUD de inversiones
    │   ├── historial.py    # Historial de precios
    │   ├── ajustes.py      # Ajustes manuales
    │   └── analisis.py     # Análisis y proyecciones
    ├── services/           # Lógica de negocio
    │   ├── inversion_service.py
    │   ├── historial_service.py
    │   ├── precio_service.py
    │   ├── calculo_service.py
    │   ├── ajuste_service.py
    │   ├── proyeccion_service.py
    │   ├── recomendacion_service.py
    │   └── riesgo_service.py
    ├── utils/              # Utilidades transversales
    │   ├── database.py     # Conexión y helpers de MySQL
    │   ├── formatters.py   # Formateo de datos
    │   └── validators.py   # Validación de entradas
    └── templates/          # HTML (Jinja2 + Bootstrap 5)
```

---

## Módulos y especificaciones técnicas

### `app/__init__.py` — Application Factory

Crea y configura la instancia Flask. Registra blueprints, filtros de template y manejadores de errores. Patrón Factory para facilitar testing y múltiples entornos.

**Filtros de template registrados:**
- `currency` — Formatea a euros: `1234.56` → `€1.234,56`
- `percentage` — Formatea con signo: `5.2` → `+5.20%`
- `number` — Decimales configurables

---

### `routes/` — Controladores (Blueprints Flask)

| Blueprint        | Prefijo URL      | Descripción                              |
|------------------|------------------|------------------------------------------|
| `main_bp`        | `/`              | Dashboard con resumen del portfolio      |
| `inversiones_bp` | `/inversiones`   | CRUD completo de inversiones             |
| `historial_bp`   | `/historial`     | Historial de precios y gráficos          |
| `ajustes_bp`     | `/ajustes`       | Ajustes manuales de valor                |
| `analisis_bp`    | `/analisis`      | Análisis de riesgo y proyecciones        |

---

### `services/` — Lógica de negocio

#### `InversionService`
Gestión completa del CRUD de inversiones.

- `get_all_with_current_data()` — Obtiene inversiones con JOIN al último precio del historial. Aplica ajustes manuales a la ganancia/pérdida.
- `create(nombre, cantidad, precio_compra, fecha_compra, inversion_total, inversion_neta)`
- `update(inversion_id, **kwargs)` — Actualización dinámica de campos.
- `delete(inversion_id)` — Elimina inversión y su historial en cascada.

#### `HistorialService`
Gestión del historial de precios.

- Guarda un precio por fecha por inversión (restricción `UNIQUE`).
- Si ya existe un registro para esa fecha, lo actualiza (upsert).
- `get_for_chart(inversion_id, limit)` — Devuelve datos ordenados para gráficos.

#### `PrecioService`
Obtención de precios en tiempo real desde APIs externas.

- **Criptomonedas** → CoinGecko API (`/simple/price`, vs_currency: EUR)
- **Metales** → Yahoo Finance API (futuros: `GC=F`, `SI=F`, `PL=F`, `PA=F`)
- Los metales se convierten de USD a EUR aplicando el spread de Revolut (1.5%).

**Activos soportados:**

| Tipo | Activos |
|------|---------|
| Cripto | Bitcoin, Ethereum, Solana, Cardano, XRP, Polkadot, Dogecoin, Avalanche, Chainlink, Polygon |
| Metales | Oro, Plata, Platino, Paladio |

#### `RiesgoService`
Análisis de riesgo del portfolio completo.

- **Volatilidad** — Calculada sobre los últimos 30 registros de historial.
- **Max Drawdown** — Caída máxima desde el pico.
- **Concentración** — Índice Herfindahl-Hirschman (HHI) normalizado.
- **Score de riesgo** — Ponderación de los 4 factores anteriores.

| Score | Nivel | Color |
|-------|-------|-------|
| 0–39  | Bajo  | Verde |
| 40–69 | Medio | Amarillo |
| 70+   | Alto  | Rojo |

#### `ProyeccionService`
Proyecciones de valor futuro basadas en historial.

- Usa los últimos 90 días de historial.
- Calcula tasa de crecimiento anualizada entre el primer y último valor.
- Genera 3 escenarios × 4 horizontes temporales:

| Escenario    | Factor |
|--------------|--------|
| Conservador  | ×0.5   |
| Moderado     | ×1.0   |
| Optimista    | ×1.5   |

| Horizonte |
|-----------|
| 30 días   |
| 90 días   |
| 180 días  |
| 365 días  |

#### `AjusteService`
Permite corregir manualmente el valor de una inversión (por ejemplo, para reflejar comisiones o conversiones no capturadas automáticamente). El ajuste se suma a la ganancia/pérdida calculada.

#### `CalculoService`
Funciones matemáticas puras reutilizadas por otros servicios:
- `calcular_volatilidad(precios)` — Desviación estándar porcentual.
- `calcular_drawdown(precios)` — Caída máxima desde el pico histórico.
- `proyectar_valor_futuro(valor, tasa, años)` — Interés compuesto.

#### `RecomendacionService`
Genera sugerencias personalizadas basadas en el análisis de riesgo y diversificación del portfolio.

---

### `utils/` — Utilidades

#### `database.py`
- `conectar_db()` — Conexión MySQL con parámetros del contexto Flask (`current_app.config`).
- `get_db_cursor(commit)` — Context manager que gestiona apertura/cierre de conexión y rollback automático en caso de error.
- `execute_query(query, params, fetch_one, fetch_all, commit)` — Wrapper genérico para ejecutar queries.

#### `validators.py`
- Valida números positivos, fechas (`%Y-%m-%d`), nombres de activos (alfanumérico + espacios + guiones).
- `sanitize_string(text, max_length)` — Limpia espacios y trunca strings.

#### `formatters.py`
- `currency(value)` — Formato moneda con símbolo.
- `percentage(value)` — Porcentaje con signo.
- `large_number(value)` — Notación K/M/B.
- `date_spanish(date)` — Fecha en español: "25 de diciembre de 2025".

---

## Base de datos

### Esquema

```sql
inversiones
├── id              INT AUTO_INCREMENT PK
├── nombre          VARCHAR(100)
├── cantidad        DECIMAL(18,8)      -- Unidades del activo
├── precio_compra   DECIMAL(18,8)      -- Precio unitario en EUR
├── fecha_compra    DATE
├── inversion_total DECIMAL(18,2)      -- cantidad × precio_compra × spread
├── inversion_neta  DECIMAL(18,2)      -- Sin comisiones
├── ajuste_manual   DECIMAL(18,2)      -- Corrección manual
└── created_at      TIMESTAMP

historial_precios
├── id              INT AUTO_INCREMENT PK
├── inversion_id    INT FK → inversiones(id) CASCADE DELETE
├── fecha           DATE
├── precio_actual   DECIMAL(18,8)
├── valor_actual    DECIMAL(18,2)      -- cantidad × precio_actual
├── ganancia_perdida DECIMAL(18,2)     -- valor_actual - inversion_total
├── created_at      TIMESTAMP
└── UNIQUE(inversion_id, fecha)        -- Un precio por día por activo
```

### Comandos útiles Docker

```bash
# Ver tablas
docker exec -it gestor_inversiones_db mysql -uroot -proot -e "SHOW TABLES FROM gestor_inversiones;"

# Conectarse al cliente MySQL
docker exec -it gestor_inversiones_db mysql -uroot -proot gestor_inversiones

# Importar esquema manualmente
docker exec -i gestor_inversiones_db mysql -uroot -proot < database.sql

# Ver logs del contenedor
docker compose logs -f
```

---

## APIs externas

| API | Uso | Autenticación | Rate limit |
|-----|-----|---------------|------------|
| [CoinGecko](https://www.coingecko.com/api/documentation) | Precios cripto en EUR | Sin API key (plan free) | 10–30 req/min |
| [Yahoo Finance](https://finance.yahoo.com) | Precios futuros de metales | Sin API key | Sin límite oficial |

> Las llamadas a APIs tienen timeout de 10 segundos. Si fallan, el precio devuelto es `None` y la app continúa sin bloquearse.

---

## Tecnologías utilizadas

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Backend | Flask | 3.0.0 |
| WSGI | Werkzeug | 3.0.1 |
| Base de datos | MySQL | 8.0 |
| Driver BD | mysql-connector-python | 8.2.0 |
| HTTP client | requests | 2.31.0 |
| Finance data | yfinance | 0.2.33 |
| Variables entorno | python-dotenv | 1.0.0 |
| Frontend | Bootstrap 5 + Jinja2 | — |
| Contenedores | Docker + Docker Compose | — |

---

## Solución de problemas

### El contenedor Docker no arranca — puerto 3306 ocupado

```bash
# Parar MySQL local si está corriendo
brew services stop mysql

# O usar el puerto alternativo 3307 (ya configurado por defecto)
docker compose up -d
```

### Flask no conecta a la base de datos

```bash
# Verificar que el contenedor está corriendo
docker compose ps

# Esperar a que MySQL esté listo (primera vez puede tardar ~15s)
docker compose logs mysql
```

### Error: ModuleNotFoundError

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Resetear la base de datos

```bash
docker compose down -v        # Borra el volumen con todos los datos
docker compose up -d          # Recrea desde cero con database.sql
```
