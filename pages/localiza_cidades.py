import streamlit as st
import pandas as pd
import pydeck as pdk
from connection_mongo import vagas  # usar coleção do Mongo

# ---------------------------
# Carrega lat/lon do CSV
# ---------------------------
@st.cache_data
def carregar_coordenadas():
    df = pd.read_csv("pages/cidades/cidades_brasil.csv")
    df["chave"] = df["cidade"] + "-" + df["estado"]
    return df.set_index("chave")[["lat", "lon"]].to_dict("index")


def main():
    st.title("Distribuição Geográfica das Vagas")
    st.write("Explore o mapa interativo e veja todas as vagas por cidade.")

    if st.button("Voltar para a Home"):
        st.switch_page("app.py")

    COORDENADAS = carregar_coordenadas()

    # ===============================
    # Carregar vagas do MongoDB
    # ===============================
    lista_vagas = list(vagas.find({}, {
        "_id": 0,
        "id": 1,
        "titulo": 1,
        "empresa": 1,
        "cidade": 1,
        "estado": 1,
        "tipo_contratacao": 1,
        "salario": 1,
        "descricao": 1
    }))

    if not lista_vagas:
        st.warning("Nenhuma vaga cadastrada para exibir.")
        return

    df = pd.DataFrame(lista_vagas)

    # ===============================
    # Agrupar por cidade + estado
    # ===============================
    agrupado = df.groupby(["cidade", "estado"])

    pontos = []

    for (cidade, estado), grupo in agrupado:
        chave = f"{cidade}-{estado}"

        if chave not in COORDENADAS:
            continue

        coord = COORDENADAS[chave]

        # Tooltip com todas vagas da cidade
        vagas_html = "<br>".join(
            [f"• {row['titulo']} — {row['empresa']}" for _, row in grupo.iterrows()]
        )

        tooltip_html = f"""
        <b>{cidade} - {estado}</b><br>
        ----------------------------------<br>
        {vagas_html}
        """

        pontos.append({
            "lat": float(coord["lat"]),
            "lon": float(coord["lon"]),
            "tooltip": tooltip_html
        })

    if not pontos:
        st.error("Nenhuma cidade com coordenadas encontradas.")
        return

    coords_df = pd.DataFrame(pontos)

    # ===============================
    # Configuração do mapa
    # ===============================
    view_state = pdk.ViewState(
        latitude=-14.2350,
        longitude=-51.9253,
        zoom=4,
        pitch=30,
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        coords_df,
        get_position=["lon", "lat"],
        get_radius=30000,
        get_color=[30, 136, 229, 200],
        pickable=True,
        auto_highlight=True,
        get_tooltip="tooltip"
    )

    tooltip = {
        "html": "{tooltip}",
        "style": {"backgroundColor": "rgba(20,20,20,0.9)", "color": "white"}
    }

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
    )

    st.pydeck_chart(deck)


if __name__ == "__main__":
    main()
