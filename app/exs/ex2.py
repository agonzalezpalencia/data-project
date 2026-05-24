import numpy as np
import pandas as pd
import streamlit as st
import seeders.load_data as data

# Método para filtrar la fecha máxima y mínima del Dataset de order
def get_max_min_date():

    # Creamos una copia del Dataframe para no modificar el Dataframe origiinal guardado en caché
    orders = data.orders().copy()

    # Filtramos la fecha mínima y máxima
    min_date = orders["order_purchase_timestamp"].min()
    max_date = orders["order_purchase_timestamp"].max()

    return max_date, min_date

# Método para obtener el número de pedidos filtrado por ciudad y estado 
def obtain_number_orders(number : int, start_date, end_date):

    # Creamos copias de los DataFrames originales para no sobreescribir los ya cargados en caché
    customers = data.customers().copy()
    orders = data.orders().copy()

    # Cambiamos el tipo de order_pruchase_timestamp para poder operar con él y decidir el rango de fechas dinámico desde el dashboard de Streamlit
    orders.loc[:, "order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])

    # Definimos fecha de inicio y de fin
    st_date = pd.to_datetime(start_date)
    ed_date = pd.to_datetime(end_date)

     # Filtramos los pedidos por las fechas
    df_filtered = orders[(orders["order_purchase_timestamp"] >= st_date) & (orders["order_purchase_timestamp"] <= ed_date)]
    
    # Declaramos el total de pedidos 
    total_pedidos = df_filtered["order_id"].count()

    # Hacemos un join con el DataFrame de clientes por el 'customer_id', para poder acceder a las ciudades y a los estados
    df_filtered_orders = pd.merge(customers, df_filtered, on="customer_id")

    # Normalizamos el nombre de la ciudad
    df_filtered_orders['customer_city'] = df_filtered_orders['customer_city'].str.capitalize()

    # Normalizamos los datos y realizamos el filtrado para quedarnos con los datos que nos interesan mostrar, agrupamos por el estado y ciudad y realizamos una
    # función de agregación donde obtenemos los clientes unicos y la cantidad de pedidos total de la ciudad, reseteamos índices para poder acceder a los datos más fácilmente 
    # y renombramos las columnas que necesitamos
    df_filtered_orders = df_filtered_orders.groupby(["customer_state", 
                                                     "customer_city"]).agg(**{"Nº Clientes por ciudad": ("customer_unique_id", "nunique"),
                                                                               "Nº Pedidos por ciudad": ("order_id", "count")}).reset_index().rename(
                                                                                       columns={"customer_state" : "Estado",
                                                                                                 "customer_city" : "Ciudad"})

    # Definimos el porcentaje de los pedidos obtenidos respecto al total de pedidos que hemos definido anteriormente
    df_filtered_orders["% Pedidos respecto al total"] = round(df_filtered_orders["Nº Pedidos por ciudad"] / total_pedidos * 100, 2)

    # Creamos una copia del dataframe anterior para poder devolverlo más adelante, en este dataframe calcularemos el ratio de pedidos por cliente
    df_customer_orders = df_filtered_orders.copy()

    # Calculamos el ratio diviendo los pedidos de la ciudad entre los clientes de la ciudad
    df_customer_orders['Ratio de pedidos por cliente'] = (df_filtered_orders["Nº Pedidos por ciudad"] / df_filtered_orders["Nº Clientes por ciudad"])
    
    # Retornamos 2 Dataframes, uno contendrá el % de pedidos respecto al total, y el otro contendrá el ratio de pedidos, así separamos las dos representaciones
    return df_filtered_orders.sort_values(ascending=False, 
                                          by="% Pedidos respecto al total").head(n=number), df_customer_orders.sort_values(ascending=False, 
                                                                                                                           by="Ratio de pedidos por cliente").head(n=number)