import random

import streamlit as st

from utils.data import generate_horses

st.set_page_config(page_title="EquiScan AI — Élevage", page_icon="🧬", layout="wide")


@st.cache_data
def load():
    return generate_horses(60)


horses_df = load()

st.title("Élevage (Breeding)")
st.caption("Généalogie, pedigree et aide à la décision pour les croisements")

tab1, tab2 = st.tabs(["Pedigree d'un cheval", "Suivi des saillies et naissances"])

with tab1:
    selected = st.selectbox("Sélectionner un cheval", horses_df["id"] + " — " + horses_df["nom"])
    horse_id = selected.split(" — ")[0]
    h = horses_df[horses_df["id"] == horse_id].iloc[0]

    st.markdown(f"### Arbre généalogique — {h['nom']}")
    random.seed(hash(horse_id) % 1000)
    pere = random.choice(["Amir El Fassi", "Nour Al Atlas", "Baraka", "Faris"])
    mere = random.choice(["Warda", "Nadia El Baraka", "Chams", "Salma Al Andalous"])
    gp1, gp2, gp3, gp4 = random.sample(
        ["Tarik", "Yasmina", "Zephyr", "Lina", "Kacem", "Aya", "Malek", "Douha"], 4
    )

    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**Père**\n\n{pere}")
        st.caption(f"Grands-parents : {gp1}, {gp2}")
    with c2:
        st.info(f"**Mère**\n\n{mere}")
        st.caption(f"Grands-parents : {gp3}, {gp4}")

    st.success(f"**{h['nom']}** — {h['race']}, {h['sexe']}, {h['age']} ans")

with tab2:
    st.subheader("Compatibilité de croisement (aide à la décision)")
    c1, c2 = st.columns(2)
    male = c1.selectbox("Étalon", horses_df[horses_df["sexe"] == "Mâle"]["nom"].unique())
    femelle = c2.selectbox("Jument", horses_df[horses_df["sexe"] == "Femelle"]["nom"].unique())
    if st.button("Évaluer la compatibilité"):
        score = random.randint(62, 96)
        st.metric("Score de compatibilité génétique estimé", f"{score}%")
        st.progress(score / 100)
        st.caption(
            "Score calculé à partir de la diversité génétique, des performances des lignées "
            "et de l'absence de consanguinité connue (démo simulée)."
        )

    st.divider()
    st.subheader("Naissances récentes")
    st.dataframe(
        {
            "Poulain": ["Anas Jr", "Widad Jr", "Reda Jr"],
            "Père": [pere, "Baraka", "Faris"],
            "Mère": [mere, "Chams", "Salma Al Andalous"],
            "Date de naissance": ["12/03/2026", "28/02/2026", "05/01/2026"],
            "Haras": ["Bouznika", "Meknès", "El Jadida"],
        },
        hide_index=True, use_container_width=True,
    )
