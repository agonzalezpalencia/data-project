import streamlit as st
import matplotlib.pyplot as plt
import exs.ex3 as ex3

# Método que carga la primera métrica del Ejercicio 3 en Streamlit
def exercise3_metric_1():

    # Definimos el título de la página y de la métrica
    st.title(f'Análisis de retrasos en pedidos\n' +
                '## Ejercicio 3.1\n - Número de pedidos que llegan tarde por ciudad')
    
    # Declaramos input númerico que ayudará a mostrar la cantidad de ciudades en la métrica
    n_metric1 = st.number_input('Número de Ciudades: ', min_value=1, max_value=100, value=25, key='n_late_orders_city')

    # Declaramos la métrica en base al número que nos pase el usuario, y mostramos el gráfico de barras
    ex3_metric1 = ex3.late_orders_per_city(n_metric1)
    st.bar_chart(ex3_metric1, x='Ciudad (Estado)', y='Cantidad Pedidos')


# Método que carga la segunda métrica del Ejercicio 3 en Streamlit
def exercise3_metric_2():

    # Definimos el título de la métrica
    st.markdown(f'## Ejercicio 3.2\n - Porcentaje de pedidos retrasados respecto al total de pedidos de la ciudad')

    # Declaramos input númerico que ayudará a mostrar la cantidad de ciudades en la métrica
    n_metric2 = st.number_input('Número de Ciudades: ', min_value=1, max_value=100, value=25, key='n_late_orders_percentage')

    # Declaramos la métrica en base al número que nos pase el usuario, y mostramos el gráfico de barras
    ex3_metric2 = ex3.late_orders_percentage(n_metric2)
    st.bar_chart(ex3_metric2, x='Ciudad (Estado)', y='Porcentaje')


# Método que carga la tercera métrica del Ejercicio 3 en Streamlit
def exercise3_metric_3():

    # Definimos el título de la métrica
    st.markdown(f'## Ejercicio 3.3\n - Tiempo medio de retraso en días')

    # Declaramos input númerico que ayudará a mostrar la cantidad de ciudades en la métrica
    n_metric3 = st.number_input('Número de Ciudades: ', min_value=1, max_value=100, value=25, key='n_late_orders_days_mean')

     # Declaramos la métrica en base al número que nos pase el usuario, y mostramos el gráfico de barras
    ex3_metric3 = ex3.late_orders_days_mean(n_metric3)
    st.bar_chart(ex3_metric3, x='Ciudad (Estado)', y='Media Dias de Retraso')
    

# Método que carga el apartado del autodiagnóstico al final la muestra de las gráficas de los ejercicios
def self_diagnosis():

    # Cargamos las métricas que mostraremos en el autodiagnóstico, estas son el conteo de total de pedidos retrasados por franjas / intervalos, 
    # la media de puntuaciones de los pedidos retrasados por franjas / intervalos,
    # las medias en dias que nos indican cuanto tarda el vendedor en enviar el pedido al repartidor, y el repartidor en enviar el pedido al cliente
    late_orders_count = ex3.obtain_late_orders_count()
    late_orders_rating = ex3.obtain_late_orders_rating()
    late_orders_deliver_metrics = ex3.obtain_carrier_customer_days()

    # Método para mostrar los totales de pedidos por las franjas / intervalos que hemos definido
    def display_orders_count():

        # Mostramos un pequeño mensaje informativo al usuario
        st.info('- Análisis de Cantidad de pedidos retrasados por franjas / rangos')

        # Declaramos las cantidades de columnas que usaremos para mostrar los 'st.metric()', según la cantidad de franjas / intervalos
        columns = st.columns(len(late_orders_count))

        # Recorremos las columnas
        for i in range(0, len(late_orders_count)):
            
            # Definimos un metric de streamlit para cada columna, mostrando el rango y la cantidad de pedidos atrasados en ese rango
            with columns[i]:
                st.metric(label=late_orders_count['Rango'][i], value=late_orders_count['Cantidad Pedidos'][i])

        # Mostramos la métrica tanto en columnas (haciendo el return) como con st.dataframe, renderizando el dataframe completo
        st.dataframe(late_orders_count, hide_index=True)
        return columns
    
    def display_orders_rating():

        # Mostramos un pequeño mensaje informativo al usuario
        st.info('- Análisis de Puntuaciones de pedidos retrasados por franjas / rangos')

        # Declaramos las cantidades de columnas que usaremos para mostrar los 'st.metric()', según la cantidad de franjas / intervalos
        columns = st.columns(len(late_orders_rating))

        # Recorremos las columnas
        for i in range(0, len(late_orders_rating)):

            # Definimos un metric de streamlit para cada columna, mostrando el rango y la cantidad de pedidos atrasados en ese rango
            with columns[i]:
                st.metric(label=late_orders_rating['Rango'][i], value=late_orders_rating['Puntuaciones'][i])
        
        # Mostramos la métrica tanto en columnas (haciendo el return) como con st.dataframe, renderizando el dataframe completo
        st.dataframe(late_orders_rating, hide_index=True)
        return columns

    # Método con el que mostramos el diagnóstico final, o autodiagnóstico, para dar un veredicto, nos basamos en las medias:
    # Tiempo en días que tarda el vendedor en enviar el paquete al repartidor, Tiempo en días que tarda el repartidor en entrgar el paquete al cliente
    def display_final_autodiag():

        # Declaramos las medias, accediendo a la columna en concreto que nos interesa y haciendo la media, redondeamos para hacer el resultado más legible
        purchase_carrier = round(late_orders_deliver_metrics['mean_purchase_carrier'].mean(),2)
        carrier_customer = round(late_orders_deliver_metrics['mean_carrier_customer'].mean(),2) 

        # Mostramos ambas medias para validar el autodiagnóstico
        st.markdown(f'- La media de dias que han tardado los productos en llegar al transportista ha sido de : {purchase_carrier}')
        st.markdown(f'- La media de dias que ha tardado el transportista en repartir el paquete al cliente ha sido de: {carrier_customer}')
        
        # Según el valor que predomine, mostramos un mensaje u otro, en este caso predomina 'carrier_customer', por lo que el motivo principal de los retrasos en los pedidos
        # es el tiempo que tarda el repartidor en enviar el paquete al cliente
        if (purchase_carrier > carrier_customer):
            st.error('- Podemos decidir gracias a estos datos que la causa del problema viene directamente de **la relación existente ' \
            'entre el vendedor del producto y la llegada a la paquetera**.')
        else:
            st.error('- Podemos decidir gracias a estos datos que la causa del problema viene directamente de **la relación existente ' \
            'entre el repartidor y la llegada del producto al cliente por parte del repartidor**.')

    # Construimos el título del autodiagnóstico y mostramos nuestras métricas
    st.markdown(f'## Autodiágnostico con Análisis exploratorio por Franjas de los Pedidos retrasados')
    display_orders_count()
    display_orders_rating()
    display_final_autodiag()

# Protegemos la ejecución para que se ejecute únicamente cuando llamamos al archivo
if __name__ == "__main__":
    exercise3_metric_1()
    exercise3_metric_2()
    exercise3_metric_3()
    self_diagnosis()