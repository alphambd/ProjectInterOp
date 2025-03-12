import streamlit as st
from pages import stock, ventes, commandes

st.set_page_config(page_title="Pharmacie Plus", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à :", ["Stock", "Ventes", "Commandes"])

if page == "Stock":
    stock.show_stock_page()
elif page == "Ventes":
    ventes.show_ventes_page()
elif page == "Commandes":
    commandes.show_commandes_page()
