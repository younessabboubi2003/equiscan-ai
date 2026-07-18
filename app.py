import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data import (
    generate_box_status,
    generate_competitions,
    generate_horses,
    generate_upcoming_vaccinations,
    generate_vet_records,
    kpi_summary,
)

st.set_page_config(
    page_title="EquiScan AI — Dashboard",
    page_icon="🐴",
    layout="wide",
)

# ---------- Style ----------
st.markdown("""
<style>
    [data-testid="stMetricValue"] { font-size: 1.7rem; }
    .block-container { padding-top: 2rem; }
    .badge {
        display:inline-block; padding: 2px 10px; border-radius: 12px;
        font-size: 0.75rem; font-weight: 600;
    }
    .badge-green { background:#e1f5ee; color:#0f6e56; }
    .badge-amber { background:#faeeda; color:#854f0b; }
    .badge-red { background:#fcebeb; color:#a32d2d; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    horses = generate_horses(60)
    vet = generate_vet_records(horses)
    comps = generate_competitions(horses)
    boxes = generate_box_status(40)
    vacc = generate_upcoming_vaccinations(horses)
    return horses, vet, comps, boxes, vacc


horses_df, vet_df, comps_df, boxes_df, vacc_df = load_data()
kpis = kpi_summary(horses_df, vet_df, boxes_df)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### 🐴 EquiScan AI")
    st.caption("Plateforme intelligente de gestion du cycle de vie du cheval")
    st.divider()
    st.selectbox("Rôle connecté", ["SOREC (vue globale)", "Éleveur", "Vétérinaire", "Propriétaire", "Gestionnaire de haras"])
    st.selectbox("Haras", ["Tous les haras"] + sorted(horses_df["haras"].unique().tolist()))
    st.divider()
    st.caption("Hackathon Enactus Morocco × SOREC — démo Streamlit")

# ---------- Header ----------
st.title("Vue d'ensemble")
st.caption("Tableau de bord global — toutes les données sont simulées à des fins de démonstration")

# ---------- KPI cards ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Chevaux enregistrés", kpis["total_chevaux"])
c2.metric("Chevaux actifs", kpis["chevaux_actifs"])
c3.metric("Alertes vétérinaires", kpis["alertes_vet"], delta_color="inverse")
c4.metric("Boxes disponibles", f"{kpis['taux_boxes_libres']}%")

st.write("")

# ---------- Row 2: vaccinations + map ----------
col1, col2 = st.columns([1.3, 1])

with col1:
    st.subheader("Vaccinations à venir")
    show = vacc_df.copy()
    show["date_prevue"] = pd.to_datetime(show["date_prevue"]).dt.strftime("%d/%m/%Y")
    st.dataframe(
        show.rename(columns={
            "cheval_nom": "Cheval", "vaccin": "Vaccin",
            "date_prevue": "Date prévue", "veterinaire": "Vétérinaire",
        })[["Cheval", "Vaccin", "Date prévue", "Vétérinaire"]],
        hide_index=True, use_container_width=True, height=280,
    )

with col2:
    st.subheader("Répartition par haras")
    haras_counts = horses_df["haras"].value_counts().reset_index()
    haras_counts.columns = ["Haras", "Chevaux"]
    fig = px.bar(haras_counts, x="Chevaux", y="Haras", orientation="h", color="Chevaux",
                 color_continuous_scale=["#c0dd97", "#3b6d11"])
    fig.update_layout(height=280, showlegend=False, coloraxis_showscale=False,
                       margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

st.write("")

# ---------- Row 3: statut + activité récente ----------
col3, col4 = st.columns([1, 1.3])

with col3:
    st.subheader("Statut du cheptel")
    statut_counts = horses_df["statut"].value_counts().reset_index()
    statut_counts.columns = ["Statut", "Nombre"]
    fig2 = px.pie(statut_counts, names="Statut", values="Nombre", hole=0.55,
                  color_discrete_sequence=["#0c447c", "#1d9e75", "#ef9f27", "#e24b4a"])
    fig2.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig2, use_container_width=True)

with col4:
    st.subheader("Activité récente")
    recent = vet_df.head(5).copy()
    recent["date"] = pd.to_datetime(recent["date"]).dt.strftime("%d/%m/%Y")
    for _, r in recent.iterrows():
        badge = "badge-red" if r["notes"] == "Suivi requis" else "badge-green"
        st.markdown(
            f"**{r['cheval_nom']}** — {r['motif']} · {r['veterinaire']} "
            f"<span class='badge {badge}'>{r['notes']}</span> "
            f"<span style='color:#888;font-size:0.8rem;'>· {r['date']}</span>",
            unsafe_allow_html=True,
        )

st.divider()
st.caption(
    "Navigation : utilisez le menu latéral pour accéder aux modules — Horses, Passeport digital, "
    "Reconnaissance IA, Vétérinaire, Compétitions, Élevage, Gestion des haras, Analytics, "
    "Supervision IoT et Paramètres."
)
