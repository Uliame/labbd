import streamlit as st
from connection_mongo import vagas

st.title("Cadastro de Vaga")

# ----------------------------
# Botão voltar para a home
# ----------------------------
if st.button("Voltar para a Home"):
    st.switch_page("app.py")


# Inicializa os valores somente uma vez
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "titulo": "",
        "empresa": "",
        "cidade": "Rio Claro",
        "salario": "",
        "descricao": "",
        "requisitos": ""
    }

# ---------------------------------
# FORMULÁRIO
# ---------------------------------
with st.form("form_vaga"):
    titulo = st.text_input("Título da vaga:", value=st.session_state.form_data["titulo"])
    empresa = st.text_input("Empresa:", value=st.session_state.form_data["empresa"])
    cidade = st.selectbox(
        "Cidade:",
        ['Rio Claro', 'São Paulo', 'Espírito Santo do Pinhal', 'Campinas'],
        index=['Rio Claro', 'São Paulo', 'Espírito Santo do Pinhal', 'Campinas'].index(st.session_state.form_data["cidade"])
    )
    salario = st.text_input("Salário:", value=st.session_state.form_data["salario"])
    descricao = st.text_area("Descrição da vaga:", value=st.session_state.form_data["descricao"])
    requisitos = st.text_area("Requisitos:", value=st.session_state.form_data["requisitos"])

    enviar = st.form_submit_button("Cadastrar Vaga")

# ---------------------------------
# SALVAR NO BANCO
# ---------------------------------
if enviar:
    if titulo and empresa and cidade:

        documento = {
            "titulo": titulo,
            "empresa": empresa,
            "cidade": cidade,
            "salario": salario,
            "descricao": descricao,
            "requisitos": requisitos
        }

        try:
            vagas.insert_one(documento)
            st.success("Vaga cadastrada com sucesso!")

            # LIMPA O FORMULÁRIO DE VERDADE
            st.session_state.form_data = {
                "titulo": "",
                "empresa": "",
                "cidade": "Rio Claro",
                "salario": "",
                "descricao": "",
                "requisitos": ""
            }

            st.rerun()  # recarrega a página com o formulário vazio

        except Exception as e:
            st.error(f"Erro ao salvar no banco: {e}")

    else:
        st.error("Preencha todos os campos obrigatórios.")

