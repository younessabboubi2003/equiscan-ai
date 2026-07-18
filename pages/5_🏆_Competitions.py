import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data import generate_competitions, generate_horses

st.set_page_config(page_title="EquiScan AI — Compétitions", page_icon="🏆", layout="wide")


@st.cache_data
def load():
    horses = generate_horses(60)
    comps = generate_competitions(horses, n=100)
    return horses, comps


horses_df, comps_df = load()

st.title("Compétitions")
st.caption("Résultats, classements et historique de performance")

c1, c2 = st.columns(2)
comp_f = c1.multiselect("Compétition", sorted(comps_df["competition"].unique()))
horse_f = c2.multiselect("Cheval", sorted(comps_df["cheval_nom"].unique()))

show = comps_df.copy()
if comp_f:
    show = show[show["competition"].isin(comp_f)]
if horse_f:
    show = show[show["cheval_nom"].isin(horse_f)]

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Résultats")
    disp = show.copy()
    disp["date"] = pd.to_datetime(disp["date"]).dt.strftime("%d/%m/%Y")
    disp["podium"] = disp["podium"].map({True: "🏅 Podium", False: ""})
    st.dataframe(
        disp.rename(columns={
            "cheval_nom": "Cheval", "competition": "Compétition", "date": "Date",
            "classement": "Classement", "podium": "",
        })[["Cheval", "Compétition", "Date", "Classement", ""]],
        hide_index=True, use_container_width=True, height=440,
    )

with col2:
    st.subheader("Taux de podium par cheval")
    podium_rate = (
        comps_df.groupby("cheval_nom")["podium"].mean().sort_values(ascending=False).head(10) * 100
    ).round(1).reset_index()
    podium_rate.columns = ["Cheval", "Taux podium (%)"]
    fig = px.bar(podium_rate, x="Taux podium (%)", y="Cheval", orientation="h",
                 color="Taux podium (%)", color_continuous_scale=["#faeeda", "#854f0b"])
    fig.update_layout(height=440, showlegend=False, coloraxis_showscale=False,
                       margin=dict(l=0, r=0, t=10, b=0), yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)
