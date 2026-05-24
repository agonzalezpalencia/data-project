import numpy as np
import pandas as pd
import streamlit as st
import os

# Utilizamos el directorio base desde el que se llama al archivo para que tanto en local como en producción, elija correctamente la ruta de acceso al archivo load_data.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Archivo de Python que se encarga de proveer los Dataframes a la capa de lógica de nuestro proyecto, usamos el decorador de 'st.cache_data' para que durante
# el flujo del proyecto solo se carguen los Dataframes una vez en caché y se reutilicen durante todo el flujo del proyecto, optimizando la gestión de recursos
# al máximo posible

@st.cache_data
def customers():
    df_customers_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/datasets/customers_dataset.csv'))
    return df_customers_all

@st.cache_data
def order_items():     
    df_order_items_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/datasets/order_items_dataset.csv'))
    return df_order_items_all

@st.cache_data
def order_payments(): 
    df_order_payments_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/datasets/order_payments_dataset.csv'))
    return df_order_payments_all

@st.cache_data
def order_review():
    df_order_reviews_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/datasets/order_reviews_dataset.csv'))
    return df_order_reviews_all

@st.cache_data
def orders():
    df_orders_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/datasets/orders_dataset.csv'))
    return df_orders_all

@st.cache_data
def product_category_name_translation():
    df_product_category_name_translation_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/datasets/product_category_name_translation.csv'))
    return df_product_category_name_translation_all

@st.cache_data
def products():
    df_products_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/datasets/products_dataset.csv'))
    return df_products_all

@st.cache_data
def sellers():
    df_sellers_all = pd.read_csv(os.path.join(BASE_DIR, '../../documents/datasets/sellers_dataset.csv'))
    return df_sellers_all