import numpy as np
import pandas as pd
from seeders import load_data as data

def obtain_carrier_customer_days():
    time_days = obtain_late_orders_days()

    time_days['order_delivered_carrier_date'] = pd.to_datetime(time_days['order_delivered_carrier_date'])
    time_days['order_purchase_timestamp'] = pd.to_datetime(time_days['order_purchase_timestamp'])

    time_days['mean_purchase_carrier'] = (time_days['order_delivered_carrier_date'] - time_days['order_purchase_timestamp']).dt.days
    time_days['mean_carrier_customer'] = (time_days['order_delivered_customer_date'] - time_days['order_delivered_carrier_date']).dt.days

    return time_days

def obtain_late_orders_count():

    time_days = obtain_late_orders_days()
    orders_reviews = data.order_review()

    df_late_orders_reviews = pd.merge(time_days, orders_reviews, on='order_id', how='left')

    bins = [0,2,5,10,20, int(df_late_orders_reviews['late_days'].max())]
    labels = ['0 a 2 dias', '2 a 5 dias', '5 a 10 dias', '10 a 20 dias', '20+ dias']

    df_late_orders_reviews['range'] = pd.cut(df_late_orders_reviews['late_days'], bins=bins, labels=labels)

    df_late_orders_count_ranges = df_late_orders_reviews.groupby('range', observed=True).size().reset_index().rename(columns={ 0 : 'count'})

    return df_late_orders_count_ranges


def obtain_late_orders_rating():

    time_days = obtain_late_orders_days()
    orders_reviews = data.order_review()

    df_late_orders_reviews = pd.merge(time_days, orders_reviews, on='order_id', how='left')

    bins = [0,2,5,10,20, int(df_late_orders_reviews['late_days'].max())]
    labels = ['0 a 2 dias', '2 a 5 dias', '5 a 10 dias', '10 a 20 dias', '20+ dias']

    df_late_orders_reviews['range'] = pd.cut(df_late_orders_reviews['late_days'], bins=bins, labels=labels)

    df_late_orders_rating_ranges = round(df_late_orders_reviews.groupby('range', observed=True)['review_score'].mean(), 2).reset_index()

    return df_late_orders_rating_ranges


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

    df_late_orders_per_city['state_city'] = (df_late_orders_per_city['customer_city'].str.capitalize() + ' (' + df_late_orders_per_city['customer_state'] + ')')

    return df_late_orders_per_city


def late_orders_per_city():

    late_order_per_city = obtain_late_orders_per_city()

    final_frame = late_order_per_city.groupby('state_city').size().sort_values(ascending=False).to_frame()

    return final_frame.reset_index().rename(columns={'state_city' : 'Ciudad (Estado)', 0 : 'Cantidad Pedidos'}).head(n=25)


def late_orders_percentage():

    orders = data.orders().copy()
    customers = data.customers().copy()

    df_customers_orders_all = pd.merge(orders, customers, on='customer_id')
    
    df_customers_orders_all['state_city'] = (df_customers_orders_all['customer_city'].str.capitalize() + ' (' + df_customers_orders_all['customer_state'] + ')')

    df_orders_percentage = pd.merge(df_customers_orders_all.groupby('state_city').size().reset_index(name='total_orders'),
                                obtain_late_orders_per_city().groupby('state_city').size().reset_index(name='total_late_orders'), on='state_city', how='left').fillna(0)

    df_orders_percentage['percentage'] = round((df_orders_percentage['total_late_orders'] / 
                                      df_orders_percentage['total_orders']) * 100, 2)

    return df_orders_percentage.sort_values(by='total_late_orders', ascending=[False]).reset_index().rename(columns={'state_city' : 'Ciudad (Estado)', 'percentage' : 'Porcentaje'}).head(n=25)

def obtain_late_orders_days():
    df_time_days = obtain_late_orders_per_city().copy()
    df_time_days['order_delivered_customer_date'] = pd.to_datetime(df_time_days['order_delivered_customer_date'])
    df_time_days['order_estimated_delivery_date'] = pd.to_datetime(df_time_days['order_estimated_delivery_date'])

    df_time_days['late_days'] = (df_time_days['order_delivered_customer_date'] - df_time_days['order_estimated_delivery_date']).dt.days

    return df_time_days



def late_orders_days_mean():

    df_mean_time_days = obtain_late_orders_days()

    return df_mean_time_days.groupby('state_city')['late_days'].mean().sort_values(ascending=False).to_frame().reset_index().rename(columns={'state_city' : 'Ciudad (Estado)', 'late_days' : 'Media Dias de Retraso'}).head(n=25)