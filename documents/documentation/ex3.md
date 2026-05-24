# Ejercicio 3 — Análisis de retrasos en pedidos

## Descripción del ejercicio

El objetivo de este ejercicio es analizar los pedidos que han llegado tarde a los clientes. Se define un retraso real como aquel donde la fecha de entrega al cliente es estrictamente mayor que la fecha estimada de entrega, y la diferencia en días es mayor a 0. Esta segunda condición es importante: sin ella, se podrían incluir pedidos que técnicamente se entregaron el mismo día pero a una hora posterior a la estimada, lo que desde nuestro punto de vista no se ha considerado un retraso real.

El ejercicio se divide en tres métricas principales y un apartado de autodiagnóstico:

1. Número de pedidos que llegan tarde por ciudad.
2. Porcentaje de pedidos retrasados respecto al total de pedidos de cada ciudad.
3. Media de días de retraso por ciudad.
4. Autodiagnóstico con análisis por franjas de retraso.

Los datasets que se usan son `orders` y `customers`, y para el autodiagnóstico también se usa `order_reviews`.

---

## Resolución del ejercicio

### Capa de datos — `seeders/load_data.py`

Se cargan los dataframes en caché de `orders`, `customers` y `order_reviews`.

### Capa lógica — `exs/ex3.py`

Se definen varios métodos que se encadenan entre sí. El método base del que se parte es de `obtain_late_orders_per_city()`:

- `obtain_late_orders_per_city()`: Convierte las fechas de entrega a datetime, calcula la diferencia de días entre la fecha de entrega real y la estimada, y filtra los pedidos que cumplen las condiciones de retraso real. Después se hace un merge con los clientes para acceder a la ciudad y el estado, y crea una columna normalizada `state_city` con el formato `"Ciudad (Estado)"`.

A partir de este método base se construyen el resto:

- `late_orders_per_city(number)`: Agrupa por `state_city`, cuenta los pedidos retrasados y devuelve los N primeros ordenados de forma descendente.
- `late_orders_percentage(number)`: Hace un merge entre el total de pedidos por ciudad y los pedidos retrasados por ciudad, usando un left join para conservar todas las ciudades. Calcula el porcentaje de retraso como `(pedidos_retrasados / total_pedidos) * 100` y rellena los nulos con 0 para evitar valores anómalos.
- `obtain_late_orders_days()`: Añade al DataFrame base una columna `late_days` con los días de retraso de cada pedido.
- `late_orders_days_mean(number)`: Agrupa por ciudad y calcula la media de días de retraso, devolviendo los N primeros ordenados de forma descendente.
- `obtain_late_orders_count()`: Divide los pedidos retrasados en franjas / intervalos usando `pd.cut()`: 0-2 días, 2-5 días, 5-10 días, 10-20 días y 20+ días. Devuelve el conteo de pedidos por franja / intervalos.
- `obtain_late_orders_rating()`: Hace un merge de los pedidos retrasados con las reviews por `order_id`, aplica las mismas franjas / intervalos que el método anterior y calcula la media de puntuaciones por cada franja / intervalos.
- `obtain_carrier_customer_days()`: Calcula dos tiempos medios: los días que tarda el vendedor en enviar el pedido al transportista (`order_purchase_timestamp` → `order_delivered_carrier_date`) y los días que tarda el transportista en entregar el pedido al cliente (`order_delivered_carrier_date` → `order_delivered_customer_date`), realizando una resta de ambas fechas y quedándonos los días, para más adelante realizar medias y poder dictaminar las causas de los retrasos.

### Capa gráfica — `streamlit_pages/ex3_executable.py`

Se definen cuatro funciones, una por cada sub-métrica:

- `exercise3_metric_1()`: Gráfico de barras con el número de pedidos retrasados por ciudad.
- `exercise3_metric_2()`: Gráfico de barras con el porcentaje de pedidos retrasados por ciudad respecto al total de pedidos de la ciudad.
- `exercise3_metric_3()`: Gráfico de barras con la media de días de retraso por ciudad.
- `self_diagnosis()`: Muestra los totales de pedidos retrasados por franjas y las medias de puntuaciones por franja con `st.metric()` y `st.dataframe()`, además se muestra un diagnóstico final en `st.error()` que indica cuál de los dos tramos de la cadena de entrega tiene la media más alta, indicando la causa más probable de los pedidos retrasados.

---

## Autodiagnóstico

El autodiagnóstico es la sección más importante y que más valor aporta dentro del ejercicio 3 ya que intenta dar una respuesta sobre el origen principal de los retrasos, basándose en los datos que podemos extraer del dataframe de pedidos retrasados.

- **Tramo 1 — Vendedor al transportista**: días que transcurren desde que se realiza el pedido y el vendedor lo envía al transportista.
- **Tramo 2 — Transportista al cliente**: días que transcurren desde que el transportista recoge el pedido hasta que lo entrega al cliente.

Si la media del tramo 1 es mayor que la del tramo 2, el problema principal está en el tiempo que tarda el vendedor en preparar y enviar el pedido al transportista. Si ocurre al revés, el problema está en el reparto del transportista al cliente.

Además, el análisis por franjas de retraso (0-2 días, 2-5 días, 5-10 días, 10-20 días, 20+ días) permite cruzar los retrasos con las puntuaciones de las reviews, mostrando cómo afectan los retrasos directamente en la satisfacción del cliente.

---

## Toma de decisiones en base al gráfico elegido

Para las tres métricas principales se eligió el **gráfico de barras**, ya que es la forma más simple de comparar el valor de cada ciudad y detectar rápidamente cuáles acumulan más retrasos, mayor porcentaje o mayor media de días.

Para el autodiagnóstico se eligieron los **`st.metric()`** y los **`st.dataframe()`** de Streamlit porque cada franja es una categoría con un único valor, y los metrics junto al pequeño dataframe transmiten de forma más visual y compacta esa información. Es una representación orientada a ser leída rápidamente, no a hacer comparaciones en profundidad.

---

## Conclusiones sobre el ejercicio

Este ejercicio nos ha supuesto el ejercicio más complejo y que más orgullosos estamos de haber realizado porque no solo mide cuántos retrasos hay, sino que intenta diagnosticar un por qué de la situación en base a datos. El análisis por franjas permite ver que a medida que aumentan los días de retraso, la puntuación media de las reviews tiende a bajar, lo cual confirma la relación directa entre los retrasos y la insatisfacción del cliente.

El autodiagnóstico identifica en qué parte de la cadena de entrega se concentra el problema. Esto es útil porque las acciones a tomar son distintas según el tramo: si el problema está en el tramo del vendedor, hay que trabajar en la gestión de stock y preparación de pedidos; si está en el tramo del transportista, el foco debería estar en la logística de reparto.

La decisión de filtrar únicamente los retrasos con diferencia de días mayor a 0 es una de las claves para la fiabilidad del análisis, ya que excluye los pedidos que, aunque técnicamente llegaron después de la fecha estimada, lo hicieron el mismo día y no suponen un problema real desde el punto de vista del cliente.
