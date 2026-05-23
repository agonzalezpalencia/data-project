import streamlit as st

if __name__ == "__main__":
    pg = st.navigation([st.Page("streamlit_pages/ex1_executable.py", title='Ejercicio 1'),
                        st.Page("streamlit_pages/ex2_executable.py", title='Ejercicio 2'), 
                        st.Page('streamlit_pages/ex3_executable.py', title='Ejercicio 3'),
                        st.Page("streamlit_pages/ex4_executable.py", title='Ejercicio 4'),
                        st.Page("streamlit_pages/pers_metric_1_executable.py", title='Métrica Personalizada Nº 1'),
                        st.Page("streamlit_pages/pers_metric_2_executable.py", title='Métrica Personalizada Nº 2')])
    
    pg.run()