import streamlit as st

def cadastro_usuario(nome, senha):
    return
def validar(nome, senha):
    if nome=="" or senha=="":
        return False
    return True

with st.form("cadusuario:"):
    st.title("Cadastro de usuários")
    nome    = st.text_input("Nome: ")
    senha   = st.text_input("Senha: ", type="password")
    submit  = st.form_submit_button("Enviar")
    
if submit and validar(nome, senha):
    cadastro_usuario(nome, senha)
    st.success("Inserido com sucesso")
elif submit:
    st.warning("Dados inválidos")

st.write(st.secrets["db_username"])