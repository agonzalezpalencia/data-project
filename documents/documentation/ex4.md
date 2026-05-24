# Ejercicio 4 — Reviews y satisfacción del cliente

## Descripción del ejercicio

El objetivo de este ejercicio es analizar las reviews que dejan los clientes, separando los pedidos entregados a tiempo de los cancelados. A diferencia del anterior ejercicio, aquí nos centramos en los pedidos que **no** llegaron tarde, para medir la satisfacción de los clientes en condiciones normales de entrega. Los pedidos cancelados se tratan como un grupo aparte, ya que tienen un comportamiento y unas puntuaciones específicas que no deben mezclarse con los entregados.

El ejercicio se divide en dos métricas:

1. Número de reviews por ciudad, separado entre pedidos entregados y cancelados.
2. Puntuación media de las reviews por ciudad, separado entre pedidos entregados y cancelados.

Los datasets que se usan son `orders`, `customers` y `order_reviews`.

---

## Resolución del ejercicio

### Capa de datos — `seeders/load_data.py`

Se cargan en cachélos datasets de `orders`, `customers` y `order_reviews`.

### Capa lógica — `exs/ex4.py`

El método base del que parten el resto es `get_raw_reviews_state_customer()`:

- `get_raw_reviews_state_customer()`: Hace un merge de `orders` con `order_reviews` por `order_id`, convierte las fechas de entrega a datetime, y filtra los pedidos que **no** se han retrasado (fecha de entrega real menor o igual a la fecha estimada de entrega). Después hace un merge con los clientes por `customer_id` y crea la columna normalizada `state_city`.

A partir de este método base se construyen el resto:

- `get_reviews_count_per_state()`: Agrupa por `state_city` y `order_status`, cuenta el número de reviews por cada combinación y ordena de forma descendente.
- `delivered_reviews_count_per_state(number)`: Filtra del DataFrame anterior solo los pedidos con estado `delivered` y devuelve los N primeros.
- `canceled_reviews_count_per_state(number)`: Filtra solo los pedidos con estado `canceled` y devuelve los N primeros.
- `mean_reviews_score_per_state()`: Agrupa por `state_city` y `order_status`, calcula el conteo de reviews y la media de puntuaciones por grupo. Hace un merge de los dos resultados, renombra las columnas y redondea la puntuación a 2 decimales, ordenamos por la cantidad de reviews para tener un gráfico basado en las medias de las ciudades que más reviews han hecho
- `delivered_mean_reviews_score_per_state(number)`: Filtra del DataFrame anterior los pedidos con estado `delivered` y devuelve los N primeros.
- `canceled_mean_reviews_score_per_state(number)`: Filtra los pedidos con estado `canceled` y devuelve los N primeros.

### Capa gráfica — `streamlit_pages/ex4_executable.py`

Se definen dos funciones principales:

- `exercise4_metric_1()`: Muestra un gráfico de barras con el número de reviews de pedidos entregados, y un conjunto de `st.metric()` para los cancelados, se usa `st.metric()` ya que la cantidad de reviews de los pedidos cancelados es mucho más pequeña que los entregados.
- `exercise4_metric_2()`: Muestra un gráfico de barras con la puntuación media de los pedidos entregados, y `st.metric()` para los cancelados, por el mismo motivo que se comento anteriormente, la cantidad de reciews de los pedidos cancelados es demasiado baja como para representarlo gráficamente

---

## Toma de decisiones en base al gráfico elegido

Se han usado dos representaciones distintas según el volumen de datos:

- El **gráfico de barras** se usa para los pedidos entregados porque hay muchas ciudades y la comparación entre ellas es el dato principal que se quiere transmitir. La altura de cada barra indica de forma rápida cuál es la ciudad con más reviews o mejor puntuación.
- Los **`st.metric()`** se usan para los pedidos cancelados porque el número de registros es mucho menor. En este caso, mostrar una barra por ciudad con pocos datos no aportaría mucho visualmente, y el formato de metric permite ver cada ciudad con su valor de forma compacta y clara.

Esta combinación de dos formatos en la misma página es una decisión deliberada para adaptarse al volumen real de datos de cada grupo, previo a esto se analizaron las franjas de estados de los pedidos para poder tomar una decisión sólida.

---

## Conclusiones sobre el ejercicio

Este ejercicio complementa al ejercicio 3, ya que este se centra en los retrasos y su impacto en la satisfacción, mientras que el ejercicio 4 analiza la satisfacción en condiciones normales de entrega. Comparar ambos resultados permite entender mejor cómo de diferente es la experiencia del cliente cuando el pedido llega a tiempo frente a cuando se retrasa.

Separar los pedidos cancelados como un grupo propio, desde nuestro punto de vista es una decisión muy acertada, ya que sus reviews reflejan una experiencia completamente distinta: el cliente no ha recibido el producto, por lo que sus puntuaciones tienen un significado diferente al de un pedido entregado, de esta manera excluimos datos que no nos benefician en los registros de reviews de pedidos entregados.
