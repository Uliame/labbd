import streamlit as st
from connection_mongo import vagas, curriculos

st.set_page_config(
    page_title="Sistema de Vagas e Currículos",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    /* Estilo geral */
    .main {
        padding: 2rem;
    }
    
    /* Cards de vagas */
    .vaga-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
    }
    
    .vaga-titulo {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .vaga-info {
        font-size: 0.95rem;
        margin: 0.3rem 0;
        opacity: 0.95;
    }
    
    /* Menu admin */
    .menu-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .menu-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Títulos */
    h1 {
        color: #667eea;
        font-weight: 700;
    }
    
    /* Botões */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    /* Login form */
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ======= CONFIGURAÇÕES DE LOGIN =======
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =============== LISTAR VAGAS (PÚBLICA) ===============
def mostrar_home():
    st.title("Vagas Disponíveis")
    st.markdown("### Encontre sua próxima oportunidade profissional")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        busca = st.text_input("Buscar por título ou empresa", "")
    with col2:
        cidade_filtro = st.selectbox(
            "Filtrar por cidade",
            ["Todas", "Rio Claro", "São Paulo", "Espírito Santo do Pinhal", "Campinas"]
        )
    
    lista_vagas = list(vagas.find())
    
    if not lista_vagas:
        st.info("Nenhuma vaga cadastrada ainda. Volte em breve!")
        return
    
    # Aplicar filtros
    vagas_filtradas = lista_vagas
    if busca:
        vagas_filtradas = [
            v for v in vagas_filtradas 
            if busca.lower() in v.get("titulo", "").lower() 
            or busca.lower() in v.get("empresa", "").lower()
        ]
    
    if cidade_filtro != "Todas":
        vagas_filtradas = [
            v for v in vagas_filtradas 
            if v.get("cidade", "") == cidade_filtro
        ]
    
    st.markdown(f"**{len(vagas_filtradas)}** vagas encontradas")
    
    # Exibir vagas em grid
    for i in range(0, len(vagas_filtradas), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(vagas_filtradas):
                vaga = vagas_filtradas[i + j]
                with col:
                    with st.container():
                        st.markdown(f"""
                        <div class="vaga-card">
                            <div class="vaga-titulo"> {vaga.get("titulo", "Sem título")}</div>
                            <div class="vaga-info"> <strong>{vaga.get('empresa', 'Não informado')}</strong></div>
                            <div class="vaga-info"> {vaga.get('salario', 'A combinar')}</div>
                            <div class="vaga-info"> {vaga.get('cidade', 'N/A')} - {vaga.get('estado', 'N/A')}</div>
                            <div class="vaga-info" style="margin-top: 0.8rem;">{vaga.get('descricao', 'Sem descrição')[:150]}...</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("")


# =============== TELA DO ADMINISTRADOR ===============
def tela_admin():
    st.title("👨‍💼 Painel Administrativo")
    st.markdown("### Bem-vindo ao sistema de gerenciamento")
    
    # Sidebar com estatísticas
    with st.sidebar:
        st.markdown("### Estatísticas")
        total_vagas = vagas.count_documents({})
        total_curriculos = curriculos.count_documents({})
        
        st.metric("Vagas Ativas", total_vagas, delta=None)
        st.metric("Currículos", total_curriculos, delta=None)
        st.divider()
        
        if st.button("Sair", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    
    # Menu principal
    st.markdown("### O que deseja fazer?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Cadastrar Vaga", use_container_width=True, type="primary"):
            st.switch_page("pages/cadastro_vaga.py")
        if st.button("Listar Vagas", use_container_width=True):
            st.switch_page("pages/listar_vagas.py")
    
    with col2:
        if st.button("Cadastrar Currículo", use_container_width=True, type="primary"):
            st.switch_page("pages/cadastro_curriculo.py")
        if st.button("Listar Currículos", use_container_width=True):
            st.switch_page("pages/listar_curriculos.py")
    
    with col3:
        if st.button("Recomendações", use_container_width=True, type="primary"):
            st.switch_page("pages/recomendacao.py")
        if st.button("Mapa de Vagas", use_container_width=True):
            st.switch_page("pages/localiza_cidades.py")
    
    st.divider()
    
    # Preview rápido
    st.markdown("### Últimas Atividades")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Vagas Recentes**")
        ultimas_vagas = list(vagas.find().sort("_id", -1).limit(3))
        if ultimas_vagas:
            for v in ultimas_vagas:
                st.markdown(f"• **{v.get('titulo')}** - {v.get('empresa')}")
        else:
            st.info("Nenhuma vaga cadastrada")
    
    with col2:
        st.markdown("**Currículos Recentes**")
        ultimos_curriculos = list(curriculos.find().sort("_id", -1).limit(3))
        if ultimos_curriculos:
            for c in ultimos_curriculos:
                st.markdown(f"• **{c.get('nome')}** - {c.get('area', 'N/A')}")
        else:
            st.info("Nenhum currículo cadastrado")


# =============== LOGIN ===============
def mostrar_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("### Acesso Administrativo")
        
        usuario = st.text_input("Usuário", key="user_input")
        senha = st.text_input("Senha", type="password", key="pass_input")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Entrar", use_container_width=True, type="primary"):
                if usuario == ADMIN_USER and senha == ADMIN_PASS:
                    st.session_state.logged_in = True
                    st.success("Login realizado!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos")
        
        with col_btn2:
            if st.button("Cancelar", use_container_width=True):
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.info("**Dica:** Use as credenciais de administrador para acessar o painel completo")


# =============== CONTROLE DE TELA ===============
if st.session_state.logged_in:
    tela_admin()
else:
    mostrar_login()
    st.divider()
    mostrar_home()