import streamlit as st

if __name__ == "__main__":
    pg = st.navigation([st.Page("streamlit_pages/ex1_executable.py", title='Ejercicio 1'),
                        st.Page("streamlit_pages/ex2_executable.py", title='Ejercicio 2'), 
                        st.Page('streamlit_pages/ex3_executable.py', title='Ejercicio 3'),
                        st.Page("streamlit_pages/ex4_executable.py", title='Ejercicio 4')])
    
    pg.run()