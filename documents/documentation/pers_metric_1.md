# Métrica Personalizada Nº 1 — Distribución de ventas por categoría de producto

## Descripción del ejercicio

El objetivo de esta métrica es visualizar cómo se distribuye el volumen de ventas entre las distintas categorías de productos, expresado como porcentaje sobre el total de productos vendidos. El usuario puede controlar cuántas categorías quiere ver en el gráfico, lo que permite tanto una visión global como un análisis más enfocado en las categorías más relevantes.

Los datasets que se usan son `order_items` y `products`, cruzándolos por `product_id` para poder acceder a la categoría de cada producto vendido.

---

## Resolución del ejercicio

### Capa de datos — `seeders/load_data.py`

Se cargan en caché los datasets de `order_items` y `products`.

### Capa lógica — `exs/pers_metric_1.py`

Se define un único método:

- `order_percentage_per_category(number)`: El proceso que sigue es:
  1. Se hacen copias de los DataFrames originales para no modificar los cargados en caché.
  2. Se hace un merge de `order_items` con `products` por `product_id`, para cruzar cada producto vendido con su categoría.
  3. Se filtran las filas con categoría nula para evitar datos no contemplados en el cálculo del porcentaje.
  4. Se agrupa por `product_category_name` y se cuenta el número de productos por categoría, ordenando de forma descendente.
  5. Se normaliza el nombre de la categoría: se reemplazan los guiones bajos por espacios y se aplica `capitalize()`.
  6. Se calcula el porcentaje de cada categoría sobre el total: `(count_categoria / sum_total) * 100`.
  7. Se devuelven las N primeras categorías según lo que indique el usuario.

### Capa gráfica — `streamlit_pages/pers_metric_1_executable.py`

Se construye el dashboard con dos representaciones del mismo dato, cada una con su propio input numérico y su propia función:

- `pers_metric_1_1()`: Un input numérico para controlar cuántas categorías mostrar, con valor por defecto de 15. Se representa con un **gráfico de barras** nativo de Streamlit (`st.bar_chart`), con la categoría en el eje X y el porcentaje en el eje Y.
- `pers_metric_1_2()`: Un input numérico independiente para controlar cuántas categorías mostrar, con valor por defecto de 15 y un diagrama circular construido con `matplotlib`, con las siguientes configuraciones:
  - Fondo oscuro para que encaje con el tema por defecto de Streamlit.
  - Etiquetas de categoría en color blanco y tamaño de fuente reducido para evitar solapamientos.
  - Porcentajes con un decimal en cada porción del gráfico, con tamaño de fuente reducido
  - Sombra activada y ángulo de inicio en 90°.
  - Ejes normalizados con `ax.axis('equal')` para que el gráfico sea perfectamente circular.

---

## Toma de decisiones en base al gráfico elegido

Esta métrica se representa con dos gráficos distintos que se complementan entre sí: un **gráfico de barras** y un **diagrama circular**.

El **diagrama circular** (también llamado diagrama de tarta o pie chart) que creemos que es el más adecuado para representar esta métrica, porque el dato que se quiere mostrar es una distribución porcentual de partes sobre el total. Este tipo de gráfico es especialmente adecuado cuando el objetivo es visualizar qué proporción ocupa cada categoría dentro del conjunto total.

El **gráfico de barras**, que permite comparar de forma directa el porcentaje de cada categoría de manera ordenada, facilitando la lectura cuando hay muchas categorías. Esta opción se ha contemplado debido a que el diagrama circular, solapa las categorías cuando existen muchas en el mismo diagrama, en el gráfico de barras podemos introducir más categorías que en el diagrama circular, mejorando así la visualización de muchas categorías

La reducción del tamaño de fuente de las etiquetas fue necesaria para que los nombres de las categorías no se solapasen entre sí. El fondo oscuro se configuró para que el gráfico encaje visualmente con la interfaz de Streamlit y parezca un gráfico que realmente ha generado Streamlit y no Matplotlib

---

## Conclusiones sobre el ejercicio

Esta métrica permite identificar cuáles son las categorías de productos más vendidas y cuánto peso tienen sobre el total del catálogo. Es especialmente útil para detectar si hay categorías muy dominantes o si el volumen está distribuido de forma más equilibrada entre varias.

La decisión de filtrar las categorías nulas antes de calcular el porcentaje es importante para que los resultados sean correctos: si no los filtrasemos, el porcentaje total no sumaría 100%, haciendo un diagrama incompleto e inválido.
