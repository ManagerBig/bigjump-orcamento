import streamlit as st

st.set_page_config(page_title="Orçamento Personalizado - Big Jump", layout="centered")
st.title("📝 Criador de Orçamento de Festa - Big Jump")

st.sidebar.header("Preencha os dados do orçamento")

nome_cliente = st.sidebar.text_input("Nome do Cliente")
data_evento = st.sidebar.date_input("Data da Festa")

st.markdown("---")
st.write("Aguardando os dados completos para configurar o sistema...")
