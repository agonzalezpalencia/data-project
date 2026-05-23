import streamlit as st
import matplotlib.pyplot as plt
import exs.ex3 as ex3

def exercise3_metric_1():

    st.title(f'Análisis de retrasos en pedidos\n' +
                '## Ejercicio 3.1\n - Número de pedidos que llegan tarde por ciudad')
    n_metric1 = st.number_input('Número de Ciudades: ', min_value=1, max_value=100, value=25, key='n_late_orders_city')
    ex3_metric1 = ex3.late_orders_per_city(n_metric1)
    st.bar_chart(ex3_metric1, x='Ciudad (Estado)', y='Cantidad Pedidos')

def exercise3_metric_2():

    st.markdown(f'## Ejercicio 3.2\n - Porcentaje de pedidos retrasados respecto al total de pedidos de la ciudad')
    n_metric2 = st.number_input('Número de Ciudades: ', min_value=1, max_value=100, value=25, key='n_late_orders_percentage')
    ex3_metric2 = ex3.late_orders_percentage(n_metric2)
    st.bar_chart(ex3_metric2, x='Ciudad (Estado)', y='Porcentaje')

def exercise3_metric_3():
    st.markdown(f'## Ejercicio 3.3\n - Tiempo medio de retraso en días')
    n_metric3 = st.number_input('Número de Ciudades: ', min_value=1, max_value=100, value=25, key='n_late_orders_days_mean')
    ex3_metric3 = ex3.late_orders_days_mean(n_metric3)
    st.bar_chart(ex3_metric3, x='Ciudad (Estado)', y='Media Dias de Retraso')
    


def self_diagnosis():
    late_orders_count = ex3.obtain_late_orders_count()
    late_orders_rating = ex3.obtain_late_orders_rating()
    late_orders_deliver_metrics = ex3.obtain_carrier_customer_days()

    def display_orders_count():
        st.info('- Análisis de Cantidad de pedidos retrasados por franjas / rangos')
        columns = st.columns(5)
        for i in range(0, len(late_orders_count)):
            with columns[i]:
                st.metric(label=late_orders_count['Rango'][i], value=late_orders_count['Cantidad Pedidos'][i])
        st.dataframe(late_orders_count, hide_index=True)
        return columns
    
    def display_orders_rating():
        st.info('- Análisis de Puntuaciones de pedidos retrasados por franjas / rangos')
        columns = st.columns(5)
        for i in range(0, len(late_orders_rating)):
            with columns[i]:
                st.metric(label=late_orders_rating['Rango'][i], value=late_orders_rating['Puntuaciones'][i])
        st.dataframe(late_orders_rating, hide_index=True)
        return columns

    def display_final_autodiag():
        purchase_carrier = round(late_orders_deliver_metrics['mean_purchase_carrier'].mean(),2)
        carrier_customer = round(late_orders_deliver_metrics['mean_carrier_customer'].mean(),2)

        st.markdown(f'- La media de dias que han tardado los productos en llegar al transportista ha sido de : {purchase_carrier}')
        st.markdown(f'- La media de dias que ha tardado el transportidta en repartir el paquete al cliente ha sido de: {carrier_customer}')
        
        if (purchase_carrier > carrier_customer):
            st.error('- Podemos decidir gracias a estos datos que la causa del problema viene directamente de la relación existente ' \
            'entre el vendedor del producto y la llegada a la paquetera, al tener una media mas alta que el reparto de los productos ' \
            'al cliente por parte del repartidor, podemos saber a ciencia cierta que es la causa más posible del problema.')
        else:
            st.error('- Podemos decidir gracias a estos datos que la causa del problema viene directamente de la relación existente ' \
            'entre el repartidor y la llegada del producto al cliente por parte del repartidor, al tener una media mas alta que la llegada ' \
            'de los productos desde el vendedor al repartidor, podemos saber a ciencia cierta que es la causa más posible del problema.')

    st.markdown(f'## Autodiágnostico con Análisis exploratorio por Franjas de los Pedidos retrasados')
    display_orders_count()
    display_orders_rating()
    display_final_autodiag()

if __name__ == "__main__":
    exercise3_metric_1()
    exercise3_metric_2()
    exercise3_metric_3()
    self_diagnosis()