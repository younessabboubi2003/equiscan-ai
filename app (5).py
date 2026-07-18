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
from utils.style import (
    PALETTE,
    PLOTLY_CATEGORICAL,
    PLOTLY_SEQUENTIAL,
    apply_theme,
    plotly_layout_defaults,
)

st.set_page_config(
    page_title="EquiScan AI — Domaine",
    page_icon="🐴",
    layout="wide",
)

apply_theme()


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
    st.markdown('<div class="eq-crest">EQ</div>', unsafe_allow_html=True)
    st.markdown("### EquiScan AI")
    st.caption("Gestion du cycle de vie du cheval, à la manière d'une maison")
    st.divider()
    st.selectbox(
        "Rôle connecté",
        ["SOREC (vue globale)", "Éleveur", "Vétérinaire", "Propriétaire", "Gestionnaire de haras"],
    )
    st.selectbox("Haras", ["Tous les haras"] + sorted(horses_df["haras"].unique().tolist()))
    st.divider()
    st.caption("Hackathon Enactus Morocco × SOREC — démonstration Streamlit")

# ---------- Header / hero ----------
st.markdown('<div class="eq-eyebrow">Domaine · Vue d\'ensemble</div>', unsafe_allow_html=True)
st.markdown('<p class="eq-hero-title">Le cheptel, d\'un seul regard</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="eq-hero-sub">Toutes les données présentées ici sont simulées, '
    'à des fins de démonstration.</p>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="eq-divider">', unsafe_allow_html=True)

# ---------- KPI cards ----------
c1, c2, c3, c4 = st.columns(4)
with c1, st.container(border=True):
    st.metric("Chevaux enregistrés", kpis["total_chevaux"])
with c2, st.container(border=True):
    st.metric("Chevaux actifs", kpis["chevaux_actifs"])
with c3, st.container(border=True):
    st.metric("Alertes vétérinaires", kpis["alertes_vet"], delta_color="inverse")
with c4, st.container(border=True):
    st.metric("Boxes disponibles", f"{kpis['taux_boxes_libres']}%")

st.write("")

# ---------- Row 2: vaccinations + répartition ----------
col1, col2 = st.columns([1.3, 1])

with col1:
    with st.container(border=True):
        st.markdown('<div class="eq-eyebrow">Suivi sanitaire</div>', unsafe_allow_html=True)
        st.markdown("#### Vaccinations à venir")
        show = vacc_df.copy()
        show["date_prevue"] = pd.to_datetime(show["date_prevue"]).dt.strftime("%d/%m/%Y")
        st.dataframe(
            show.rename(columns={
                "cheval_nom": "Cheval", "vaccin": "Vaccin",
                "date_prevue": "Date prévue", "veterinaire": "Vétérinaire",
            })[["Cheval", "Vaccin", "Date prévue", "Vétérinaire"]],
            hide_index=True, use_container_width=True, height=260,
        )

with col2:
    with st.container(border=True):
        st.markdown('<div class="eq-eyebrow">Patrimoine</div>', unsafe_allow_html=True)
        st.markdown("#### Répartition par haras")
        haras_counts = horses_df["haras"].value_counts().reset_index()
        haras_counts.columns = ["Haras", "Chevaux"]
        fig = px.bar(
            haras_counts, x="Chevaux", y="Haras", orientation="h", color="Chevaux",
            color_continuous_scale=PLOTLY_SEQUENTIAL,
        )
        fig.update_layout(
            **plotly_layout_defaults(),
            height=260, showlegend=False, coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

st.write("")

# ---------- Row 3: statut + activité récente ----------
col3, col4 = st.columns([1, 1.3])

with col3:
    with st.container(border=True):
        st.markdown('<div class="eq-eyebrow">Cheptel</div>', unsafe_allow_html=True)
        st.markdown("#### Statut du cheptel")
        statut_counts = horses_df["statut"].value_counts().reset_index()
        statut_counts.columns = ["Statut", "Nombre"]
        fig2 = px.pie(
            statut_counts, names="Statut", values="Nombre", hole=0.6,
            color_discrete_sequence=PLOTLY_CATEGORICAL,
        )
        fig2.update_layout(
            **plotly_layout_defaults(),
            height=260, margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15),
        )
        fig2.update_traces(marker=dict(line=dict(color=PALETTE["ivory"], width=2)))
        st.plotly_chart(fig2, use_container_width=True)

with col4:
    with st.container(border=True):
        st.markdown('<div class="eq-eyebrow">Journal</div>', unsafe_allow_html=True)
        st.markdown("#### Activité récente")
        recent = vet_df.head(5).copy()
        recent["date"] = pd.to_datetime(recent["date"]).dt.strftime("%d/%m/%Y")
        for _, r in recent.iterrows():
            badge = "badge-red" if r["notes"] == "Suivi requis" else "badge-green"
            st.markdown(
                f"**{r['cheval_nom']}** — {r['motif']} · {r['veterinaire']} "
                f"<span class='badge {badge}'>{r['notes']}</span> "
                f"<span style='color:#8A8A80;font-size:0.8rem;'>· {r['date']}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div style='border-bottom:1px solid #EFE9D9;margin:0.5rem 0;'></div>",
                unsafe_allow_html=True,
            )

st.markdown('<hr class="eq-divider">', unsafe_allow_html=True)
st.caption(
    "Navigation : utilisez le menu latéral pour accéder aux modules — Horses, Passeport digital, "
    "Reconnaissance IA, Vétérinaire, Compétitions, Élevage, Gestion des haras, Analytics, "
    "Supervision IoT et Paramètres."
)
