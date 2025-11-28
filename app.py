import streamlit as st
from src.data_manager import DataManager
from src.ai_search import busca_inteligente
from views import home, employer, candidate, admin

# Configuração da Página
st.set_page_config(
    page_title="LabBD Vagas",
    page_icon="rocket",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização de Estado e Dados
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()

if 'user' not in st.session_state:
    st.session_state.user = None

dm = st.session_state.data_manager

# --- Sidebar (Autenticação e Navegação) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2910/2910791.png", width=100) # Logo genérico
    st.title("LabBD Jobs")
    
    if st.session_state.data_manager:
        st.success("MongoDB Conectado 🟢")

    if st.session_state.user:
        st.success(f"Olá, {st.session_state.user['name']}")
        st.info(f"Perfil: {st.session_state.user['role']}")
        if st.button("Sair"):
            st.session_state.user = None
            st.rerun()
    else:
        st.subheader("Login")
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            user = dm.authenticate(u, p)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Credenciais inválidas")
        
        st.markdown("---")
        st.caption("Contas Demo: admin/123, empresa/123, candidato/123")

# --- Roteamento de Views ---

if st.session_state.user is None:
    # Usuário não logado vê a Home
    home.render_home(dm)

else:
    role = st.session_state.user['role']
    
    if role == 'admin':
        # Admin vê tudo
        st.title("Painel Administrativo")
        tab1, tab2 = st.tabs(["Todos os Candidatos", "Todas as Vagas"])
        with tab1: st.dataframe(dm.get_curriculos())
        with tab2: st.dataframe(dm.get_vagas())

    elif role == 'employer':
        employer.render_employer(dm, st.session_state.user)
        
    elif role == 'candidate':
        st.title("Painel do Candidato")
        
        # Exemplo de uso da IA na view do candidato
        st.subheader("Assistente de Carreira (RAG)")
        query = st.text_input("Descreva o emprego dos seus sonhos: ")
        if query:
            df_vagas = dm.get_vagas()
            resultados = busca_inteligente(query, df_vagas, tipo="vaga")
            st.dataframe(resultados[['titulo', 'empresa', 'skills', 'salario']])
        
        st.divider()
        # Aqui importaria candidate.render_candidate...
        st.write("Funcionalidades de cadastro de currículo aqui...")