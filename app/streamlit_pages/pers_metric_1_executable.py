import streamlit as st
import matplotlib.pyplot as plt
import exs.pers_metric_1 as ps1

def pers_metric_1():

    st.title(f'Métrica personalizada Nº 1\n' +
                '- Distribución de volumen de ventas según categoría de producto sobre el total de productos')
    n_metric = st.number_input('Número de  Categorías: ', min_value=1, max_value=100, value=15, key='n_delivered')
    pers_metric_1 = ps1.order_percentage_per_category(n_metric)
    labels = pers_metric_1['Categoria']
    sizes = pers_metric_1['Porcentaje']

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#0e1117')
    _, texts, autotexts =  ax.pie(sizes, autopct='%1.1f%%', shadow=True, startangle=90, labels=labels)

    for text in texts:
        text.set_color('White')
        text.set_fontsize(6)

    for autotext in autotexts:
        autotext.set_fontsize(6)

    ax.axis('equal')
    st.pyplot(fig)

if __name__ == "__main__":
    pers_metric_1()

