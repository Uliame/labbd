import streamlit as st
import pandas as pd
import os

def listar_curriculos(caminho_arquivo):
    """
    Lê o arquivo CSV de currículos a partir de um caminho fixo e o exibe.
    """
    st.header("Lista de Currículos")
    try:
        # Verifica se o arquivo existe no caminho especificado
        if os.path.exists(caminho_arquivo):
            # Lê o CSV usando pandas, especificando o ponto e vírgula como separador
            df_curriculos = pd.read_csv(caminho_arquivo, sep=';')
            st.dataframe(df_curriculos)
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
    st.title("Visualizador de Currículos")

    
    CAMINHO_ARQUIVO = "src\dataset\curriculos.csv" 

    listar_curriculos(CAMINHO_ARQUIVO)