import streamlit as st
import exs.pers_metric_2 as ps2


def pers_metric_2():

    st.title(
        'Métrica personalizada Nº 2\n'
        '- Análisis de métodos de pago'
    )

    df = ps2.payment_type_global()
    st.bar_chart(df, x='Método de pago', y='Cantidad')
    st.dataframe(df, hide_index=True)


if __name__ == "__main__":
    pers_metric_2()
