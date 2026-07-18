import pandas as pd
import streamlit as st

from utils.data import generate_horses, generate_upcoming_vaccinations, generate_vet_records

st.set_page_config(page_title="EquiScan AI — Vétérinaire", page_icon="🩺", layout="wide")


@st.cache_data
def load():
    horses = generate_horses(60)
    vet = generate_vet_records(horses)
    vacc = generate_upcoming_vaccinations(horses, n=20)
    return horses, vet, vacc


horses_df, vet_df, vacc_df = load()

st.title("Module vétérinaire")
st.caption("Historique médical, vaccinations et alertes automatiques")

tab1, tab2, tab3 = st.tabs(["Alertes & vaccinations", "Historique des consultations", "Ajouter une consultation"])

with tab1:
    st.subheader("Vaccinations à venir — alertes automatiques")
    vacc_show = vacc_df.copy()
    vacc_show["date_prevue"] = pd.to_datetime(vacc_show["date_prevue"])
    vacc_show["urgence"] = vacc_show["date_prevue"].apply(
        lambda d: "🔴 Urgent" if (d - pd.Timestamp.now()).days <= 3 else ("🟠 Bientôt" if (d - pd.Timestamp.now()).days <= 10 else "🟢 Planifié")
    )
    vacc_show["date_prevue"] = vacc_show["date_prevue"].dt.strftime("%d/%m/%Y")
    st.dataframe(
        vacc_show.rename(columns={
            "cheval_nom": "Cheval", "vaccin": "Vaccin", "date_prevue": "Date prévue",
            "veterinaire": "Vétérinaire assigné", "urgence": "Priorité",
        })[["Cheval", "Vaccin", "Date prévue", "Vétérinaire assigné", "Priorité"]],
        hide_index=True, use_container_width=True, height=420,
    )
    st.caption(
        "Chaque échéance déclenche automatiquement une notification vers le vétérinaire assigné "
        "et le propriétaire du cheval, avec la date et l'action requise."
    )

with tab2:
    st.subheader("Historique des consultations")
    c1, c2 = st.columns(2)
    motif_f = c1.multiselect("Filtrer par motif", sorted(vet_df["motif"].unique()))
    vet_f = c2.multiselect("Filtrer par vétérinaire", sorted(vet_df["veterinaire"].unique()))
    show = vet_df.copy()
    if motif_f:
        show = show[show["motif"].isin(motif_f)]
    if vet_f:
        show = show[show["veterinaire"].isin(vet_f)]
    show["date"] = pd.to_datetime(show["date"]).dt.strftime("%d/%m/%Y")
    st.dataframe(
        show.rename(columns={
            "cheval_nom": "Cheval", "date": "Date", "motif": "Motif",
            "veterinaire": "Vétérinaire", "notes": "Notes",
        })[["Cheval", "Date", "Motif", "Vétérinaire", "Notes"]],
        hide_index=True, use_container_width=True, height=420,
    )

with tab3:
    st.subheader("Ajouter une consultation (démo)")
    with st.form("new_vet_record"):
        horse = st.selectbox("Cheval", horses_df["id"] + " — " + horses_df["nom"])
        motif = st.selectbox("Motif", ["Vaccination", "Contrôle de routine", "Blessure", "Suivi post-course", "Dentisterie"])
        vet = st.selectbox("Vétérinaire", ["Dr. Alaoui", "Dr. Benkirane", "Dr. Idrissi", "Dr. Squalli"])
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Enregistrer")
        if submitted:
            st.success(f"Consultation enregistrée pour {horse} — une alerte de suivi sera envoyée si nécessaire.")
