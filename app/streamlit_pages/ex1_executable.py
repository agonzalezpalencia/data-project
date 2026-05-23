import streamlit as st
import matplotlib.pyplot as plt
import exs.ex1 as ex1


def exercise1_metric_1():

    max_date = ex1.get_max_min_date()[0]
    min_date = ex1.get_max_min_date()[1]

    st.title(f'Clientes por estado y ciudad\n' +
                '- Representación en Tabla, incluyendo Estado, Ciudad y Número de clientes por ciudad')
    
    start_date = st.datetime_input("Selecciona la fecha de inicio:", value= min_date, min_value=min_date, max_value=max_date, key="start_date")
    end_date = st.datetime_input("Selecciona la fecha de fin:", value=max_date, min_value=min_date, max_value=max_date, key="end_date")
    n_metric = st.number_input('Número de Ciudades: ', min_value=1, max_value=100, value=25, key='n_customers_per_city')
    
    ex1_metric1 = ex1.obtain_number_customers_per_city(n_metric, start_date, end_date)
    st.dataframe(ex1_metric1, hide_index=True)

    st.markdown("- Representación en Gráfico de Barras, incluyendo Ciudad y Clientes por ciudad")

    st.bar_chart(ex1_metric1, x="Ciudad", y="Nº Clientes por ciudad", )


if __name__ == "__main__":
    exercise1_metric_1()