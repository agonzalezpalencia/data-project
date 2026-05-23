import numpy as np
import pandas as pd
import streamlit as st
import seeders.load_data as data

def get_max_min_date():

    orders = data.orders().copy()

    min_date = orders["order_purchase_timestamp"].min()
    max_date = orders["order_purchase_timestamp"].max()

    return max_date, min_date

def obtain_number_customers_per_city(number : int, start_date, end_date):

    customers = data.customers().copy()
    orders = data.orders().copy()

    orders.loc[:, "order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])

    st_date = pd.to_datetime(start_date)
    ed_date = pd.to_datetime(end_date)

    df_filtered = orders[(orders["order_purchase_timestamp"] >= st_date) & (orders["order_purchase_timestamp"] <= ed_date)]

    df_filtered_orders = pd.merge(customers, df_filtered, on="customer_id")

    df_filtered_orders['customer_city'] = df_filtered_orders['customer_city'].str.capitalize()

    df_filtered_orders = df_filtered_orders.groupby(["customer_state", 
                                                     "customer_city"])['customer_unique_id'].nunique().sort_values(ascending=False).reset_index(
                                                         name="Nº Clientes por ciudad").rename(
                                                             columns={"customer_state": "Estado", 
                                                                      "customer_city": "Ciudad"})

    return df_filtered_orders.head(n=number)


