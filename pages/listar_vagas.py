import streamlit as st
import pandas as pd
import os

def listar_vagas(caminho_arquivo):
    """
    Lê o arquivo CSV de vagas a partir de um caminho fixo e o exibe.
    """
    st.header("Lista de Vagas")
    try:
        # Verifica se o arquivo existe no caminho especificado
        if os.path.exists(caminho_arquivo):
            # Lê o CSV usando pandas, especificando o ponto e vírgola como separador
            df_vagas = pd.read_csv(caminho_arquivo, sep=';')
            st.dataframe(df_vagas)
        else:
            st.error(f"Arquivo não encontrado no caminho: '{caminho_arquivo}'")
            st.info("Verifique se a variável 'CAMINHO_ARQUIVO' no script está correta.")
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado no caminho: '{caminho_arquivo}'")
    except pd.errors.ParserError:
        st.error(f"Erro ao processar o arquivo '{caminho_arquivo}'. Verifique o formato e o separador.")
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao ler '{caminho_arquivo}': {e}")

if __name__ == "__main__":
    st.title("Visualizador de Vagas")

    CAMINHO_ARQUIVO = "src\dataset\vagas.csv"

    listar_vagas(CAMINHO_ARQUIVO)