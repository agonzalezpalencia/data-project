import numpy as np
import pandas as pd
import streamlit as st
import seeders.load_data as data

def get_max_min_date():

    orders = data.orders().copy()

    min_date = orders["order_purchase_timestamp"].min()
    max_date = orders["order_purchase_timestamp"].max()

    return max_date, min_date

def obtain_number_orders(number : int, start_date, end_date):

    customers = data.customers().copy()
    orders = data.orders().copy()

    orders.loc[:, "order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])

    st_date = pd.to_datetime(start_date)
    ed_date = pd.to_datetime(end_date)

    df_filtered = orders[(orders["order_purchase_timestamp"] >= st_date) & (orders["order_purchase_timestamp"] <= ed_date)]
    
    total_pedidos = df_filtered["order_id"].count()

    df_filtered_orders = pd.merge(customers, df_filtered, on="customer_id")

    df_filtered_orders['customer_city'] = df_filtered_orders['customer_city'].str.capitalize()

    df_filtered_orders = df_filtered_orders.groupby(["customer_state", 
                                                     "customer_city"]).agg(**{"Nº Clientes por ciudad": ("customer_unique_id", "nunique"),
                                                                               "Nº Pedidos por ciudad": ("order_id", "count")}).reset_index().rename(
                                                                                       columns={"customer_state" : "Estado",
                                                                                                 "customer_city" : "Ciudad"})

    df_filtered_orders["% Pedidos respecto al total"] = round(df_filtered_orders["Nº Pedidos por ciudad"] / total_pedidos * 100, 2)

    df_customer_orders = df_filtered_orders.copy()

    df_customer_orders['Ratio de pedidos por cliente'] = (df_filtered_orders["Nº Pedidos por ciudad"] / df_filtered_orders["Nº Clientes por ciudad"])
    
    return df_filtered_orders.sort_values(ascending=False, 
                                          by="% Pedidos respecto al total").head(n=number), df_customer_orders.sort_values(ascending=False, 
                                                                                                                           by="Ratio de pedidos por cliente").head(n=number)