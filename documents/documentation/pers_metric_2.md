# Métrica Personalizada Nº 2 — Análisis de métodos de pago

## Descripción del ejercicio

El objetivo de esta métrica es analizar qué métodos de pago utilizan los clientes al realizar sus pedidos, mostrando tanto la cantidad total de usos de cada método como el porcentaje que representa sobre el total. excluimos los registros con método de pago `not_defined`, ya que corresponden a pagos de importe 0 que no aportan información válida a nuestra métrica.

El dataset que se usa es `order_payments`, que contiene el detalle de los pagos asociados a cada pedido.

---

## Resolución del ejercicio

### Capa de datos — `seeders/load_data.py`

Se carga en caché el dataset de `order_payments`.

### Capa lógica — `exs/pers_metric_2.py`

Se define un único método:

- `payment_type_global()`: El proceso que sigue es:
  1. Se hace una copia del DataFrame original para no sobreescribir el cargado en caché.
  2. Se agrupa por `payment_type`, se cuenta el número de usos de cada método, se ordena de forma descendente y se resetean los índices.
  3. Se excluyen los registros con método de pago `not_defined`, ya que sus importes son 0 y distorsionarían los resultados.
  4. Se normaliza el nombre del método de pago: se reemplazan los guiones bajos por espacios y se aplica `capitalize()`.
  5. Se calcula el porcentaje de cada método sobre el total de pagos: `(cantidad_metodo / total_pagos) * 100`, redondeado a un decimal.
  6. Se devuelve el DataFrame con las columnas `Método de pago`, `Cantidad` y `Porcentaje (%)`.

### Capa gráfica — `streamlit_pages/pers_metric_2_executable.py`

Se construye el dashboard con dos representaciones del mismo dato, cada una con su propia función:

- `pers_metric_2_1()`: Muestra el título de la página y un **gráfico de barras** nativo de Streamlit (`st.bar_chart`), con el método de pago en el eje X y la cantidad de usos en el eje Y.
- `pers_metric_2_2()`: Muestra un **diagrama circular** construido con `matplotlib`, con las siguientes configuraciones:
  - Fondo oscuro para que encaje con el tema por defecto de Streamlit.
  - Etiquetas de método de pago en color blanco y tamaño de fuente reducido para evitar solapamientos.
  - Porcentajes con un decimal en cada porción del gráfico, con tamaño de fuente reducido.
  - Sombra activada y ángulo de inicio en 90°.
  - Ejes normalizados con `ax.axis('equal')` para que el gráfico sea perfectamente circular.

---

## Toma de decisiones en base al gráfico elegido

Esta métrica se representa con dos gráficos distintos que se complementan entre sí: un **gráfico de barras** y un **diagrama circular**.

El **gráfico de barras** permite comparar de forma directa la cantidad de usos de cada método de pago. Al ser pocos métodos de pago (cuatro excluyendo `not_defined`), el gráfico de barras es muy limpio y claro, y facilita la comparación de volúmenes entre métodos.

El **diagrama circular** complementa al gráfico de barras mostrando la misma información en términos de distribución porcentual. Con tan pocos segmentos, el diagrama circular es el más efectivo: cada porción es grande y legible, y así vemos rápidamente cuál es el método dominante y cuánto espacio ocupa cada uno dentro del total. A diferencia de la métrica personalizada nº 1, donde si se introducían muchas categorías, el diagrama se volvía difícil de leer, aquí el número reducido de métodos de pago hace que ambas representaciones sean igual de válidas.

---

## Conclusiones sobre el ejercicio

Esta métrica revela de forma clara cuál es el método de pago preferido por los clientes. La tarjeta de crédito domina de forma significativa sobre el resto, lo que indica que los clientes prefieren este método frente a otras opciones como boleto o voucher.

La decisión de excluir los pagos `not_defined` es clave para la fiabilidad de los datos: incluirlos inflaría el total de pagos y reduciría los porcentajes del resto de métodos, además de añadir una categoría sin significado real para nuestro negocio.

El hecho de calcular tanto la cantidad absoluta como el porcentaje en la misma función aporta flexibilidad a la capa gráfica, que puede elegir qué dato representar en cada gráfico sin necesidad de hacer cálculos adicionales, accedemos a la columna que necesitamos y la mostramos.
