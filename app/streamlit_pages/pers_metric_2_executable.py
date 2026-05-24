import streamlit as st
import matplotlib.pyplot as plt
import exs.pers_metric_2 as ps2

# Método que carga en Streamlit la segunda métrica personalizada con un gráfico de barras
def pers_metric_2_1():

    # Ponemos un título a la página
    st.title(
        'Métrica personalizada Nº 2\n'
        '- Análisis de métodos de pago en función del total de tipos de pago, representación en gráfico de barras'
    )

    # Declaramos el Dataframe que queremos mostrar en el gráfico de barras y en el gráfico circular (cake)
    df = ps2.payment_type_global()

    # Mostramos el gráfico de barras, tomando como 'x' los tipos de métodos de pago y en la 'y' 
    # la cantidad de esos métodos de pago respecto el total de tipos de pago
    st.bar_chart(df, x='Método de pago', y='Cantidad')

# Método que carga en Streamlit la segunda métrica personalizada con un diagrama circular (cake)
def pers_metric_2_2():

    # Damos un título al gráfico que vamos a representar dando un feedback al usuario
    st.markdown('- Análisis de métodos de pago en función del total de tipos de pago, representación en diagrama circular (cake)')

    # Creamos el dataframe desde el que vamos a extraer los datos
    df_pers_metric_2_2 = ps2.payment_type_global()

    # Construcción del gráfico circular: declaramos las etiquetas y las 'porciones' o 'quesitos' de nuestro diagrama 
    labels = df_pers_metric_2_2['Método de pago']
    sizes = df_pers_metric_2_2['Porcentaje (%)']

    # Declaramos el contenedor y el área del gfráfico
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#0e1117')

    # Declaramos el gráfico en base a las etiquetas y porciones, tambien nos quedamos con los textos de las categorías y los textos de las porciones (Porcentajes)
    _, texts, autotexts =  ax.pie(sizes, autopct='%1.1f%%', shadow=True, startangle=90, labels=labels)

    # Recorremos los textos de las categorías y los ponemos de color blanco, además reducimos un poco el tamaño para no solapar nombres
    for text in texts:
        text.set_color('White')
        text.set_fontsize(6)

    # Recorremos los textos de las porciones o porcentajes y reducimos un poco el tamaño para no solapar los porcentajes
    for autotext in autotexts:
        autotext.set_fontsize(6)

    # Normalizamos los ejes y mostramos la figura que hemos configurado
    ax.axis('equal')
    st.pyplot(fig)
    


# Protegemos la ejecución para que se ejecute únicamente cuando llamamos al archivo
if __name__ == "__main__":
    pers_metric_2_1()
    pers_metric_2_2()
