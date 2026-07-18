import streamlit as st

from utils.data import generate_box_status

st.set_page_config(page_title="EquiScan AI — Gestion des haras", page_icon="🏠", layout="wide")


@st.cache_data
def load():
    return generate_box_status(40)


boxes_df = load()

st.title("Gestion des haras")
st.caption("Occupation des boxes, propreté et vue opérationnelle par site")

haras_f = st.selectbox("Haras", ["Tous"] + sorted(boxes_df["haras"].unique().tolist()))
show = boxes_df if haras_f == "Tous" else boxes_df[boxes_df["haras"] == haras_f]

c1, c2, c3 = st.columns(3)
c1.metric("Boxes occupés", int(show["occupe"].sum()))
c2.metric("Boxes libres", int((~show["occupe"]).sum()))
c3.metric("Nettoyage requis", int((show["proprete"] == "Nettoyage requis").sum()))

st.divider()
st.subheader("Plan des boxes")

cols = st.columns(8)
for i, (_, row) in enumerate(show.iterrows()):
    with cols[i % 8]:
        if not row["occupe"]:
            color = "#e1f5ee"
            icon = "⬜"
        elif row["proprete"] == "Nettoyage requis":
            color = "#fcebeb"
            icon = "🧹"
        elif row["proprete"] == "À vérifier":
            color = "#faeeda"
            icon = "🔶"
        else:
            color = "#e6f1fb"
            icon = "🐴"
        st.markdown(
            f"<div style='background:{color}; border-radius:8px; padding:10px; text-align:center; margin-bottom:8px;'>"
            f"<div style='font-size:1.3rem;'>{icon}</div>"
            f"<div style='font-size:0.75rem; font-weight:600;'>{row['box']}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

st.divider()
st.subheader("Détail par box")
st.dataframe(
    show.rename(columns={
        "box": "Box", "haras": "Haras", "occupe": "Occupé", "proprete": "Propreté",
        "temperature_ambiante": "Température (°C)", "qualite_air": "Qualité de l'air (indice)",
    }),
    hide_index=True, use_container_width=True, height=360,
)
