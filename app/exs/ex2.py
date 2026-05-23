import numpy as np
import pandas as pd
import streamlit as st
import seeders.load_data as data
from exs import ex1


def obtain_number_orders():


    customers = data.customers().copy()
    orders = data.orders().copy()

    orders.loc[:, "order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])

    min_date = orders["order_purchase_timestamp"].min()
    max_date = orders["order_purchase_timestamp"].max()

    start_date = st.datetime_input("Selecciona la fecha de inicio:", value= min_date, min_value=min_date, max_value=max_date, key="start_date")
    start_date = pd.to_datetime(start_date)


    end_date = st.datetime_input("Selecciona la fecha de fin:", value=max_date, min_value=min_date, max_value=max_date, key="end_date")
    end_date = pd.to_datetime(end_date)

    df_filtered = orders[(orders["order_purchase_timestamp"] >= start_date) & (orders["order_purchase_timestamp"] <= end_date)]
    
    total_pedidos = df_filtered["order_id"].count()

    df_filtered_orders = pd.merge(customers, df_filtered, on="customer_id")

    df_filtered_orders = df_filtered_orders.groupby(["customer_state", 
                                                     "customer_city"]).agg(**{"Nº Clientes por ciudad": ("customer_unique_id", "nunique"),
                                                                               "Nº Pedidos por ciudad": ("order_id", "count")}).rename(
                                                                                       columns={"customer_state": "Estado",
                                                                                                 "customer_city": "Ciudad"})
    

    df_filtered_orders["% Pedidos respecto al total"] = round(df_filtered_orders["Nº Pedidos por ciudad"] / total_pedidos * 100, 2)

    df_customer_orders = (df_filtered_orders["Nº Pedidos por ciudad"] / df_filtered_orders["Nº Clientes por ciudad"]).rename("Ratio de pedidos por cliente").reset_index()
    
    
    return df_filtered_orders.sort_values(ascending=False, by="% Pedidos respecto al total").head(n=25), df_customer_orders.sort_values(ascending=False, by="Ratio de pedidos por cliente").head(n=25)