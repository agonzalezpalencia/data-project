import numpy as np
import pandas as pd
from seeders import load_data as data

# Método con el que obtenemos un dataset en crudo, es decir, con todos los datos sin agrupar, reflejando todos los datos del cruce entre orders, customers y orders_reviews
def get_raw_reviews_state_customer():

    # Hacemos copias de los dataframes para no cambiar los datos de los originales
    orders = data.orders().copy()
    customers = data.customers().copy()
    orders_reviews = data.order_review().copy()

    # Hacemos merge de orders y orders_reviws por el 'order_id
    raw_df_reviews_state = pd.merge(orders, orders_reviews, on='order_id')

    # Convertimos a datetime de Pandas las columnas que nos interesa usar para el filtrado, así trabajamos más comodamente
    raw_df_reviews_state['order_delivered_customer_date'] = pd.to_datetime(raw_df_reviews_state['order_delivered_customer_date'])
    raw_df_reviews_state['order_estimated_delivery_date'] = pd.to_datetime(raw_df_reviews_state['order_estimated_delivery_date'])

    # Excluimos en este caso los pedidos que se han retrasado
    df_reviews_state = raw_df_reviews_state[(raw_df_reviews_state['order_delivered_customer_date'] 
                                             <= raw_df_reviews_state['order_estimated_delivery_date'])]

    # Cuando el Dataframe se ha filtrado correctamente, hacemos merge con los clientes por el customer_id
    raw_df_reviews_state_customer = pd.merge(df_reviews_state, customers, on='customer_id')

    # Normalizamos la columna de 'state_city' concatenando la ciudad con el estado de esa misma fila
    raw_df_reviews_state_customer['state_city'] = (raw_df_reviews_state_customer['customer_city'].str.capitalize() 
                                                   + ' (' + raw_df_reviews_state_customer['customer_state'] + ')')
    
    # Retornamos el Dataframe con todos los datos
    return raw_df_reviews_state_customer


# Método que obtiene la cantidad de reviews por estado
def get_reviews_count_per_state():

    # Hacemos una copia del Dataframe para no modificar el Dataframe ya existente
    raw_df = get_raw_reviews_state_customer().copy() 

    # Realizamos el agrupamiento por la ciudad con su estado concatenado, y por el estado del pedido, obtenemos el dataframe, reseteamos los índices para 
    # acceder a los datos más comodamente y renombramos / normalizamos las columnas, por último ordenamos descendemente
    df_reviews_state_customer = raw_df.groupby(['state_city', 'order_status']).size().to_frame().reset_index().rename(
        columns={'state_city' : 'Ciudad (Estado)', 
                 'order_status' : 'Estado', 
                 0 : 'Cantidad Reviews'}).sort_values(
                     by='Cantidad Reviews', 
                     ascending=False)
    
    return df_reviews_state_customer


# Método que filtra los pedidos entregados del dataframe retornado del método 'get-reviews_count_per_state'
def delivered_reviews_count_per_state(number : int):

    # Hacemos una copia del Dataframe para no modificar el Dataframe ya existente
    delivered_reviews_count_per_state = get_reviews_count_per_state().copy()
    
    # Filtramos pedidos en estado 'delivered', reseteamos índices y filtramos tantos registros como indique el usuario
    return delivered_reviews_count_per_state[delivered_reviews_count_per_state['Estado'] == 'delivered'].reset_index().head(n=number)


# Método que filtra los pedidos cancelados del dataframe retornado del método 'get-reviews_count_per_state'
def canceled_reviews_count_per_state(number : int):

    # Hacemos una copia del Dataframe para no modificar el Dataframe ya existente
    canceled_reviews_count_per_state = get_reviews_count_per_state().copy()
    
    # Filtramos pedidos en estado 'canceled', reseteamos índices y filtramos tantos registros como indique el usuario
    return canceled_reviews_count_per_state[canceled_reviews_count_per_state['Estado'] == 'canceled'].reset_index().head(n=number)


# Método para obtener la media de reviews por cada uno de los estados, tanto estado de ciudad como estado de pedido
def mean_reviews_score_per_state():

    # Hacemos una copia del Dataframe para no modificar el Dataframe ya existente
    raw_df = get_raw_reviews_state_customer().copy() 

    # De este Dataframe vamos a obtener dos dataframes, en uno agruparemos por la ciudad, el estado y el estado del pedido
    # en el otro ordenaremos por lo mismo que el anterior, pero en este caso sacaremos la media de puntuaciones 
    raw_df_reviews_state_customer_orders = raw_df.groupby(['state_city', 'order_status']).size().to_frame()
    raw_df_reviews_state_customer_ratings_mean = raw_df.groupby(['state_city', 'order_status'])['review_score'].mean().to_frame()

    # Hacemos merge de los dos dataframes
    raw_df_reviews_state_customer_ratings_orders = pd.merge(raw_df_reviews_state_customer_orders, raw_df_reviews_state_customer_ratings_mean, on=['state_city','order_status'] )
    
    # Declaramos el Dataframe que vamos  retornar, resetando los índices, ordenando los valores de manera ascendente y renombrando las columnas que necesitamos mostrar
    df_reviews_state_customer_ratings_orders = raw_df_reviews_state_customer_ratings_orders.reset_index().sort_values(
                    0, ascending=False).rename(
                        columns={'state_city' : 'Ciudad (Estado)', 
                                 'order_status' : 'Estado', 
                                 0 : 'Cantidad Reviews', 
                                 'review_score' : 'Puntuacion'})
    
    # Redondeamos la media de las puntuaciones a dos decimales para tener una visión mas normal del porcentaje
    df_reviews_state_customer_ratings_orders['Puntuacion'] = round(df_reviews_state_customer_ratings_orders['Puntuacion'], 2)

    # Retornamos el Dataframe filtrado
    return df_reviews_state_customer_ratings_orders


# Método que filtra las puntuaciones de los pedidos entregados del dataframe retornado del método 'mean_reviews_score_per_state'
def delivered_mean_reviews_score_per_state(number : int):

    # Hacemos una copia del Dataframe para no modificar el Dataframe ya existente
    delivered_mean_reviews_score_per_state = mean_reviews_score_per_state().copy()

    # Filtramos pedidos en estado 'cancceled', reseteamos índices y filtramos tantos registros como indique el usuario
    return delivered_mean_reviews_score_per_state[delivered_mean_reviews_score_per_state['Estado'] == 'delivered'].reset_index().head(n=number)


# Método que filtra las puntuaciones de los pedidos cancelados del dataframe retornado del método 'mean_reviews_score_per_state'
def canceled_mean_reviews_score_per_state(number : int):

    # Hacemos una copia del Dataframe para no modificar el Dataframe ya existente
    canceled_mean_reviews_score_per_state = mean_reviews_score_per_state().copy()

    # Filtramos pedidos en estado 'canceled', reseteamos índices y filtramos tantos registros como indique el usuario
    return canceled_mean_reviews_score_per_state[canceled_mean_reviews_score_per_state['Estado'] == 'canceled'].reset_index().head(n=number)