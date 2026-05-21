import numpy as np
import pandas as pd
from seeders import load_data as data

def obtain_late_orders_per_city():

    orders = data.orders().copy()
    customers = data.customers().copy()

    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
    orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

    days_measurement = (orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']).dt.days

    df_late_orders = orders[
        (orders['order_delivered_customer_date'] > orders['order_estimated_delivery_date']) 
        & (orders['order_status'] == 'delivered') & (days_measurement > 0)
    ]

    df_late_orders_per_city = pd.merge(df_late_orders, customers, on='customer_id')

    df_late_orders_per_city['customer_city'] = df_late_orders_per_city['customer_city'].str.capitalize()

    return df_late_orders_per_city


def late_orders_per_city():

    late_order_per_city = obtain_late_orders_per_city()

    final_frame = late_order_per_city.groupby('customer_city').size().sort_values(ascending=False).to_frame()

    return final_frame.reset_index().rename(columns={'customer_city' : 'Ciudad', 0 : 'Cantidad Pedidos'}).head(n=25)


def late_orders_percentage():

    orders = data.orders().copy()
    customers = data.customers().copy()

    df_customers_orders_all = pd.merge(orders, customers, on='customer_id')
    df_customers_orders_all['customer_city'] = df_customers_orders_all['customer_city'].str.capitalize()

    df_orders_percentage = pd.merge(df_customers_orders_all.groupby('customer_city').size().reset_index(name='total_orders'),
                                obtain_late_orders_per_city().groupby('customer_city').size().reset_index(name='total_late_orders'), on='customer_city', how='left').fillna(0)

    df_orders_percentage['percentage'] = round((df_orders_percentage['total_late_orders'] / 
                                      df_orders_percentage['total_orders']) * 100, 2)

    return df_orders_percentage.sort_values(by='percentage', ascending=[False]).reset_index().rename(columns={'customer_city' : 'Ciudad', 'percentage' : 'Porcentaje'}).head(n=50)

def late_orders_days_mean():

    df_mean_time_days = obtain_late_orders_per_city().copy()
    df_mean_time_days['order_delivered_customer_date'] = df_mean_time_days['order_delivered_customer_date'].astype('date64[pyarrow]')
    df_mean_time_days['order_estimated_delivery_date'] = df_mean_time_days['order_estimated_delivery_date'].astype('date64[pyarrow]')

    df_mean_time_days['late_days'] = (df_mean_time_days['order_delivered_customer_date'] - df_mean_time_days['order_estimated_delivery_date']).dt.days

    return df_mean_time_days.groupby('customer_city')['late_days'].mean().sort_values(ascending=False).to_frame()