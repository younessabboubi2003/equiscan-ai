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
    COLORS,
    PLOTLY_CONTINUOUS,
    PLOTLY_SEQUENCE,
    badge,
    card_end,
    card_start,
    inject_css,
    page_header,
    render_kpi_grid,
    sidebar_brand,
)

st.set_page_config(
    page_title="EquiScan AI — Dashboard",
    page_icon="🐴",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()


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

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_brand()
    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    st.selectbox(
        "Rôle connecté",
        ["SOREC (vue globale)", "Éleveur", "Vétérinaire", "Propriétaire", "Gestionnaire de haras"],
    )
    st.selectbox("Haras", ["Tous les haras"] + sorted(horses_df["haras"].unique().tolist()))
    st.divider()
    st.caption("🇲🇦 Hackathon Enactus Morocco × SOREC")
    st.caption("Démo Streamlit — données simulées")

# ---------------------------------------------------------------------------
# Hero header
# ---------------------------------------------------------------------------
page_header(
    icon="📊",
    eyebrow="Tableau de bord — vue d'ensemble",
    title="Pilotage unifié de la filière équine",
    subtitle=(
        "Une vision consolidée du cheptel, de la santé et de l'occupation des infrastructures — "
        "en temps réel, pour l'ensemble des parties prenantes (SOREC, haras, vétérinaires, éleveurs)."
    ),
)

# ---------------------------------------------------------------------------
# KPI cards
# ---------------------------------------------------------------------------
render_kpi_grid([
    {"label": "Chevaux enregistrés", "value": kpis["total_chevaux"], "delta": "Base consolidée", "delta_direction": "flat"},
    {"label": "Chevaux actifs", "value": kpis["chevaux_actifs"],
     "delta": f"{round(100 * kpis['chevaux_actifs'] / kpis['total_chevaux'])}% du cheptel", "delta_direction": "up"},
    {"label": "Alertes vétérinaires", "value": kpis["alertes_vet"], "delta": "Suivi requis", "delta_direction": "down"},
    {"label": "Boxes disponibles", "value": f"{kpis['taux_boxes_libres']}%", "delta": "Occupation en temps réel", "delta_direction": "flat"},
])

# ---------------------------------------------------------------------------
# Row 2 — vaccinations + répartition par haras
# ---------------------------------------------------------------------------
col1, col2 = st.columns([1.3, 1])

with col1:
    card_start("Vaccinations à venir", "Prochaines échéances planifiées, tous haras confondus")
    show = vacc_df.copy()
    show["date_prevue"] = pd.to_datetime(show["date_prevue"]).dt.strftime("%d/%m/%Y")
    st.dataframe(
        show.rename(columns={
            "cheval_nom": "Cheval", "vaccin": "Vaccin",
            "date_prevue": "Date prévue", "veterinaire": "Vétérinaire",
        })[["Cheval", "Vaccin", "Date prévue", "Vétérinaire"]],
        hide_index=True, use_container_width=True, height=280,
    )
    card_end()

with col2:
    card_start("Répartition par haras", "Nombre de chevaux enregistrés par site")
    haras_counts = horses_df["haras"].value_counts().reset_index()
    haras_counts.columns = ["Haras", "Chevaux"]
    fig = px.bar(
        haras_counts, x="Chevaux", y="Haras", orientation="h", color="Chevaux",
        color_continuous_scale=PLOTLY_CONTINUOUS,
    )
    fig.update_layout(
        height=270, showlegend=False, coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=6, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color=COLORS["text"]),
        yaxis=dict(title=None), xaxis=dict(title=None, gridcolor="rgba(16,24,40,0.06)"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    card_end()

# ---------------------------------------------------------------------------
# Row 3 — statut du cheptel + activité récente
# ---------------------------------------------------------------------------
col3, col4 = st.columns([1, 1.3])

with col3:
    card_start("Statut du cheptel", "Répartition actuelle par état opérationnel")
    statut_counts = horses_df["statut"].value_counts().reset_index()
    statut_counts.columns = ["Statut", "Nombre"]
    fig2 = px.pie(
        statut_counts, names="Statut", values="Nombre", hole=0.6,
        color_discrete_sequence=PLOTLY_SEQUENCE,
    )
    fig2.update_layout(
        height=270, margin=dict(l=0, r=0, t=6, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color=COLORS["text"]),
        legend=dict(orientation="h", yanchor="bottom", y=-0.18),
    )
    fig2.update_traces(textinfo="percent", textfont_size=12)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    card_end()

with col4:
    card_start("Activité récente", "Dernières interventions vétérinaires enregistrées")
    recent = vet_df.head(5).copy()
    recent["date"] = pd.to_datetime(recent["date"]).dt.strftime("%d/%m/%Y")
    rows_html = ""
    for _, r in recent.iterrows():
        b = badge(r["notes"], "red" if r["notes"] == "Suivi requis" else "green")
        rows_html += f"""
        <div class="es-feed-row">
            <span class="es-feed-name">{r['cheval_nom']}</span>
            &nbsp;— {r['motif']} · {r['veterinaire']} &nbsp;{b}
            <div class="es-feed-meta">{r['date']}</div>
        </div>
        """
    st.markdown(rows_html, unsafe_allow_html=True)
    card_end()

# ---------------------------------------------------------------------------
# Footer / navigation
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div style="text-align:center;color:{COLORS['muted']};font-size:0.82rem;padding-top:0.6rem;">
        Navigation — utilisez le menu latéral pour accéder aux modules : Chevaux, Passeport digital,
        Reconnaissance IA, Vétérinaire, Compétitions, Élevage, Gestion des haras, Analytics,
        Supervision IoT et Paramètres.
    </div>
    """,
    unsafe_allow_html=True,
)
