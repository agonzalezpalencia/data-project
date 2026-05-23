import numpy as np
import pandas as pd
from seeders import load_data as data

def order_percentage_per_category(number : int):

    order_items = data.order_items()
    products = data.products()

    raw_df_order_items_products = pd.merge(order_items, products, on='product_id') 
    raw_df_order_items_products = raw_df_order_items_products[raw_df_order_items_products['product_category_name'].notna()]

    raw_df_order_items_products = raw_df_order_items_products.groupby('product_category_name').size().sort_values(ascending=False)

    df_order_items_products = raw_df_order_items_products.to_frame().reset_index().rename(columns={ 'product_category_name' : 'Categoria', 0 : 'Porcentaje'})

    df_order_items_products['Categoria'] = df_order_items_products['Categoria'].str.replace('_', ' ').str.capitalize()
    df_order_items_products['Porcentaje'] = (df_order_items_products['Porcentaje'] / df_order_items_products['Porcentaje'].sum()) * 100

    return df_order_items_products.head(n=number)