import streamlit as st
from src.matching import calcular_score

def render_employer(data_manager, user):
    st.title(f"Painel da Empresa: {user['name']}")
    
    tab1, tab2 = st.tabs(["Cadastrar Vaga", "Gerenciar Vagas e Matching"])
    
    with tab1:
        st.subheader("Nova Vaga")
        with st.form("form_vaga"):
            titulo = st.text_input("Título da Vaga")
            desc = st.text_area("Descrição")
            col1, col2 = st.columns(2)
            cidade = col1.text_input("Cidade")
            estado = col2.text_input("Estado (Sigla)")
            salario = st.text_input("Salário")
            skills = st.text_input("Skills (separadas por vírgula)")
            
            submitted = st.form_submit_button("Publicar Vaga")
            if submitted:
                nova_vaga = {
                    "titulo": titulo, "descricao": desc, "cidade": cidade,
                    "estado": estado, "salario": salario, "empresa": user['name'],
                    "skills": skills, "tipo_contratacao": "CLT"
                }
                data_manager.save_vaga(nova_vaga)
                st.success("Vaga publicada com sucesso!")

    with tab2:
        st.subheader("Suas Vagas e Candidatos Recomendados")
        df_vagas = data_manager.get_vagas()
        # Filtra vagas apenas desta empresa
        minhas_vagas = df_vagas[df_vagas['empresa'] == user['name']]
        
        vaga_selecionada = st.selectbox("Selecione uma vaga para ver recomendações:", minhas_vagas['titulo'].unique())
        
        if vaga_selecionada:
            # Pega dados da vaga
            dados_vaga = minhas_vagas[minhas_vagas['titulo'] == vaga_selecionada].iloc[0]
            st.markdown(f"**Requisitos:** {dados_vaga['skills']}")
            
            # Busca currículos e calcula match
            df_curriculos = data_manager.get_curriculos()
            if not df_curriculos.empty:
                df_curriculos['Match Score'] = df_curriculos['skills'].apply(
                    lambda x: calcular_score(dados_vaga['skills'], x)
                )
                
                # Ordena pelo melhor score
                melhores = df_curriculos.sort_values(by='Match Score', ascending=False)
                
                st.write("### Melhores Candidatos")
                st.dataframe(
                    melhores[['nome', 'email', 'Match Score', 'skills']],
                    use_container_width=True
                )