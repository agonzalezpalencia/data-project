import pandas as pd
from seeders import load_data as data


def payment_type_global():
    payments = data.order_payments()

    df_payments = (
        payments.groupby('payment_type').size().sort_values(
            ascending=False).reset_index().rename(
                columns={'payment_type': 'Método de pago',
                          0: 'Cantidad'})
    )
    df_payments = df_payments[df_payments["Método de pago"] != "not_defined"]
    df_payments['Método de pago'] = df_payments['Método de pago'].str.replace('_', ' ').str.capitalize()
  
    df_payments['Porcentaje (%)'] = (df_payments['Cantidad'] / df_payments['Cantidad'].sum() * 100).round(1)

    return df_payments