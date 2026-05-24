import numpy as np
import pandas as pd
from seeders import load_data as data

# Método con el que obtenemos los dias que se tarda en enviar el producto tanto desde el vendedor al repartidor, como del repartidor al cliente
def obtain_carrier_customer_days():

    # Guardamos una referencia al DataFrame con los pedidos retrasdados, hacemos una copia para no modificar el original
    time_days = obtain_late_orders_days().copy()

    # Convertimos las fechas necesarias para el cálculo a datetime, para poder tratar mejor las fechas
    time_days['order_delivered_carrier_date'] = pd.to_datetime(time_days['order_delivered_carrier_date'])
    time_days['order_purchase_timestamp'] = pd.to_datetime(time_days['order_purchase_timestamp'])

    # Calculamos los días que se tarda tanto en enviar el producto desde el vendedor hacia el repartidor, como del repartidor al cliente, 
    # de estos valores nos quedamos con los días
    time_days['mean_purchase_carrier'] = (time_days['order_delivered_carrier_date'] - time_days['order_purchase_timestamp']).dt.days
    time_days['mean_carrier_customer'] = (time_days['order_delivered_customer_date'] - time_days['order_delivered_carrier_date']).dt.days

    return time_days # Retornamos el DataFrame

# Método para devolver en franjas o intervalos los pedidos retrasados
def obtain_late_orders_count():

    # Creamos copias de los DataFramos originales para no modificarlos directamente
    time_days = obtain_late_orders_days().copy()

    # Declaramos los intervalos sobre los que vamos a operar los totales de pedidos
    bins = [0,2,5,10,20, int(time_days['late_days'].max())]

    # Declaramos las etiquetas de los intervalos
    labels = ['0 a 2 dias', '2 a 5 dias', '5 a 10 dias', '10 a 20 dias', '20+ dias']

    # Hacemos un cut, que nos ayudará a dividir el dataframe en los intervalos con sus correspondientes etiquetas y así 
    # visualizar mejor en que franjas se mueven los pedidos atrasados
    time_days['range'] = pd.cut(time_days['late_days'], bins=bins, labels=labels)

    # Agrupamos por cada uno de los rangos obtenidos, Pandas nos obliga a poner el parámetro observed=True cuando hacemos cut, así que lo ponemos
    # por último obtenemos el dataframe, reseteamos el índice y renombramos la columna de 0
    df_late_orders_count_ranges = time_days.groupby('range', observed=True).size().reset_index().rename(columns={ 0 : 'count'})

    return df_late_orders_count_ranges.rename(columns={'range' : 'Rango', 'count' : 'Cantidad Pedidos'}) # Renombramos columnas y retornamos el DataFrame


# Método para devolver en franjas o intervalos la media de puntuaciones de los pedidos retrasados
def obtain_late_orders_rating():

    # Obtenemos copias de los Dataframes originales oara o modificar los ya creados
    time_days = obtain_late_orders_days().copy()
    orders_reviews = data.order_review().copy()

    # Hacemos merge con el Dataframe de reviews para poder tener las reviews de todos los pedidos y poder obtener una media consistente
    df_late_orders_reviews = pd.merge(time_days, orders_reviews, on='order_id')

    # Declaramos los intervalos sobre los que vamos a operar las medias de los pedidos retrasados
    bins = [0,2,5,10,20, int(df_late_orders_reviews['late_days'].max())]

    # Declaramos las etiquetas de los intervalos
    labels = ['0 a 2 dias', '2 a 5 dias', '5 a 10 dias', '10 a 20 dias', '20+ dias']

    # Hacemos un cut, que nos ayudará a dividir el dataframe en los intervalos con sus correspondientes etiquetas y así 
    # visualizar mejor en que franjas se mueven las medias de las puntuaciones de los pedidos atrasados
    df_late_orders_reviews['range'] = pd.cut(df_late_orders_reviews['late_days'], bins=bins, labels=labels)

    # Agrupamos el dataframe por el rango que hemos obtenido, y obtenemos la media de las puntuaciones, redondeando a 2 decimales y reseteando los índices para
    # mayor comodidad al acceder al dato
    df_late_orders_rating_ranges = round(df_late_orders_reviews.groupby('range', observed=True)['review_score'].mean(), 2).reset_index()

    return df_late_orders_rating_ranges.rename(columns={'range' : 'Rango', 'review_score' : 'Puntuaciones'}) # Renombramos columnas y devolvemos DataFrame

# Método para obtener los pedidos que se han retrasado en su entrega
def obtain_late_orders_per_city():

    # Obtenemos copias de los Dataframes originales para no sobreesecibir los almacenados en caché
    orders = data.orders().copy()
    customers = data.customers().copy()

    # Transformams las fechas a datetime de Pandas para poder operar de una mejor manera con ellas
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
    orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

    # Obtenemos los días que se han tardado entre la fecha de entrega al cliente y la fecha de entrega esperada al cliente
    days_measurement = (orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']).dt.days

    # Filtramos el dataframe por los pedidos que han sido repartidos, donde la fecha de entrega es mayor a la fecha de espera de entrega
    # y donde la diferencia de dias sea mayor a 0, ya que si no lo hacemos podríamos incluir pedidos que se han entregado ese mismo día
    # y es correcto excluirlos, debido a que son pedidos que se han podido entregar esa misma tarde o noche (NOS QUEDAMOS CON RETRASOS REALES)
    df_late_orders = orders[
        (orders['order_delivered_customer_date'] > orders['order_estimated_delivery_date']) 
        & (orders['order_status'] == 'delivered') & (days_measurement > 0)
    ]

    # Hacemos un merge con los clientes para poder acceder a las ciudades y a sus estados
    df_late_orders_per_city = pd.merge(df_late_orders, customers, on='customer_id')

    # Normalizamos la columna de junte de la ciudad del cliente y el estado del cliente
    df_late_orders_per_city['state_city'] = (df_late_orders_per_city['customer_city'].str.capitalize() + ' (' + df_late_orders_per_city['customer_state'] + ')')

    return df_late_orders_per_city # Devolvemos el DataFrame con los datos en crudo

# Método en el que obtenemos los pedidos que se han retrsado agrupando por la ciudad y su estado, se le paso como argumento el número que introduzca el usuario en Streamlit
def late_orders_per_city(number : int):

    # Creamos copia temporal para no modificar el DataFrame original
    late_order_per_city = obtain_late_orders_per_city().copy()

    # Agrupamos por la ciudad y estado, obtenemos DataFrame y lo ordenamos de manera descendente
    dframe = late_order_per_city.groupby('state_city').size().sort_values(ascending=False).to_frame()

    # Normalizamos columnas y retornamos, nos quedamos con los registros que el usuario nos pida en Streamlit
    return dframe.reset_index().rename(columns={'state_city' : 'Ciudad (Estado)', 0 : 'Cantidad Pedidos'}).head(n=number)

# Método con el que obtenemos el porcentaje de pedidos retrasados por la ciudad y estado del cliente
def late_orders_percentage(number : int):

    # Creamos copias temporales para no modificar los DataFrames originales
    orders = data.orders().copy()
    customers = data.customers().copy()

    # Hacemos merge de los clientes y los pedidos para tener una base de datos más grande sobre la que trabajar
    df_customers_orders_all = pd.merge(orders, customers, on='customer_id')
    
    # Normalizamos la columna de 'state_city' donde guardaremos la ciudad acompañada del estado 
    df_customers_orders_all['state_city'] = (df_customers_orders_all['customer_city'].str.capitalize() + ' (' + df_customers_orders_all['customer_state'] + ')')

    # Hacemos merge de dos datasets distintos, uno será el DataFrame que contendrá el total de pedidos y el otro contendrá el total de pedidos atrasados
    # Usamos la columna que hemos normalizado anteriormente como clave común y indicamos que queremos hacer un left join para obtener todos los pedidos completos 
    # y rellenamos los nulos con 0 para evitar valores anómalos
    df_orders_percentage = pd.merge(df_customers_orders_all.groupby('state_city').size().reset_index(name='total_orders'),
                                obtain_late_orders_per_city().groupby('state_city').size().reset_index(name='total_late_orders'), on='state_city', how='left').fillna(0)

    # Creamos una columna 'percentage' donde vamos a reflejar el porcentaje de pedidos atrasados de esa ciudad respecto al total de pedidos completo, redondeamos
    # el valor para hacerlo más legible
    df_orders_percentage['percentage'] = round((df_orders_percentage['total_late_orders'] / 
                                      df_orders_percentage['total_orders']) * 100, 2)

    # Ordenamos los valores del Dataframe, reseteamos los indices y renombramos las columnas antes de devolver el DataFrame, nos quedamos con los registros que el usuario nos pida en Streamlit
    return df_orders_percentage.sort_values(by='total_late_orders', ascending=[False]).reset_index().rename(columns={'state_city' : 'Ciudad (Estado)', 'percentage' : 'Porcentaje'}).head(n=number)

# Método con el que obtenemos un DataFrame con los días de retraso de los pedidos atrasados
def obtain_late_orders_days():
    
    # Creamos copia temporal del DataFrame para no modificar el original
    df_time_days = obtain_late_orders_per_city().copy()

    # Cambiamos de tipo a datetime de Pandas las columnas para poder trabajar con ellas de manera más cómoda
    df_time_days['order_delivered_customer_date'] = pd.to_datetime(df_time_days['order_delivered_customer_date'])
    df_time_days['order_estimated_delivery_date'] = pd.to_datetime(df_time_days['order_estimated_delivery_date'])

    # Obtenemos los días de retraso de los pedidos atrasados a partir de la diferencia de fechas, nos quedamos con los días
    df_time_days['late_days'] = (df_time_days['order_delivered_customer_date'] - df_time_days['order_estimated_delivery_date']).dt.days

    return df_time_days


# Método para obtener la media de retraso de los pedidos atrasados en días
def late_orders_days_mean(number : int):

    # Creamos una copia temporal del DataFrame con la que conseguimos no sobreescribir el DataFrame original
    df_mean_time_days = obtain_late_orders_days().copy()

    # Agrupamos por nuestra columna que contiene la ciudad y el estado y obtenemos la media de los días de retraso, ordenamos los valores, convertimos a DataFrame,
    # reseteamos índices para mayor legibilidad y renombramos las columnas, nos quedamos con los registros que el usuario nos pida en Streamlit
    return df_mean_time_days.groupby('state_city')['late_days'].mean().sort_values(ascending=False).to_frame().reset_index().rename(columns={'state_city' : 'Ciudad (Estado)', 'late_days' : 'Media Dias de Retraso'}).head(n=number)