import time

def busca_inteligente(query, df_alvo, tipo="vaga"):
    """
    Simula um RAG. Recebe uma pergunta em linguagem natural e filtra o DataFrame.
    """
    # TODO: Implementar OpenAI Embeddings + Vector Store aqui
    time.sleep(1) # Simula processamento
    
    # Lógica "Fake" simples: busca textual keyword match
    query = query.lower()
    if tipo == "vaga":
        mask = df_alvo['descricao'].str.lower().str.contains(query) | \
               df_alvo['skills'].str.lower().str.contains(query)
    else:
        mask = df_alvo['resumo'].str.lower().str.contains(query) | \
               df_alvo['skills'].str.lower().str.contains(query)
               
    return df_alvo[mask]