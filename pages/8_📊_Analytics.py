import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data import generate_competitions, generate_horses, generate_vet_records

st.set_page_config(page_title="EquiScan AI — Analytics", page_icon="📊", layout="wide")


@st.cache_data
def load():
    horses = generate_horses(60)
    vet = generate_vet_records(horses, n=150)
    comps = generate_competitions(horses, n=100)
    return horses, vet, comps


horses_df, vet_df, comps_df = load()

st.title("Analytics")
st.caption("Pilotage stratégique — indicateurs agrégés pour la SOREC et les décideurs de la filière")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Taux de réussite sportive (podiums)", f"{round(100*comps_df['podium'].mean(),1)}%")
col2.metric("Consultations vétérinaires / mois (moy.)", round(len(vet_df) / 6, 1))
col3.metric("Âge moyen du cheptel", f"{round(horses_df['age'].mean(),1)} ans")
col4.metric("Coût vétérinaire estimé / cheval / an", "4 200 DH")

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.subheader("Consultations vétérinaires par motif")
    motif_counts = vet_df["motif"].value_counts().reset_index()
    motif_counts.columns = ["Motif", "Nombre"]
    fig = px.bar(motif_counts, x="Motif", y="Nombre", color="Motif",
                 color_discrete_sequence=["#0c447c", "#1d9e75", "#ef9f27", "#e24b4a", "#534ab7"])
    fig.update_layout(height=340, showlegend=False, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Coûts vétérinaires estimés par haras (DH, simulé)")
    costs = horses_df.groupby("haras").size().reset_index(name="chevaux")
    costs["cout_estime"] = costs["chevaux"] * np.random.randint(3500, 5000, len(costs))
    fig2 = px.bar(costs, x="haras", y="cout_estime", color="haras",
                  color_discrete_sequence=["#0c447c", "#1d9e75", "#ef9f27", "#e24b4a", "#534ab7"])
    fig2.update_layout(height=340, showlegend=False, margin=dict(l=0, r=0, t=10, b=0),
                        xaxis_title="Haras", yaxis_title="Coût estimé (DH)")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.subheader("Évolution du nombre de compétitions (12 derniers mois, simulé)")
months = pd.date_range(end=pd.Timestamp.now(), periods=12, freq="M").strftime("%b %Y")
trend = pd.DataFrame({"Mois": months, "Compétitions": np.random.randint(4, 15, 12)})
fig3 = px.line(trend, x="Mois", y="Compétitions", markers=True)
fig3.update_traces(line_color="#0c447c")
fig3.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig3, use_container_width=True)

st.caption("Toutes les données affichées sur cette page sont simulées à des fins de démonstration du hackathon.")
