# Ejercicio 1 — Clientes por estado y ciudad

## Descripción del ejercicio

El objetivo de este ejercicio es obtener el número de clientes únicos que han realizado algún pedido, agrupados por ciudad y estado. Para hacer el análisis más flexible, además se añade un filtrado de datos por un rango de fechas dinámico que delimitará el usuario desde el dashboard de Streamlit. Existe un input númerico que permite controlar cuántas ciudades se quieren mostrar en los resultados.

Los datasets que se usan en este ejercicio son `orders` y `customers`, ya que necesitamos cruzar los pedidos con los clientes para poder acceder a la ciudad y el estado de cada uno.

---

## Resolución del ejercicio

La resolución se divide en tres capas bien diferenciadas:

### Capa de datos — `seeders/load_data.py`

Los datasets de `orders` y `customers` se cargan desde los archivos CSV mediante funciones decoradas con `@st.cache_data`, lo que evita que se vuelvan a leer del disco cada vez que el usuario interactúa con el dashboard.

### Capa lógica — `exs/ex1.py`

Se definen dos métodos:

- `get_max_min_date()`: Obtiene la fecha mínima y máxima del dataset de pedidos, para delimitar el rango de fechas que se puede seleccionar en el dashboard.
- `obtain_number_customers_per_city(number, start_date, end_date)`: Recibe el número de ciudades a mostrar y el rango de fechas. El proceso que sigue es:
  1. Se hacen copias de los DataFrames originales para no modificar los dataframes en caché.
  2. Se convierte la columna `order_purchase_timestamp` a datetime para poder operar con ella.
  3. Se filtran los pedidos que se encuentran dentro del rango de fechas seleccionado (incluyendo ambos extremos).
  4. Hacemos un merge de los pedidos filtrados con los clientes por `customer_id`, para poder acceder a la ciudad y el estado.
  5. Se normaliza el nombre de la ciudad con `capitalize()`, simplemente por estética.
  6. Se agrupa por estado y ciudad, obteniendo el número de clientes únicos con `nunique()` sobre `customer_unique_id`.
  7. Se ordena de manera descendente, se resetean los índices y se renombran las columnas para que sean más legibles.
  8. Se devuelve el número de filas que haya indicado el usuario en Streamlit.

### Capa gráfica — `streamlit_pages/ex1_executable.py`

Se crea el dashboard con los siguientes componentes:

- Dos inputs de tipo fecha (`st.datetime_input`) para seleccionar el rango, limitados por las fechas mínima y máxima del dataset.
- Un input numérico (`st.number_input`) para definir cuántas ciudades mostrar, con un valor por defecto de 25.
- Una tabla (`st.dataframe`) con los resultados.
- Un gráfico de barras (`st.bar_chart`) con la ciudad en el eje X y el número de clientes en el eje Y.

---

## Toma de decisiones en base al gráfico elegido

Se eligió el **gráfico de barras** para representar los datos dado que es la forma más clara de comparar valores entre categorías. En este caso, cada barra representa una ciudad, y la altura de la barra muestra directamente cuántos clientes únicos hay en esa ciudad.

El gráfico de barras también permite al usuario identificar de un vistazo cuáles son las ciudades con mayor concentración de clientes debido a la altura de cada barra. Se descartaron otras representaciones como el diagrama circular porque con muchas ciudades se vuelve ilegible, y el diagrama de dispersión no tendría sentido al no haber una segunda dimensión númerica que relacionar.

---

## Conclusiones sobre el ejercicio

Con este ejercicio se puede observar de una manera directa cómo se distribuyen los clientes a lo largo del territorio. Las ciudades más grandes concentran la mayor parte de los clientes, lo cual por norma general suele ser lo correcto debido a la gran afluencia que estas contienen.

El filtro por fechas un mayor valor a esta métrica, ya que permite comparar cómo ha evolucionado esa distribución a lo largo del tiempo. Por ejemplo, se puede restringir el análisis a un periodo concreto para ver si en algún momento hubo un crecimiento destacado en una ciudad/es determinada/s.

Usar `nunique()` sobre `customer_unique_id` en lugar de un `count()` sobre `customer_id` permite reflejar claramente los clientes reales, ya que un mismo cliente puede haber realizado varios pedidos en el periodo seleccionado. De esta forma, el resultado refleja clientes reales y no pedidos.
