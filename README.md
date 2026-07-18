# EquiScan AI — Prototype Streamlit

Prototype fonctionnel de la plateforme **EquiScan AI**, préparé pour le hackathon
**Enactus Morocco × SOREC**. Toutes les données sont **simulées** à des fins de démonstration.

## Installation

```bash
pip install -r requirements.txt
```

## Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans le navigateur (`http://localhost:8501`).

## Structure du projet

```
equiscan_ai/
├── app.py                          # Dashboard principal
├── utils/
│   └── data.py                     # Génération des données simulées
├── pages/
│   ├── 1_🐴_Horses.py               # Gestion des chevaux
│   ├── 2_📄_Passeport_Digital.py    # Passeport digital (identité, historique, timeline)
│   ├── 3_🤖_Reconnaissance_IA.py    # Reconnaissance IA par photo
│   ├── 4_🩺_Veterinaire.py          # Module vétérinaire (alertes, historique)
│   ├── 5_🏆_Competitions.py         # Résultats et classements
│   ├── 6_🧬_Elevage.py              # Pedigree et aide au croisement
│   ├── 7_🏠_Gestion_Haras.py        # Occupation des boxes
│   ├── 8_📊_Analytics.py            # Tableaux de bord stratégiques
│   ├── 9_📡_Supervision_IoT.py      # Capteurs : température, eau, mouvement, air
│   └── 10_⚙️_Parametres.py          # Gestion des accès par rôle
└── requirements.txt
```

## Notes

- Les données (chevaux, consultations, compétitions, capteurs IoT) sont générées
  aléatoirement à chaque premier chargement puis mises en cache (`@st.cache_data`).
- La reconnaissance IA est simulée : elle retourne un cheval aléatoire de la base
  avec un score de confiance réaliste, pour illustrer le comportement attendu du produit final.
- Les seuils IoT (température, eau, mouvement, qualité de l'air) sont indicatifs et
  à calibrer avec un vétérinaire avant toute mise en production réelle.
