import streamlit as st
import matplotlib.pyplot as plt
import exs.ex2 as ex2


def exercise2_metric_1():

    ex2_df_orders, ex2_df_customers_orders = ex2.obtain_number_orders()

    st.dataframe(ex2_df_orders)

    st.subheader("Nº de pedidos por cada ciudad")
    st.scatter_chart(ex2_df_customers_orders, x="customer_city", x_label="Ciudades", y="Ratio de pedidos por cliente")


if __name__ == "__main__":
    exercise2_metric_1()