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

# Método para obtener el número de clientes filtrado por estado y ciudad del cliente
def obtain_number_customers_per_city(number : int, start_date, end_date):

    # Creamos instancias temporales de los Dataframes, para no modificar los originales
    customers = data.customers().copy()
    orders = data.orders().copy()

    # Cambiamos el tipo de order_pruchase_timestamp para poder operar con él y decidir el rango de fechas dinámico desde el dashboard de Streamlit
    orders.loc[:, "order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])

    # Definimos fecha de inicio y de fin
    st_date = pd.to_datetime(start_date)
    ed_date = pd.to_datetime(end_date)

    # Filtramos los pedidos por las fechas
    df_filtered = orders[(orders["order_purchase_timestamp"] >= st_date) & (orders["order_purchase_timestamp"] <= ed_date)]

    # Hacemos un join con el DataFrame de clientes por el 'customer_id', para poder acceder a las ciudades y a los estados
    df_filtered_orders = pd.merge(customers, df_filtered, on="customer_id")

    # Normalizamos el nombre de la ciudad
    df_filtered_orders['customer_city'] = df_filtered_orders['customer_city'].str.capitalize()

    # Normalizamos los datos y realizamos el filtrado para quedarnos con los datos que nos interesan mostrar, agrupamos por el estado y ciudad y obtenemos
    # los clientes unicos, ordenamos de manera descendente, reseteamos índices para poder acceder a los datos más fácilmente y renombramos las columnas que necesitamos
    df_filtered_orders = df_filtered_orders.groupby(["customer_state", 
                                                     "customer_city"])['customer_unique_id'].nunique().sort_values(ascending=False).reset_index(
                                                         name="Nº Clientes por ciudad").rename(
                                                             columns={"customer_state": "Estado", 
                                                                      "customer_city": "Ciudad"})

    return df_filtered_orders.head(n=number) # Devolvemos el DataFrame según el número que se nos pase en streamlit


