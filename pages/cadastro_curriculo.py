import streamlit as st

st.title("Cadastro de Currículo")

with st.form("form_curriculo"):
    nome = st.text_input("Nome completo:")
    email = st.text_input("Email:")
    telefone = st.text_input("Telefone:")
    cidade = st.selectbox("Cidade:", ['Rio Claro', 'São Paulo', 'Espírito Santo do Pinhal', 'Cumpenis'])
    area = st.text_input("Área de atuação:")
    experiencia = st.text_area("Experiências anteriores:")
    habilidades = st.text_area("Habilidades:")
    enviar = st.form_submit_button("Cadastrar Currículo")

if enviar:
    if nome and email:
        st.success(f"Currículo de {nome} cadastrado!")
    else:
        st.error("Preencha todos os campos obrigatórios.")
