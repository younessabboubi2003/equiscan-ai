import plotly.express as px
import streamlit as st

from utils.data import generate_box_status, generate_horses, generate_iot_readings

st.set_page_config(page_title="EquiScan AI — Supervision IoT", page_icon="📡", layout="wide")


@st.cache_data
def load():
    horses = generate_horses(60)
    iot = generate_iot_readings(horses, hours=24)
    boxes = generate_box_status(40)
    return horses, iot, boxes


horses_df, iot_df, boxes_df = load()

st.title("Supervision IoT — Bien-être & environnement")
st.caption(
    "Capteurs connectés en box : température corporelle, mouvement, niveau d'eau, "
    "état du box et qualité de l'air, avec alertes automatiques en cas d'anomalie"
)

# ---------- Alertes ----------
st.subheader("Alertes actives")
latest = iot_df.sort_values("timestamp").groupby("cheval_id").tail(1)
alerts = []
for _, r in latest.iterrows():
    if r["temperature_c"] > 38.5 or r["temperature_c"] < 37.2:
        alerts.append((r["cheval_nom"], r["box"], "🌡️ Température anormale", f"{r['temperature_c']} °C"))
    if r["niveau_eau_pct"] < 25:
        alerts.append((r["cheval_nom"], r["box"], "💧 Niveau d'eau bas", f"{r['niveau_eau_pct']}%"))
    if r["mouvement_score"] < 15:
        alerts.append((r["cheval_nom"], r["box"], "🚨 Immobilité prolongée", f"score {r['mouvement_score']}"))
    if r["qualite_air_index"] < 65:
        alerts.append((r["cheval_nom"], r["box"], "🌫️ Qualité de l'air dégradée", f"indice {r['qualite_air_index']}"))

if alerts:
    for cheval, box, label, val in alerts:
        st.warning(f"**{cheval}** (box {box}) — {label} : {val} → notification envoyée au vétérinaire / gestionnaire de haras")
else:
    st.success("Aucune anomalie détectée — tous les indicateurs sont dans les seuils normaux.")

st.divider()

# ---------- Sélection cheval ----------
selected = st.selectbox("Suivre un cheval", sorted(iot_df["cheval_nom"].unique()))
h_iot = iot_df[iot_df["cheval_nom"] == selected].sort_values("timestamp")

c1, c2, c3, c4 = st.columns(4)
last = h_iot.iloc[-1]
c1.metric("Température corporelle", f"{last['temperature_c']} °C")
c2.metric("Score de mouvement", f"{last['mouvement_score']}")
c3.metric("Niveau d'eau (abreuvoir)", f"{last['niveau_eau_pct']}%")
c4.metric("Qualité de l'air (box)", f"{last['qualite_air_index']}")

col1, col2 = st.columns(2)
with col1:
    fig = px.line(h_iot, x="timestamp", y="temperature_c", title="Température corporelle (24h)")
    fig.add_hline(y=38.5, line_dash="dash", line_color="#e24b4a")
    fig.add_hline(y=37.2, line_dash="dash", line_color="#e24b4a")
    fig.update_traces(line_color="#0c447c")
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)

    fig3 = px.line(h_iot, x="timestamp", y="niveau_eau_pct", title="Niveau d'eau — abreuvoir (24h)")
    fig3.update_traces(line_color="#1d9e75")
    fig3.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    fig2 = px.area(h_iot, x="timestamp", y="mouvement_score", title="Activité / mouvement (24h)")
    fig2.update_traces(line_color="#ef9f27", fillcolor="rgba(239,159,39,0.2)")
    fig2.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig2, use_container_width=True)

    fig4 = px.line(h_iot, x="timestamp", y="qualite_air_index", title="Qualité de l'air — box (24h)")
    fig4.update_traces(line_color="#534ab7")
    fig4.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig4, use_container_width=True)

st.caption(
    "Les seuils affichés (température 37,2–38,5 °C, niveau d'eau < 25%, mouvement < 15, "
    "qualité de l'air < 65) sont des valeurs indicatives pour la démo — à calibrer avec un "
    "vétérinaire avant mise en production."
)
