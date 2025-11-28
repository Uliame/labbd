import streamlit as st
from src.utils import adicionar_lat_lon

def render_home(data_manager):
    st.title("Portal de Vagas de Emprego")
    st.markdown("Encontre a oportunidade perfeita ou o talento ideal.")

    df_vagas = data_manager.get_vagas()

    # Mapa de Vagas ^^
    st.subheader("Distribuição de Oportunidades")
    if not df_vagas.empty:
        df_mapa = adicionar_lat_lon(df_vagas.copy())
        st.map(df_mapa, latitude='lat', longitude='lon', size=20)
    else:
        st.info("Nenhuma vaga mapeada.")

    # Listagem Pública :o
    st.divider()
    st.subheader("Vagas Recentes")
    for index, row in df_vagas.head(5).iterrows():
        with st.expander(f"{row['titulo']} - {row['empresa']} ({row['cidade']}/{row['estado']})"):
            st.write(f"**Salário:** {row['salario']}")
            st.write(f"**Descrição:** {row['descricao']}")
            st.write(f"**Requisitos:** {row['skills']}")
            st.info("Faça login como candidato para se aplicar.")