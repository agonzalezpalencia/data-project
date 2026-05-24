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

Se construye el dashboard con los siguientes componentes:

- Un input numérico para controlar cuántas categorías mostrar, con valor por defecto de 15.
- Un diagrama circular construido con `matplotlib`, con las siguientes configuraciones:
  - Fondo oscuro para que encaje con el tema por defecto de Streamlit.
  - Etiquetas de categoría en color blanco y tamaño de fuente reducido para evitar solapamientos.
  - Porcentajes con un decimal en cada porción del gráfico, con tamaño de fuente reducido
  - Sombra activada y ángulo de inicio en 90°.
  - Ejes normalizados con `ax.axis('equal')` para que el gráfico sea perfectamente circular.

---

## Toma de decisiones en base al gráfico elegido

Se eligió el **diagrama circular** (también llamado diagrama de tarta o pie chart) porque el dato que se quiere mostrar es una distribución porcentual de partes sobre un todo. Este tipo de gráfico es especialmente adecuado cuando el objetivo es visualizar qué proporción ocupa cada categoría dentro del conjunto total.

El gráfico de barras habría sido una alternativa válida y posiblemente más fácil de leer cuando hay muchas categorías, pero el diagrama circular aporta una idea más intuitiva y amigable sobre la distribución relativa: de un vistazo se puede ver si hay una categoría que domina claramente el mercado o si la distribución está más repartida, gracias a sus colores facilita mucho el análisis de estos datos.

La reducción del tamaño de fuente de las etiquetas fue necesaria para que los nombres de las categorías no se solapasen entre sí. El fondo oscuro se configuró para que el gráfico encaje visualmente con la interfaz de Streamlit y parezca un gráfico que realmente ha generado Streamlit y no Matplotlib

---

## Conclusiones sobre el ejercicio

Esta métrica permite identificar cuáles son las categorías de productos más vendidas y cuánto peso tienen sobre el total del catálogo. Es especialmente útil para detectar si hay categorías muy dominantes o si el volumen está distribuido de forma más equilibrada entre varias.

La decisión de filtrar las categorías nulas antes de calcular el porcentaje es importante para que los resultados sean correctos: si no los filtrasemos, el porcentaje total no sumaría 100%, haciendo un diagrama incompleto e inválido.
