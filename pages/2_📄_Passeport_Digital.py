import pandas as pd
import streamlit as st

from utils.data import generate_competitions, generate_horses, generate_vet_records

st.set_page_config(page_title="EquiScan AI — Passeport digital", page_icon="📄", layout="wide")


@st.cache_data
def load():
    horses = generate_horses(60)
    vet = generate_vet_records(horses)
    comps = generate_competitions(horses)
    return horses, vet, comps


horses_df, vet_df, comps_df = load()

st.title("Passeport digital")
st.caption("Remplace le carnet papier — identité, historique et documents du cheval, en un seul endroit")

selected = st.selectbox("Sélectionner un cheval", horses_df["id"] + " — " + horses_df["nom"])
horse_id = selected.split(" — ")[0]
h = horses_df[horses_df["id"] == horse_id].iloc[0]

col1, col2 = st.columns([1, 2])
with col1:
    st.image("https://placehold.co/400x400?text=Photo+cheval", use_container_width=True)
    st.markdown(f"### {h['id']}")
    st.code(f"RFID  {h['rfid']}\nQR    {h['qr']}", language=None)
    st.download_button("⬇️ Exporter le passeport (PDF)", data=f"Passeport digital — {h['nom']} ({h['id']})",
                        file_name=f"passeport_{h['id']}.txt", use_container_width=True)

with col2:
    tab1, tab2, tab3, tab4 = st.tabs(["Identité", "Historique vétérinaire", "Compétitions", "Timeline"])

    with tab1:
        st.markdown(f"**Nom :** {h['nom']}")
        st.markdown(f"**Race :** {h['race']}")
        st.markdown(f"**Sexe :** {h['sexe']}")
        st.markdown(f"**Âge :** {h['age']} ans — né le {h['date_naissance']}")
        st.markdown(f"**Statut :** {h['statut']}")
        st.markdown(f"**Propriétaire :** {h['proprietaire']}")
        st.markdown(f"**Éleveur :** {h['eleveur']}")
        st.markdown(f"**Haras de rattachement :** {h['haras']}  ·  Box {h['box']}")

    with tab2:
        hv = vet_df[vet_df["cheval_id"] == horse_id].copy()
        if hv.empty:
            st.info("Aucun événement vétérinaire enregistré pour ce cheval.")
        else:
            hv["date"] = pd.to_datetime(hv["date"]).dt.strftime("%d/%m/%Y")
            st.dataframe(
                hv.rename(columns={"date": "Date", "motif": "Motif", "veterinaire": "Vétérinaire", "notes": "Notes"})
                [["Date", "Motif", "Vétérinaire", "Notes"]],
                hide_index=True, use_container_width=True,
            )

    with tab3:
        hc = comps_df[comps_df["cheval_id"] == horse_id].copy()
        if hc.empty:
            st.info("Aucune compétition enregistrée pour ce cheval.")
        else:
            hc["date"] = pd.to_datetime(hc["date"]).dt.strftime("%d/%m/%Y")
            st.dataframe(
                hc.rename(columns={"date": "Date", "competition": "Compétition", "classement": "Classement"})
                [["Date", "Compétition", "Classement"]],
                hide_index=True, use_container_width=True,
            )

    with tab4:
        events = []
        for _, r in vet_df[vet_df["cheval_id"] == horse_id].iterrows():
            events.append((r["date"], f"🩺 {r['motif']} — {r['veterinaire']}"))
        for _, r in comps_df[comps_df["cheval_id"] == horse_id].iterrows():
            events.append((r["date"], f"🏆 {r['competition']} — classement {r['classement']}"))
        events.sort(key=lambda x: x[0], reverse=True)
        if not events:
            st.info("Aucun événement enregistré.")
        for d, label in events:
            st.markdown(f"**{pd.to_datetime(d).strftime('%d/%m/%Y')}** — {label}")
