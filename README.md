# Python Orientado al Dato — Proyecto Final

Proyecto de análisis de datos sobre un dataset de e-commerce brasileño (Olist). Incluye resolución de ejercicios propuestos y métricas personalizadas, todo visualizado mediante un dashboard interactivo construido con **Streamlit**.

---

## Contenido del proyecto

### Ejercicios propuestos

| Ejercicio | Descripción |
|-----------|-------------|
| **Ejercicio 1** | Clientes únicos por estado y ciudad, con filtro por rango de fechas |
| **Ejercicio 2** | Pedidos por ciudad, con porcentaje sobre el total y ratio pedidos/cliente |
| **Ejercicio 3** | Análisis de retrasos en pedidos: pedidos que llegan tarde, porcentaje de pedidos retrasados, tiempo medio de retraso y autodiagnóstico |
| **Ejercicio 4** | Reviews y satisfacción del cliente, separando pedidos entregados a tiempo de los cancelados |

### Métricas personalizadas

| Métrica | Descripción |
|---------|-------------|
| **Métrica Personalizada 1** | Distribución de ventas por categoría de producto en porcentaje sobre el total, con gráfico de barras y diagrama circular |
| **Métrica Personalizada 2** | Análisis de métodos de pago: usos totales y porcentaje de cada método, con gráfico de barras y diagrama circular |

---

## Estructura del proyecto

```
Proyecto/
├── app/
│   ├── main.py                          # Punto de entrada de Streamlit
│   ├── exs/                             # Capa lógica
│   │   ├── ex1.py ... ex4.py
│   │   ├── pers_metric_1.py
│   │   └── pers_metric_2.py
│   ├── streamlit_pages/                 # Capa de presentación (UI)
│   │   ├── ex1_executable.py ... ex4_executable.py
│   │   ├── pers_metric_1_executable.py
│   │   └── pers_metric_2_executable.py
│   ├── seeders/                         # Capa de datos
│   │   └── load_data.py
│   └── jupyter/                         # Notebooks exploratorios
│       ├── notebook_abel.ipynb
│       └── notebook_pedro.ipynb
├── documents/
│   ├── datasets/                        # CSVs del dataset
│   ├── documentation/                   # Documentación por ejercicio (.md)
│   └── model/                           # Modelo de datos
└── requirements.txt                     # Requerimientos del Proyecto
```

---

## Arquitectura por capas

El proyecto sigue una separación clara en tres capas:

### Capa de datos — `seeders/load_data.py`
Carga los datasets CSV y los sirve en caché mediante `@st.cache_data`. Evita releer en disco en cada interacción del usuario.

### Capa lógica — `exs/`
Contiene toda la lógica de negocio y transformación de datos: filtros, merges, agrupaciones y cálculos. Cada ejercicio y métrica tiene su propio módulo. No tiene dependencias con Streamlit.

### Capa de presentación — `streamlit_pages/`
Construye el dashboard: inputs, tablas y gráficos. Llama a la capa lógica y renderiza los resultados. Toda la interacción con Streamlit ocurre aquí.

---

## Flujo de trabajo en GitHub

Se ha seguido un flujo **`dev` → `main`** mediante Pull Requests:

1. Todo el desarrollo se realiza sobre la rama `dev`.
2. Cuando una funcionalidad está completa y revisada, se abre una Pull Request de `dev` a `main`.
3. `main` siempre refleja el estado estable del proyecto.

---

## Tecnologías utilizadas

- **Python 3.11 - 3.12**
- **Pandas** — manipulación y análisis de datos
- **NumPy** — operaciones numéricas
- **Streamlit** — dashboard interactivo
- **Matplotlib** — visualizaciones personalizadas

---

## Cómo ejecutar el proyecto

### 1. Crear el entorno virtual e instalar dependencias

Desde la raíz del proyecto, ejecuta los siguientes comandos:

```bash
python -m venv .venv
```

Activa el entorno virtual:

- **Windows:**
```bash
.venv\Scripts\activate
```
- **Linux/Mac:**
```bash
source .venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

### 2. Ejecutar el dashboard

Una vez instaladas las dependencias, navega a la carpeta `app` y lanza Streamlit:

```bash
cd app
streamlit run main.py
```

La aplicación estará disponible en `http://localhost:8501`.

---

## Autores

Proyecto creado por **Pedro Arriero Domec** y **Abel González Palencia**.

---
