import random
import time

import streamlit as st

from utils.data import generate_horses

st.set_page_config(page_title="EquiScan AI — Reconnaissance IA", page_icon="🤖", layout="centered")


@st.cache_data
def load():
    return generate_horses(60)


horses_df = load()

st.title("Reconnaissance IA")
st.caption("Identifiez un cheval automatiquement à partir d'une simple photo")

st.markdown(
    """
    <div style="border: 2px dashed #ccc; border-radius: 12px; padding: 40px; text-align:center; background:#fafbfc;">
        <p style="font-size:1.1rem; margin-bottom:0;">📷 Prenez ou importez une photo du cheval</p>
        <p style="color:#888; font-size:0.85rem;">Formats acceptés : JPG, PNG</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
photo = st.camera_input("Prendre une photo") or st.file_uploader("...ou importer une image", type=["jpg", "jpeg", "png"])

if photo:
    st.image(photo, caption="Photo capturée", use_container_width=True)

    with st.spinner("Analyse en cours par le modèle de reconnaissance..."):
        time.sleep(1.4)

    match = horses_df.sample(1, random_state=random.randint(0, 9999)).iloc[0]
    confidence = round(random.uniform(97.5, 99.9), 1)

    st.success(f"✓ Match {confidence}% — Cheval identifié")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.image("https://placehold.co/300x300?text=" + match["nom"], use_container_width=True)
    with c2:
        st.markdown(f"### {match['nom']}")
        st.markdown(f"**ID :** {match['id']}")
        st.markdown(f"**Race :** {match['race']}  ·  **Âge :** {match['age']} ans")
        st.markdown(f"**Haras :** {match['haras']}  ·  **Box :** {match['box']}")
        st.markdown(f"**Statut :** {match['statut']}")
        st.page_link("pages/2_📄_Passeport_Digital.py", label="Ouvrir le passeport digital →", icon="📄")
else:
    st.info("En attente d'une photo — utilisez l'appareil photo ou importez un fichier ci-dessus.")

st.divider()
st.caption(
    "Démo — dans cette version simulée, le modèle sélectionne un cheval aléatoire de la base pour illustrer "
    "le comportement attendu. En production, la reconnaissance s'appuie sur un modèle de vision entraîné "
    "sur les traits morphologiques distinctifs de chaque cheval."
)
