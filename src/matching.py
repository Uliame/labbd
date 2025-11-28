def calcular_score(skills_vaga, skills_candidato):
    """
    Retorna um score de 0 a 100 baseado na interseção de habilidades.
    Espera strings separadas por vírgula.
    """
    if not isinstance(skills_vaga, str) or not isinstance(skills_candidato, str):
        return 0
    
    set_vaga = set([s.strip().lower() for s in skills_vaga.split(',')])
    set_cand = set([s.strip().lower() for s in skills_candidato.split(',')])
    
    if len(set_vaga) == 0: return 0
    
    match = set_vaga.intersection(set_cand)
    score = (len(match) / len(set_vaga)) * 100
    return round(score, 1)