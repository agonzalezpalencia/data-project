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


# Protegemos la ejecución para que se ejecute únicamente cuando llamamos al archivo
if __name__ == "__main__":
    exercise2_metric_1()