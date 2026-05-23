import streamlit as st
import exs.ex4 as ex4

def exercise4_metric_1():
    st.title(f'Reviews y satisfacción del cliente\n' +
                '## Ejercicio 1\n - Número de reviews por estado (Estado de Ciudad y Estado de Pedido "delivered")')
    
    n_metric1 = st.number_input('Número de Ciudades: ', min_value=1, max_value=100, value=25, key='n_delivered')
    ex4_1_metric_1 = ex4.delivered_reviews_count_per_state(n_metric1)
    st.bar_chart(ex4_1_metric_1, x='Ciudad (Estado)', y='Cantidad Reviews')
    
    n_metric2 = st.number_input('Número de Ciudades: ', min_value=1, max_value=100, value=25, key='n_canceled')
    ex4_1_metric_2 = ex4.canceled_reviews_count_per_state(n_metric2)
    
    st.markdown('- Número de reviews por estado (Estado de Ciudad y Estado de Pedido "canceled")')
    columns = st.columns(len(ex4_1_metric_2))
    for i in range(0, len(ex4_1_metric_2)):
        with columns[i]:
            st.metric(label=ex4_1_metric_2['Ciudad (Estado)'][i], value=ex4_1_metric_2['Cantidad Reviews'][i])
    return columns

def exercise4_metric_2():
    st.markdown(f'## Ejercicio 2\n - Score medio de las reviews en cada estado (Estado de Ciudad y Estado de Pedido "delivered")')

    n_metric1 = st.number_input('Número de Ciudades: ', min_value=1, max_value=100, value=25, key='n_delivered_2')
    ex4_2_metric_1 = ex4.delivered_mean_reviews_score_per_state(n_metric1)
    st.bar_chart(ex4_2_metric_1, x='Ciudad (Estado)', y='Puntuacion')
    
    n_metric2 = st.number_input('Número de Ciudades: ', min_value=1, max_value=100, value=25, key='n_canceled_2')
    ex4_2_metric_2 = ex4.canceled_mean_reviews_score_per_state(n_metric2)

    st.markdown(f'- Score medio de las reviews en cada estado (Estado de Ciudad y Estado de Pedido "canceled")')
    columns = st.columns(len(ex4_2_metric_2))
    for i in range(0, len(ex4_2_metric_2)):
        with columns[i]:
            st.metric(label=ex4_2_metric_2['Ciudad (Estado)'][i], value=ex4_2_metric_2['Puntuacion'][i])
    return columns

if __name__ == "__main__":
    exercise4_metric_1()
    exercise4_metric_2()