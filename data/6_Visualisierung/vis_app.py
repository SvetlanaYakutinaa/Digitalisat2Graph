import streamlit as st

pg = st.navigation([
    st.Page("seite_1.py", title="Über das Projekt"),
    st.Page("seite_2.py", title="Netzwerk"),
    st.Page("seite_3.py", title="Räumliche Visualisierung"),
])
st.set_page_config(page_title="Digitalisat2Graph")
pg.run()


