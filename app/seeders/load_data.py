import numpy as np
import pandas as pd
import streamlit as st
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def customers():
    df_customers_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/customers_dataset.csv'))
    return df_customers_all

@st.cache_data
def order_items():     
    df_order_items_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/order_items_dataset.csv'))
    return df_order_items_all

@st.cache_data
def order_payments(): 
    df_order_payments_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/order_payments_dataset.csv'))
    return df_order_payments_all

@st.cache_data
def order_review():
    df_order_reviews_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/order_reviews_dataset.csv'))
    return df_order_reviews_all

@st.cache_data
def orders():
    df_orders_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/orders_dataset.csv'))
    return df_orders_all

@st.cache_data
def product_category_name_translation():
    df_product_category_name_translation_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/product_category_name_translation.csv'))
    return df_product_category_name_translation_all

@st.cache_data
def products():
    df_products_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/products_dataset.csv'))
    return df_products_all

@st.cache_data
def sellers():
    df_sellers_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/sellers_dataset.csv'))
    return df_sellers_all