import numpy as np
import pandas as pd
import streamlit as st
import seeders.load_data as data

def obtain_number_customers_per_city():

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
 

    df_filtered_orders = pd.merge(customers, df_filtered, on="customer_id")

    df_filtered_orders = df_filtered_orders.groupby(["customer_state", "customer_city"]).size().sort_values(ascending=False).reset_index(name="Nº Clientes por ciudad").rename(columns={"customer_state": "Estado", "customer_city": "Ciudad"})


    return df_filtered_orders.head(n=25)


