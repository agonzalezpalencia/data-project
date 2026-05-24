import streamlit as st
import matplotlib.pyplot as plt
import exs.pers_metric_1 as ps1

def pers_metric_1():

    # Creamos el título de la página y un input númerico que delimitará los registros que queremos obtener en el gráfico final
    st.title(f'Métrica personalizada Nº 1\n' +
                '- Distribución de volumen de ventas según categoría de producto sobre el total de productos')
    n_metric = st.number_input('Número de  Categorías: ', min_value=1, max_value=100, value=15, key='n_delivered')

    # Declaramos la métrica en base a las filas que quiera ver el usuario en el gráfico
    pers_metric_1 = ps1.order_percentage_per_category(n_metric)

    # Construcción del gráfico circular: declaramos las etiquetas y las 'porciones' o 'quesitos' de nuestro diagrama 
    labels = pers_metric_1['Categoria']
    sizes = pers_metric_1['Porcentaje']

    # Declaramos el contenedor y el área del gfráfico
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#0e1117')

    # Declaramos el gráfico en base a las etiquetas y porciones, tambien nos quedamos con los textos de las categorías y los textos de las porciones (Porcentajes)
    _, texts, autotexts =  ax.pie(sizes, autopct='%1.1f%%', shadow=True, startangle=90, labels=labels)

    # Recorremos los textos de las categorías y los ponemos de color blanco, además reducimos un poco el tamaño para no solapar nombres
    for text in texts:
        text.set_color('White')
        text.set_fontsize(6)

#    Recorremos los textos de las porciones o porcentajes y reducimos un poco el tamaño para no solapar los porcentajes
    for autotext in autotexts:
        autotext.set_fontsize(6)

    # normalizamos los ejes y mostramos la figura que hemos configurado
    ax.axis('equal')
    st.pyplot(fig)

# Protegemos la ejecución para que se ejecute únicamente cuando llamamos al archivo
if __name__ == "__main__":
    pers_metric_1()

