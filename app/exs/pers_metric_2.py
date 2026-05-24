import pandas as pd
from seeders import load_data as data

# Método con el que se obtiene las cantidades de usos de los métodos de pago en los pagos de los pedidos
def payment_type_global():

    # Hacemos una copia del Dataframe para no sobreescribir el original
    payments = data.order_payments().copy()

    # Declaramos el dataframe en el cual vamos a grupar por el tipo de pago, ordenaremos de manera descendente estas cantidades, reseteamos los índices
    # para acceder más comodamente a las columnas y por último renombramos las columnas que nos interesan
    df_payments = (
        payments.groupby('payment_type').size().sort_values(
            ascending=False).reset_index().rename(
                columns={'payment_type': 'Método de pago',
                          0: 'Cantidad'})
    )

    # Excluimos los métodos de pago 'not_defined' puesto a que sus pagos tienen un precio de 0, no aportan nada a la métrica
    df_payments = df_payments[df_payments["Método de pago"] != "not_defined"]

    # Normalizamos la columna de métodos de pago
    df_payments['Método de pago'] = df_payments['Método de pago'].str.replace('_', ' ').str.capitalize()
  
    # Calculamos el porcentaje respecto a la cantidad total de pedidos
    df_payments['Porcentaje (%)'] = (df_payments['Cantidad'] / df_payments['Cantidad'].sum() * 100).round(1)

    # Retornamos el dataframe
    return df_payments