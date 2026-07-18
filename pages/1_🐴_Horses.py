import streamlit as st

from utils.data import generate_horses

st.set_page_config(page_title="EquiScan AI — Horses", page_icon="🐴", layout="wide")


@st.cache_data
def load():
    return generate_horses(60)


horses_df = load()

st.title("Gestion des chevaux")
st.caption("Base de données centralisée du cheptel")

col1, col2, col3, col4 = st.columns(4)
haras_f = col1.multiselect("Haras", sorted(horses_df["haras"].unique()))
race_f = col2.multiselect("Race", sorted(horses_df["race"].unique()))
statut_f = col3.multiselect("Statut", sorted(horses_df["statut"].unique()))
search = col4.text_input("Recherche (nom, ID, propriétaire)")

filtered = horses_df.copy()
if haras_f:
    filtered = filtered[filtered["haras"].isin(haras_f)]
if race_f:
    filtered = filtered[filtered["race"].isin(race_f)]
if statut_f:
    filtered = filtered[filtered["statut"].isin(statut_f)]
if search:
    s = search.lower()
    filtered = filtered[
        filtered["nom"].str.lower().str.contains(s)
        | filtered["id"].str.lower().str.contains(s)
        | filtered["proprietaire"].str.lower().str.contains(s)
    ]

st.caption(f"{len(filtered)} cheval(aux) trouvé(s) sur {len(horses_df)}")

st.dataframe(
    filtered.rename(columns={
        "id": "ID", "nom": "Nom", "race": "Race", "sexe": "Sexe", "age": "Âge",
        "statut": "Statut", "proprietaire": "Propriétaire", "eleveur": "Éleveur",
        "haras": "Haras", "box": "Box",
    })[["ID", "Nom", "Race", "Sexe", "Âge", "Statut", "Propriétaire", "Éleveur", "Haras", "Box"]],
    hide_index=True, use_container_width=True, height=420,
)

st.divider()
st.subheader("Voir la fiche d'un cheval")
selected = st.selectbox("Sélectionner un cheval", filtered["id"] + " — " + filtered["nom"])
if selected:
    horse_id = selected.split(" — ")[0]
    h = horses_df[horses_df["id"] == horse_id].iloc[0]

    c1, c2 = st.columns([1, 2])
    with c1:
        st.image("https://placehold.co/400x400?text=Photo+cheval", use_container_width=True)
        st.caption(f"RFID : `{h['rfid']}`")
        st.caption(f"QR code : `{h['qr']}`")
    with c2:
        st.markdown(f"## {h['nom']}")
        st.markdown(f"**Statut :** {h['statut']}")
        st.markdown(f"**Race :** {h['race']}  ·  **Sexe :** {h['sexe']}  ·  **Âge :** {h['age']} ans")
        st.markdown(f"**Date de naissance :** {h['date_naissance']}")
        st.markdown(f"**Propriétaire :** {h['proprietaire']}")
        st.markdown(f"**Éleveur :** {h['eleveur']}")
        st.markdown(f"**Haras :** {h['haras']}  ·  **Box :** {h['box']}")
        st.info("Consultez l'onglet **Passeport digital** pour l'historique complet du cycle de vie.")
