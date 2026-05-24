import numpy as np
import pandas as pd
from seeders import load_data as data

# Método que nos devuelve el porcentaje de pedidos por cada categoría del producto, usada para represnetar un diágrama circular (cake)
def order_percentage_per_category(number : int):

    # Hacemos copias de los Dataframes originales para no modificar los Dataframes originales
    order_items = data.order_items().copy()
    products = data.products().copy()

    # Creamos un dataset haciendo merge con 'order_items' y 'products', por el 'product_id', así obtenemos las categorías de los productos que se han pedido
    raw_df_order_items_products = pd.merge(order_items, products, on='product_id') 

    # Filtramos los que tengan categorías nulas para evitar distorsiones en la métrica final
    raw_df_order_items_products = raw_df_order_items_products[raw_df_order_items_products['product_category_name'].notna()]

    # Agrupamos el Dataframe por la caetgoría del producto, obtenemos el dataframe y lo ordenamos de manera descendente
    raw_df_order_items_products = raw_df_order_items_products.groupby('product_category_name').size().sort_values(ascending=False)

    # Reseteamos indices del Dataframe y renombramos las columnas que queremos mostrar más adelante (Porcentaje aún no convertido)
    df_order_items_products = raw_df_order_items_products.to_frame().reset_index().rename(columns={ 'product_category_name' : 'Categoria', 0 : 'Porcentaje'})

    # Normalizamos la columna de 'Categoría' y calculamos el porcentaje en base a la suma total de productos por categoría
    df_order_items_products['Categoria'] = df_order_items_products['Categoria'].str.replace('_', ' ').str.capitalize()
    df_order_items_products['Porcentaje'] = (df_order_items_products['Porcentaje'] / df_order_items_products['Porcentaje'].sum()) * 100

    # Retornamos el Dataframe con el número de filas que nos delimite el usuario
    return df_order_items_products.head(n=number)