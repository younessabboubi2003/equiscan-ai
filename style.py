"""
EquiScan AI — thème visuel "Maison Équestre"
================================================
Palette et typographie partagées par toutes les pages du dashboard.
Importer et appeler `apply_theme()` en tête de chaque fichier de page
(pages/1_..., pages/2_..., etc.) pour garder une identité cohérente
dans toute l'application.

    from utils.style import apply_theme, PALETTE
    apply_theme()
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Jetons de design (design tokens)
# ---------------------------------------------------------------------------
PALETTE = {
    "forest": "#12251B",       # vert "sellerie" — fond sombre, sidebar, hero
    "forest_light": "#1E3A28", # vert dégradé, survols
    "ivory": "#FAF6EC",        # fond principal, couleur "papier"
    "card": "#FFFFFF",
    "gold": "#B08D3E",         # laiton / boucle de selle — accent signature
    "gold_light": "#D9C48B",
    "cognac": "#7C4A2D",       # cuir fauve — accent secondaire
    "text": "#1C261E",
    "text_muted": "#6E7A6C",
    "border": "#E3DAC3",
    "red": "#8C2F2F",
    "green": "#33613F",
    "amber": "#96692A",
}

# Séquences de couleurs pour les graphiques Plotly
PLOTLY_SEQUENTIAL = ["#D9C48B", "#B08D3E", "#8A6B2F", "#5F4A20"]
PLOTLY_CATEGORICAL = ["#12251B", "#7C4A2D", "#B08D3E", "#33613F", "#8C2F2F"]

FONT_DISPLAY = "'Fraunces', 'Georgia', serif"
FONT_BODY = "'Inter', -apple-system, sans-serif"


def plotly_layout_defaults() -> dict:
    """Réglages Plotly communs pour rester dans la charte graphique."""
    return dict(
        font=dict(family=FONT_BODY, color=PALETTE["text"], size=13),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font=dict(family=FONT_DISPLAY, size=16, color=PALETTE["forest"]),
    )


def apply_theme() -> None:
    """Injecte la feuille de style 'Maison Équestre' dans la page courante."""
    st.markdown(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,500;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

        <style>
        :root {{
            --forest: {PALETTE["forest"]};
            --forest-light: {PALETTE["forest_light"]};
            --ivory: {PALETTE["ivory"]};
            --card: {PALETTE["card"]};
            --gold: {PALETTE["gold"]};
            --gold-light: {PALETTE["gold_light"]};
            --cognac: {PALETTE["cognac"]};
            --text: {PALETTE["text"]};
            --text-muted: {PALETTE["text_muted"]};
            --border: {PALETTE["border"]};
        }}

        /* ---------- Fond général & typographie ---------- */
        .stApp {{
            background: var(--ivory);
            color: var(--text);
            font-family: {FONT_BODY};
        }}
        .block-container {{
            padding-top: 1.6rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }}
        h1, h2, h3, h4 {{
            font-family: {FONT_DISPLAY} !important;
            color: var(--forest) !important;
            font-weight: 600 !important;
            letter-spacing: 0.2px;
        }}
        h1 {{ font-weight: 500 !important; }}
        p, span, div, label {{ font-family: {FONT_BODY}; }}

        /* Eyebrow / libellé de section en petites capitales dorées */
        .eq-eyebrow {{
            font-family: {FONT_BODY};
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--gold);
            margin-bottom: 0.15rem;
        }}
        .eq-hero-title {{
            font-family: {FONT_DISPLAY};
            font-weight: 500;
            font-size: 2.3rem;
            color: var(--forest);
            margin: 0.1rem 0 0.3rem 0;
        }}
        .eq-hero-sub {{
            color: var(--text-muted);
            font-size: 0.95rem;
        }}
        .eq-divider {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, var(--gold) 0%, var(--border) 40%, transparent 100%);
            margin: 1.4rem 0;
        }}

        /* ---------- Barre latérale ---------- */
        [data-testid="stSidebar"] {{
            background: var(--forest);
        }}
        [data-testid="stSidebar"] * {{
            color: #EDE7D6 !important;
        }}
        [data-testid="stSidebar"] .eq-crest {{
            width: 46px; height: 46px; border-radius: 50%;
            border: 1px solid var(--gold);
            display: flex; align-items: center; justify-content: center;
            font-family: {FONT_DISPLAY}; color: var(--gold) !important;
            font-size: 1rem; letter-spacing: 0.05em; margin-bottom: 0.6rem;
        }}
        [data-testid="stSidebar"] hr {{ border-color: rgba(217,196,139,0.25); }}
        [data-testid="stSidebar"] label {{ color: #C9C2A9 !important; font-size: 0.8rem; }}
        [data-testid="stSidebar"] [data-baseweb="select"] > div {{
            background: var(--forest-light) !important;
            border-color: rgba(217,196,139,0.35) !important;
        }}

        /* ---------- Cartes / conteneurs à bordure ---------- */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: var(--card);
            border: 1px solid var(--border) !important;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(18,37,27,0.05);
        }}

        /* ---------- Métriques ---------- */
        [data-testid="stMetric"] {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.1rem 1.2rem 0.9rem 1.2rem;
            box-shadow: 0 1px 3px rgba(18,37,27,0.05);
        }}
        [data-testid="stMetricLabel"] {{
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--text-muted) !important;
        }}
        [data-testid="stMetricValue"] {{
            font-family: {FONT_DISPLAY} !important;
            font-size: 1.9rem !important;
            color: var(--forest) !important;
            font-weight: 500 !important;
        }}
        [data-testid="stMetricDelta"] svg {{ display: none; }}

        /* ---------- Tableaux ---------- */
        [data-testid="stDataFrame"] {{
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
        }}

        /* ---------- Badges de statut ---------- */
        .badge {{
            display:inline-block; padding: 2px 11px; border-radius: 20px;
            font-size: 0.72rem; font-weight: 600; letter-spacing: 0.02em;
        }}
        .badge-green {{ background:#E4EEE3; color: var(--green); }}
        .badge-amber {{ background:#F3E7D2; color: var(--amber); }}
        .badge-red {{ background:#F4E1E1; color: var(--red); }}

        /* ---------- Boutons ---------- */
        .stButton > button, .stDownloadButton > button {{
            background: var(--forest);
            color: #F4F0E2;
            border: 1px solid var(--forest);
            border-radius: 6px;
            font-family: {FONT_BODY};
            font-weight: 500;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            background: var(--gold);
            border-color: var(--gold);
            color: var(--forest);
        }}

        /* ---------- Caption / footer ---------- */
        [data-testid="stCaptionContainer"] {{ color: var(--text-muted); }}
        </style>
        """,
        unsafe_allow_html=True,
    )
