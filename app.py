import streamlit as st
import time

#st.logo("https://www2.unesp.br/images/unesp-full-center.svg")
st.image("https://www2.unesp.br/images/unesp-full-center.svg", width=500)

with st.sidebar:
    st.title("Configurações: ")
    st.selectbox("Escolha uma cidade: ", ['Rio Claro', 'São Paulo', 'Espírito Santo do Pinhal', 'Cumpenis'])

st.title(" ")

with st.spinner("Carregando balões..."):
    time.sleep(5)
    
st.balloons()

nome    = st.text_input("Nome: ")
senha   = st.text_input("Senha: ", type="password")

with st.form("meu_form"):
    st.title("Cadastro de Usuário")
    nome    = st.text_input("Nome: ")
    senha   = st.text_input("Senha: ", type="password")
    cidade  = st.selectbox("Escolha uma cidade: ", ['Rio Claro', 'São Paulo', 'Espírito Santo do Pinhal', 'Cumpenis'])
    if st.form_submit_button("Enviar"): 
        st.write(nome, " da cidade ", cidade)
