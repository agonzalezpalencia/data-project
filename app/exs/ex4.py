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

def get_reviews_count_per_state():

    raw_df = get_raw_reviews_state_customer() 


    df_reviews_state_customer = raw_df.groupby(['state_city', 'order_status']).size().to_frame().reset_index().rename(
        columns={'state_city' : 'Ciudad (Estado)', 
                 'order_status' : 'Estado', 
                 0 : 'Cantidad Reviews'}).sort_values(
                     by='Cantidad Reviews', 
                     ascending=False)
    
    return df_reviews_state_customer


def delivered_reviews_count_per_state():

    delivered_reviews_count_per_state = get_reviews_count_per_state()
    
    return delivered_reviews_count_per_state[delivered_reviews_count_per_state['Estado'] == 'delivered'].reset_index().head(n=25)


def canceled_reviews_count_per_state():

    canceled_reviews_count_per_state = get_reviews_count_per_state()
    
    return canceled_reviews_count_per_state[canceled_reviews_count_per_state['Estado'] == 'canceled'].reset_index().head(n=5)


def mean_reviews_score_per_state():

    raw_df = get_raw_reviews_state_customer() 

    raw_df_reviews_state_customer_orders = raw_df.groupby(['state_city', 'order_status']).size().to_frame()
    raw_df_reviews_state_customer_ratings_mean = raw_df.groupby(['state_city', 'order_status'])['review_score'].mean().to_frame()

    raw_df_reviews_state_customer_ratings_orders = pd.merge(raw_df_reviews_state_customer_orders, raw_df_reviews_state_customer_ratings_mean, on=['state_city','order_status'] )
    df_reviews_state_customer_ratings_orders = raw_df_reviews_state_customer_ratings_orders.reset_index().sort_values(
                    0, ascending=False).rename(
                        columns={'state_city' : 'Ciudad (Estado)', 
                                 'order_status' : 'Estado', 
                                 0 : 'Cantidad Reviews', 
                                 'review_score' : 'Puntuacion'})
    
    df_reviews_state_customer_ratings_orders['Puntuacion'] = round(df_reviews_state_customer_ratings_orders['Puntuacion'], 2)

    return df_reviews_state_customer_ratings_orders

def delivered_mean_reviews_score_per_state():

    delivered_mean_reviews_score_per_state = mean_reviews_score_per_state()

    return delivered_mean_reviews_score_per_state[delivered_mean_reviews_score_per_state['Estado'] == 'delivered'].reset_index().head(n=25)

def canceled_mean_reviews_score_per_state():

    canceled_mean_reviews_score_per_state = mean_reviews_score_per_state()

    return canceled_mean_reviews_score_per_state[canceled_mean_reviews_score_per_state['Estado'] == 'canceled'].reset_index().head(n=5)



