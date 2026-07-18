import streamlit as st

st.set_page_config(page_title="EquiScan AI — Paramètres", page_icon="⚙️", layout="wide")

st.title("Paramètres — Gestion des accès par rôle")
st.caption("Chaque acteur dispose d'un espace dédié avec des droits différenciés")

roles = {
    "SOREC (vue globale)": [
        "Vue d'ensemble de toute la filière", "Analytics et rapports stratégiques",
        "Supervision de tous les haras", "Gestion des accès des autres acteurs",
    ],
    "Éleveur": [
        "Gestion de ses propres chevaux", "Suivi des saillies, gestations et naissances",
        "Consultation du pedigree et des performances",
    ],
    "Vétérinaire": [
        "Accès aux dossiers médicaux des chevaux suivis", "Ajout de consultations et de vaccinations",
        "Réception des alertes IoT (température, immobilité)",
    ],
    "Propriétaire": [
        "Consultation du passeport digital de son cheval", "Suivi des performances en compétition",
        "Réception des notifications vétérinaires",
    ],
    "Gestionnaire de haras": [
        "Gestion de l'occupation des boxes", "Suivi IoT du bien-être (température, eau, air)",
        "Planification des rotations et du personnel",
    ],
}

cols = st.columns(len(roles))
for col, (role, perms) in zip(cols, roles.items()):
    with col:
        st.markdown(f"**{role}**")
        for p in perms:
            st.markdown(f"- {p}")

st.divider()
st.subheader("Simuler une connexion")
role = st.selectbox("Se connecter en tant que", list(roles.keys()))
if st.button("Appliquer ce rôle"):
    st.success(f"Session simulée en tant que **{role}** — les modules affichés dans la sidebar seront adaptés à ce rôle en production.")

st.divider()
st.subheader("Notifications")
st.checkbox("Alertes vétérinaires (vaccination, consultation)", value=True)
st.checkbox("Alertes IoT (température, eau, air, immobilité)", value=True)
st.checkbox("Résultats de compétitions", value=False)
st.checkbox("Rapports analytics hebdomadaires", value=False)
