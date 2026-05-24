# Ejercicio 2 — Pedidos por ciudad

## Descripción del ejercicio

El objetivo de este ejercicio es obtener el número de pedidos agrupados por ciudad y estado, calculando también el porcentaje que representa cada ciudad sobre el total de pedidos del periodo seleccionado y el ratio de pedidos por cliente. Al igual que en el ejercicio 1, filtramos por un rango de fechas definido por el usuario desde el dashboard para controlar cuántas ciudades se quieren ver en los resultados.

Los datasets que se usan son `orders` y `customers`, cruzándolos para poder acceder a la ubicación de cada cliente.

---

## Resolución del ejercicio

### Capa de datos — `seeders/load_data.py`

Los datasets de `orders` y `customers` se cargan en caché una sola vez.

### Capa lógica — `exs/ex2.py`

Se definen dos métodos:

- `get_max_min_date()`: Igual que en el ejercicio 1, devuelve las fechas límite del dataset para delimitar el selector de fechas del dashboard.
- `obtain_number_orders(number, start_date, end_date)`: Recibe el número de ciudades y el rango de fechas. El proceso que sigue es:
  1. Se hacen copias de los DataFrames originales para no sobreescribir los que están en caché.
  2. Se convierte `order_purchase_timestamp` a datetime.
  3. Se filtran los pedidos por el rango de fechas seleccionado.
  4. Se guarda el total de pedidos del periodo en `total_pedidos`, para usarlo mas adelante en cálculo de % de pedidos respecto al total.
  5. Se hace un merge de los pedidos filtrados con los clientes por `customer_id`.
  6. Se normaliza el nombre de la ciudad.
  7. Se agrupa por estado y ciudad con una función de agregación doble: `nunique()` para obtener los clientes únicos y `count()` para obtener el total de pedidos de cada ciudad.
  8. Se calcula el porcentaje de pedidos de cada ciudad respecto al total del periodo: `(pedidos_ciudad / total_pedidos) * 100`.
  9. Se crea una copia del DataFrame para calcular el ratio de pedidos por cliente: `pedidos_ciudad / clientes_ciudad`.
  10. Se devuelven dos DataFrames: uno ordenado por el porcentaje de pedidos y otro por el ratio de pedidos por cliente, a partir de esos dos, repsentaremos dos métricas (Dataframe y Scatter Chart)

### Capa gráfica — `streamlit_pages/ex2_executable.py`

Se crea el dashboard con los siguientes componentes:

- Dos inputs de tipo fecha para el rango temporal.
- Un input numérico para definir cuántas ciudades mostrar, con valor por defecto de 25.
- Una tabla con los resultados del primer DataFrame (porcentaje de pedidos).
- Un diagrama de dispersión (`st.scatter_chart`) con las ciudades en el eje X y el ratio de pedidos por cliente en el eje Y.

---

## Toma de decisiones en base al gráfico elegido

Se usaron dos representaciones distintas en este ejercicio, porque cada métrica tiene una forma muy distinta de poder reporesentarse en Streamlit:

- La **tabla** se usa para mostrar el porcentaje de pedidos por ciudad respecto al total de pedidos, ya que este dato es más fácil de consumir en formato tabular cuando hay muchas ciudades.
- El **diagrama de dispersión** se eligió para representar el ratio de pedidos por cliente. A diferencia del gráfico de barras, el diagrama de dispersión permite ver de forma más clara si hay ciudades con distitno compartamiento, es decir, ciudades donde los clientes hacen muchos más pedidos de lo habitual. En un gráfico de barras esto también sería visible, pero el diagrama de dispersión transmite mejor nuestra idea de mostrar los puntos de intéres donde los clientes concentran sus pedidos.

---

## Conclusiones sobre el ejercicio

Este ejercicio aporta una visión más completa que el ejercicio 1, ya que no solo cuenta clientes sino que mide el comportamiento de los pedidos por ciudad. El porcentaje de pedidos respecto al total permite analizar de una manera mád clara los datos y no dejarse llevar únicamente por el volumen: una ciudad pequeña puede tener un porcentaje relevante si sus clientes compran con mucha frecuencia.

El ratio de pedidos por cliente es especialmente útil para identificar ciudades con alta recurrencia de compra. Si una ciudad tiene pocos clientes pero un ratio alto, puede indicar un perfil de usuario muy activo o fidelizado, lo que puede sernos de gran ayuda a la hora de lógica de negocio o una estrategia comercial en esa ciudad

Devolver dos DataFrames desde la misma función es una decisión que evita repetir peraciones que necesitan de cómputo, reutilizando el trabajo que ya hemos realizado para obtener dos perspectivas distintas del mismo dato.
