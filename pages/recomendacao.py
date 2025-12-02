import streamlit as st
from connection_mongo import vagas, curriculos
from pymongo import TEXT

st.set_page_config(page_title="Recomendações", page_icon="🎯", layout="wide")

# CSS personalizado
st.markdown("""
<style>
    .page-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .candidato-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #f5576c;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .score-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .vaga-info-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Criar índices de texto
try:
    vagas.create_index([("titulo", TEXT), ("descricao", TEXT), ("requisitos", TEXT)])
    curriculos.create_index([
        ("nome", TEXT), ("experiencia", TEXT), ("formacao", TEXT), 
        ("resumo", TEXT), ("idiomas", TEXT), ("habilidades", TEXT), ("area", TEXT)
    ])
except:
    pass

# Header
st.markdown("""
<div class="page-header">
    <h1>Sistema de Recomendação Inteligente</h1>
    <p>Encontre os candidatos ideais para cada vaga usando tecnologia de busca avançada</p>
</div>
""", unsafe_allow_html=True)

# Botão voltar
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    if st.button("Voltar", use_container_width=True):
        st.switch_page("app.py")

st.markdown("---")

# Buscar vagas
lista_vagas = list(vagas.find({}))

if not lista_vagas:
    st.warning("Nenhuma vaga cadastrada no sistema.")
    if st.button("Cadastrar Vaga"):
        st.switch_page("pages/cadastro_vaga.py")
    st.stop()

# Criar dicionário de vagas
vaga_titulos = {f"{vaga['titulo']} - {vaga.get('empresa', 'N/A')}": vaga for vaga in lista_vagas}

# Seleção de vaga
st.markdown("### Selecione a Vaga")
titulo_selecionado = st.selectbox(
    "Escolha a vaga para ver candidatos recomendados:",
    list(vaga_titulos.keys()),
    help="Selecione uma vaga para ver os candidatos mais compatíveis"
)

if not titulo_selecionado:
    st.stop()

vaga_escolhida = vaga_titulos[titulo_selecionado]

# Exibir informações da vaga
st.markdown("### Detalhes da Vaga Selecionada")
st.markdown('<div class="vaga-info-box">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Título:** {vaga_escolhida['titulo']}")
    st.markdown(f"**Empresa:** {vaga_escolhida.get('empresa', 'Não informado')}")
    st.markdown(f"**Localização:** {vaga_escolhida.get('cidade', 'N/A')} - {vaga_escolhida.get('estado', 'N/A')}")
    st.markdown(f"**Salário:** {vaga_escolhida.get('salario', 'A combinar')}")

with col2:
    st.markdown(f"**Descrição:** {vaga_escolhida.get('descricao', 'Não informado')}")
    st.markdown(f"**Requisitos:** {vaga_escolhida.get('requisitos', 'Não informado')}")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Busca com Full Text Search
texto_busca = f"{vaga_escolhida.get('descricao', '')} {vaga_escolhida.get('requisitos', '')} {vaga_escolhida.get('titulo', '')}"

with st.spinner("Analisando candidatos..."):
    try:
        resultados = list(curriculos.aggregate([
            {
                "$match": {
                    "$text": {"$search": texto_busca}
                }
            },
            {
                "$addFields": {
                    "score": {"$meta": "textScore"}
                }
            },
            {
                "$sort": {"score": -1}
            },
            {
                "$limit": 20  # Limitar a 20 melhores resultados
            }
        ]))
    except Exception as e:
        st.error(f"Erro ao buscar candidatos: {e}")
        resultados = []

# Exibir resultados
st.markdown("### 👥 Candidatos Recomendados")

if not resultados:
    st.info("Nenhum candidato com match significativo para esta vaga.")
    st.markdown("**Sugestões:**")
    st.markdown("- Revise os requisitos da vaga")
    st.markdown("- Adicione mais palavras-chave na descrição")
    st.markdown("- Cadastre novos currículos no sistema")
else:
    # Estatísticas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Candidatos Encontrados", len(resultados))
    with col2:
        media_score = sum([c.get('score', 0) for c in resultados]) / len(resultados)
        st.metric("Score Médio", f"{media_score:.2f}")
    with col3:
        top_score = resultados[0].get('score', 0) if resultados else 0
        st.metric("Melhor Match", f"{top_score:.2f}")
    
    st.markdown("---")
    
    # Filtro de score mínimo
    score_minimo = st.slider(
        "Filtrar por score mínimo:",
        min_value=0.0,
        max_value=float(max([r.get('score', 0) for r in resultados])),
        value=0.0,
        step=0.5,
        help="Ajuste para ver apenas candidatos com score acima do valor selecionado"
    )
    
    resultados_filtrados = [r for r in resultados if r.get('score', 0) >= score_minimo]
    
    st.markdown(f"**{len(resultados_filtrados)}** candidato(s) exibido(s)")
    
    # Exibir candidatos
    for i, c in enumerate(resultados_filtrados, 1):
        st.markdown('<div class="candidato-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {i}. {c.get('nome', 'Sem nome')}")
            st.markdown(f"**E-mail:** {c.get('email', 'Não informado')}")
            st.markdown(f"**Telefone:** {c.get('telefone', 'Não informado')}")
            st.markdown(f"**Cidade:** {c.get('cidade', 'Não informado')}")
            st.markdown(f"**Área:** {c.get('area', 'Não informado')}")
        
        with col2:
            score = c.get('score', 0)
            # Calcular percentual (score normalizado)
            max_score = resultados[0].get('score', 1) if resultados else 1
            percentual = int((score / max_score) * 100) if max_score > 0 else 0
            
            st.markdown(f'<div class="score-badge">Match: {percentual}%</div>', unsafe_allow_html=True)
            st.markdown(f"**Score:** {score:.4f}")
        
        # Expandir para ver mais detalhes
        with st.expander("Ver detalhes completos"):
            st.markdown("**Formação:**")
            st.write(c.get('formacao', 'Não informado'))
            
            st.markdown("**Habilidades:**")
            st.write(c.get('habilidades', 'Não informado'))
            
            st.markdown("**Experiência:**")
            st.write(c.get('experiencia', 'Não informado'))
            
            # Botão de contato
            email = c.get('email', '')
            if email:
                st.markdown(f"[Enviar E-mail](mailto:{email})")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Dicas
st.markdown("---")
with st.expander("Como funciona o sistema de recomendação?"):
    st.markdown("""
    O sistema utiliza **Full Text Search** do MongoDB para analisar a compatibilidade entre vagas e candidatos:
    
    1. **Análise de Texto:** O sistema analisa descrição, requisitos e título da vaga
    2. **Busca Inteligente:** Compara com habilidades, experiência e formação dos candidatos
    3. **Score de Match:** Gera uma pontuação baseada na relevância textual
    4. **Ranking:** Ordena candidatos do mais compatível para o menos compatível
    
    **Score mais alto = maior compatibilidade com a vaga**
    """)