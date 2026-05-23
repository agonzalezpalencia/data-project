import streamlit as st
import matplotlib.pyplot as plt
import exs.ex1 as ex1


def exercise1_metric_1():

    ex1_metric1 = ex1.obtain_number_customers_per_city()
    st.dataframe(ex1_metric1)

    st.subheader("Número de clientes por ciudad")

    st.bar_chart(ex1_metric1, x="Ciudad", y="Nº Clientes por ciudad")


if __name__ == "__main__":
    exercise1_metric_1()