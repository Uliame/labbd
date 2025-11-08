import streamlit as st

st.title("Cadastro de Vaga")

with st.form("form_vaga"):
    titulo = st.text_input("Título da vaga:")
    empresa = st.text_input("Empresa:")
    cidade = st.selectbox("Cidade:", ['Rio Claro', 'São Paulo', 'Espírito Santo do Pinhal', 'Campinas'])
    salario = st.text_input("Salário:")
    descricao = st.text_area("Descrição da vaga:")
    requisitos = st.text_area("Requisitos:")
    enviar = st.form_submit_button("Cadastrar Vaga")

if enviar:
    if titulo and empresa and cidade:
        st.success(f"A vaga de {titulo} foi cadastrada com sucesso!")
    else:
        st.error("Preencha todos os campos obrigatórios.")
