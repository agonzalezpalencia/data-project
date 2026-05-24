import streamlit as st
import matplotlib.pyplot as plt
import exs.ex2 as ex2

# Método que carga las métricas del Ejercicio 2 directamente en Streamlit
def exercise2_metric_1():

    # Declaramos fecha máxima y mínima
    max_date = ex2.get_max_min_date()[0]
    min_date = ex2.get_max_min_date()[1]

    # Pintamos el título
    st.title(f'Pedidos por ciudad\n' +
                '- Representación en Tabla, incluyendo Estado, Ciudad y Número de clientes por ciudad')

    # Creamos los inputs de fechas, limitándolo con las fechas máximas y mínimas, creamos un input númerico que marcará la cantidad de ciudades a mostrar
    start_date = st.datetime_input("Selecciona la fecha de inicio:", value= min_date, min_value=min_date, max_value=max_date, key="start_date")
    end_date = st.datetime_input("Selecciona la fecha de fin:", value=max_date, min_value=min_date, max_value=max_date, key="end_date")
    n_metric = st.number_input('Número de Ciudades: ', min_value=1, max_value=100, value=25, key='n_cutomers_per_city')

    # Declaramos los DataFrames
    ex2_df_orders, ex2_df_customers_orders = ex2.obtain_number_orders(n_metric, start_date, end_date)
    
    # Mostramos el DataFrame que contiene los pedidos agrupados por las ciudades y estado
    st.dataframe(ex2_df_orders, hide_index=True)

    # Enseñamos al usuario sobre que vea nuestra siguiente gráfica
    st.markdown("- Ratio de Pedidos por cliente, representado con un Diagrama de Dispersión ")

    # Pintamos el siguiente DataFrame utilizando un Diagrama de dispersión
    st.scatter_chart(ex2_df_customers_orders, x="Ciudad", x_label="Ciudades", y="Ratio de pedidos por cliente")


def questions_answer():

    # Pregunta Nº 1 -  ¿Qué información o patrones se pueden identificar a partir de estos datos?
    st.title('Respuesta a las preguntas formuladas\n'
    '- ¿Qué información o patrones se pueden identificar a partir de estos datos?')

    # Respuesta a Pregunta Nº 1
    st.markdown('> Podemos ver como Sao Paulo es el líder indiscutible del total de pedidos, ya que concentra un 15,63%, seguido de Rio de Janeiro con un 6,92%.' \
    'En los países del sureste de Brasil, podemos ver como hay una concentración geográfica a tener en cuenta, debido a que la gran mayoría de los pedidos se agrupan sobre esa aparte, ' \
    'concretamente en los estados de SP,RJ,MG y DF, Los datos también nos dicen como el ratio de pedidos por cliente se situa entre 2 y 3 en las ciudades que menor población tienen' \
    ', mientras que en las grandes ciudades este ratio se mantiene entre 1 y 1.5, indicando que los clientes en las grandes ciudades solo suelen hacer 1 pedido y en pocas ocasiones 2.')

     # Pregunta Nº 2 -  ¿Qué acciones, como analista de datos, crees que debería tomar la empresa para mejorar sus ventas?
    st.markdown('- ¿Qué acciones, como analista de datos, crees que debería tomar la empresa para mejorar sus ventas?')

    # Respuesta a Pregunta Nº 2
    st.markdown('> Para mejorar sus ventas la empresa puede tomar varias acciones, las más importantes y que más impacto pueden llegar a tener son: Reforzar la logística y '
    'el marketing en las ciudades del sureste puesto a que tienen un volumen de clientela fija y consolidado, manteniendo esos mercados a flote y poder crecer en consecuencia, otra'
    'de las cosas que podría mejorar las ventas es, aumentar el ratio de los pedidos de los clientes utilizando programas de fidelización de estos mismos en base a puntos '
    'que puedan usar en los pedidos, o descuentos en los mismos, por último, las ciudades que tienen un ratio alto de pedidos pero población baja podrían ser'
    'candidatos a programas de captación de clientes, sumando a los clientes recurrentes que ya tienen los captados con estas campañas')

# Protegemos la ejecución para que se ejecute únicamente cuando llamamos al archivo
if __name__ == "__main__":
    exercise2_metric_1()
    questions_answer()