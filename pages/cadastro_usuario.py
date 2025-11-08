import streamlit as st

# validação
def validar(nome, senha):
    if nome.strip() == "" or senha.strip() == "":
        return False
    return True

st.title("Cadastro de Usuários")

with st.form("cadusuario"):
    nome  = st.text_input("Nome:")
    senha = st.text_input("Senha:", type="password")
    submit = st.form_submit_button("Enviar")

if submit:
    if validar(nome, senha):
        st.success("Usuário inserido com sucesso!")
    else:
        st.warning("Por favor, preencha todos os campos corretamente.")