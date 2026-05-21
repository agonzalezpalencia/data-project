import streamlit as st
import exs.ex3 as ex3

def exercise3_metrics():
    ex3_metric1 = ex3.late_orders_per_city()
    ex3_metric2 = ex3.late_orders_percentage()

    st.title(f'Análisis de retrasos en pedidos\n' +
                '## Ejercicio 1\n - Número de pedidos que llegan tarde por ciudad')
    st.bar_chart(ex3_metric1, x='Ciudad', y='Cantidad Pedidos')
    st.markdown(f'## Ejercicio 2\n - Número de pedidos que llegan tarde por ciudad')
    st.bar_chart(ex3_metric2, x='Ciudad', y='Porcentaje')
    st.markdown(f'## Ejercicio 3\n - Tiempo medio de retraso en días')

if __name__ == "__main__":
    exercise3_metrics()