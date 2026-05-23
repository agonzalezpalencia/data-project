import numpy as np
import pandas as pd
from seeders import load_data as data

def get_raw_reviews_state_customer():

    orders = data.orders()
    customers = data.customers()
    orders_reviews = data.order_review()

    raw_df_reviews_state = pd.merge(orders, orders_reviews, on='order_id')

    raw_df_reviews_state['order_delivered_customer_date'] = pd.to_datetime(raw_df_reviews_state['order_delivered_customer_date'])
    raw_df_reviews_state['order_estimated_delivery_date'] = pd.to_datetime(raw_df_reviews_state['order_estimated_delivery_date'])

    df_reviews_state = raw_df_reviews_state[(raw_df_reviews_state['order_delivered_customer_date'] 
                                             <= raw_df_reviews_state['order_estimated_delivery_date'])]

    raw_df_reviews_state_customer = pd.merge(df_reviews_state, customers, on='customer_id')

    raw_df_reviews_state_customer['state_city'] = (raw_df_reviews_state_customer['customer_city'].str.capitalize() 
                                                   + ' (' + raw_df_reviews_state_customer['customer_state'] + ')')
    
    return raw_df_reviews_state_customer

def reviews_count_per_state():

    raw_df = get_raw_reviews_state_customer() 


    df_reviews_state_customer = raw_df.groupby(['state_city', 'order_status']).size().to_frame().reset_index().rename(
        columns={'state_city' : 'Ciudad (Estado)', 
                 'order_status' : 'Estado', 
                0 : 'Cant. Pedidos'}).sort_values(
                     by='Cant. Pedidos', 
                     ascending=False)
    
    return df_reviews_state_customer
