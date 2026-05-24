import streamlit as st
import matplotlib.pyplot as plt
import exs.ex1 as ex1

# Método que carga las métricas del Ejercicio 1 directamente en Streamlit
def exercise1_metric_1():

    # Definimos fechas máximas y mínimas
    max_date = ex1.get_max_min_date()[0]
    min_date = ex1.get_max_min_date()[1]

    # Pintamos el título
    st.title(f'Clientes por estado y ciudad\n' +
                '- Representación en Tabla, incluyendo Estado, Ciudad y Número de clientes por ciudad')
    
    # Creamos los inputs de fechas, limitándolo con las fechas máximas y mínimas, creamos un input númerico que marcará la cantidad de ciudades a mostrar
    start_date = st.datetime_input("Selecciona la fecha de inicio:", value= min_date, min_value=min_date, max_value=max_date, key="start_date")
    end_date = st.datetime_input("Selecciona la fecha de fin:", value=max_date, min_value=min_date, max_value=max_date, key="end_date")
    n_metric = st.number_input('Número de Ciudades: ', min_value=1, max_value=100, value=25, key='n_customers_per_city')
    
    # Declaramos el DataFrame y lo mostramos en Streamlit, obviamos el índice
    ex1_metric1 = ex1.obtain_number_customers_per_city(n_metric, start_date, end_date)
    st.dataframe(ex1_metric1, hide_index=True)

    # Pintamos un texto representativo para enseñar al usuario sobre que irá el siguiente gráfico
    st.markdown("- Representación en Gráfico de Barras, incluyendo Ciudad y Clientes por ciudad")

    # Pintamos el gráfico de barras
    st.bar_chart(ex1_metric1, x="Ciudad", y="Nº Clientes por ciudad", )


# Protegemos la ejecución para que se ejecute únicamente cuando llamamos al archivo
if __name__ == "__main__":
    exercise1_metric_1()