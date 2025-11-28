import pandas as pd

# Coordenadas de alguns estados
COORDS = {
    'SP': {'lat': -23.5505, 'lon': -46.6333},
    'RJ': {'lat': -22.9068, 'lon': -43.1729},
    'SC': {'lat': -27.5954, 'lon': -48.5480},
    'MG': {'lat': -19.9167, 'lon': -43.9345},
    # Adicione outros conforme necessário...
}

def adicionar_lat_lon(df_vagas):
    # Adiciona colunas de lat/lon para exibição no mapa
    if df_vagas.empty:
        return df_vagas
    
    def get_coords(estado):
        # Pequeno random para não ficar todos os pontos um em cima do outro
        base = COORDS.get(estado.strip().upper(), {'lat': -15.7801, 'lon': -47.9292})
        return base['lat'], base['lon']

    coords = df_vagas['estado'].apply(get_coords)
    df_vagas['lat'] = [c[0] for c in coords]
    df_vagas['lon'] = [c[1] for c in coords]
    return df_vagas