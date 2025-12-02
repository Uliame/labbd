import streamlit as st
from connection_mongo import curriculos

# ----------------------------
# Botão voltar para a home
# ----------------------------
if st.button("Voltar para a Home"):
    st.switch_page("app.py")


st.title("Cadastro de Currículo")

# opções de cidade
cidades = ['Rio Claro', 'São Paulo', 'Espírito Santo do Pinhal', 'Campenas']

# Inicializa valores padrões (opcional — evita KeyError)
if "nome_input" not in st.session_state:
    st.session_state.nome_input = ""
if "email_input" not in st.session_state:
    st.session_state.email_input = ""
if "telefone_input" not in st.session_state:
    st.session_state.telefone_input = ""
if "cidade_input" not in st.session_state:
    st.session_state.cidade_input = cidades[0]
if "area_input" not in st.session_state:
    st.session_state.area_input = ""
if "experiencia_input" not in st.session_state:
    st.session_state.experiencia_input = ""
if "habilidades_input" not in st.session_state:
    st.session_state.habilidades_input = ""

# Função que será chamada ao clicar no botão (callback)
def submit_callback():
    nome = st.session_state.nome_input.strip()
    email = st.session_state.email_input.strip()
    telefone = st.session_state.telefone_input.strip()
    cidade = st.session_state.cidade_input
    area = st.session_state.area_input.strip()
    experiencia = st.session_state.experiencia_input.strip()
    habilidades = st.session_state.habilidades_input.strip()

    if not nome or not email:
        # mostrar mensagem de erro (no callback funciona)
        st.session_state._feedback = ("error", "Preencha os campos obrigatórios: Nome e Email.")
        return

    documento = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "cidade": cidade,
        "area": area,
        "experiencia": experiencia,
        "habilidades": habilidades
    }

    try:
        curriculos.insert_one(documento)

        # limpar os campos — fazemos isso *na mesma função* antes de qualquer rerun
        st.session_state.nome_input = ""
        st.session_state.email_input = ""
        st.session_state.telefone_input = ""
        st.session_state.cidade_input = cidades[0]
        st.session_state.area_input = ""
        st.session_state.experiencia_input = ""
        st.session_state.habilidades_input = ""

        # armazenar feedback para exibir fora do callback
        st.session_state._feedback = ("success", f"Currículo de {nome} cadastrado com sucesso! 🎉")

    except Exception as e:
        st.session_state._feedback = ("error", f"Erro ao salvar no banco: {e}")


# ----------------------------
# FORMULÁRIO
# ----------------------------
with st.form("form_curriculo"):
    st.text_input("Nome completo:", key="nome_input", value=st.session_state.nome_input)
    st.text_input("Email:", key="email_input", value=st.session_state.email_input)
    st.text_input("Telefone:", key="telefone_input", value=st.session_state.telefone_input)

    st.selectbox(
        "Cidade:",
        cidades,
        index=cidades.index(st.session_state.cidade_input),
        key="cidade_input"
    )

    st.text_input("Área de atuação:", key="area_input", value=st.session_state.area_input)
    st.text_area("Experiências anteriores:", key="experiencia_input", value=st.session_state.experiencia_input)
    st.text_area("Habilidades:", key="habilidades_input", value=st.session_state.habilidades_input)

    # note o uso do on_click que chama a função que salva e limpa
    st.form_submit_button("Cadastrar Currículo", on_click=submit_callback)

# ----------------------------
# Exibir feedback (mensagem) após a tentativa de envio
# ----------------------------
if "_feedback" in st.session_state:
    kind, message = st.session_state._feedback
    if kind == "success":
        st.success(message)
    else:
        st.error(message)
    # opcional: remover feedback para não repetir sempre
    del st.session_state._feedback

