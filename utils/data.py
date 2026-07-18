"""Génération de données simulées pour la démo EquiScan AI (hackathon Enactus x SOREC)."""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

HARAS = ["El Jadida", "Bouznika", "Oujda", "Marrakech", "Meknès"]
RACES = ["Pur-sang arabe", "Barbe", "Anglo-arabe", "Selle français"]
NOMS = [
    "Sultan", "Ayida", "Kahil", "Nassim", "Amira", "Zayd", "Layla", "Rayan",
    "Yasmine", "Karim", "Nadia", "Hicham", "Salma", "Othman", "Malika",
    "Idriss", "Fatine", "Anas", "Widad", "Reda",
]
PROPRIETAIRES = ["Écurie Al Fadila", "Haras Bel Air", "M. Bennani", "Mme Toumi", "Écurie Chellah", "M. El Amrani"]
ELEVEURS = ["Élevage Sahraoui", "Élevage Ziani", "Élevage Bouzid", "Élevage Cavalia", "Élevage Al Andalous"]
STATUTS = ["Actif", "En repos", "À l'entraînement", "En soins"]
VET_MOTIFS = ["Vaccination", "Contrôle de routine", "Blessure", "Suivi post-course", "Dentisterie"]
COMPETITIONS = ["Grand Prix de Rabat", "Coupe SOREC", "Derby de Casablanca", "Prix du Roi", "Meeting de Marrakech"]


def _rand_date(days_back=0, days_forward=0):
    return datetime.now() + timedelta(days=random.randint(-days_back, days_forward))


def generate_horses(n=60):
    rows = []
    for i in range(1, n + 1):
        rows.append({
            "id": f"EQ-{1000 + i}",
            "nom": random.choice(NOMS) + (f" {i}" if random.random() < 0.3 else ""),
            "race": random.choice(RACES),
            "sexe": random.choice(["Mâle", "Femelle", "Hongre"]),
            "age": random.randint(2, 18),
            "statut": random.choices(STATUTS, weights=[50, 15, 25, 10])[0],
            "proprietaire": random.choice(PROPRIETAIRES),
            "eleveur": random.choice(ELEVEURS),
            "haras": random.choice(HARAS),
            "box": f"{random.choice(['A','B','C','D'])}-{random.randint(1,40)}",
            "rfid": f"MA{random.randint(100000000,999999999)}",
            "qr": f"QR-{1000+i}-{random.randint(1000,9999)}",
            "date_naissance": (datetime.now() - timedelta(days=365 * random.randint(2, 18))).strftime("%d/%m/%Y"),
        })
    return pd.DataFrame(rows)


def generate_vet_records(horses_df, n=120):
    rows = []
    for _ in range(n):
        h = horses_df.sample(1).iloc[0]
        rows.append({
            "cheval_id": h["id"],
            "cheval_nom": h["nom"],
            "date": _rand_date(days_back=200, days_forward=0),
            "motif": random.choice(VET_MOTIFS),
            "veterinaire": random.choice(["Dr. Alaoui", "Dr. Benkirane", "Dr. Idrissi", "Dr. Squalli"]),
            "notes": "RAS" if random.random() > 0.2 else "Suivi requis",
        })
    return pd.DataFrame(rows).sort_values("date", ascending=False)


def generate_upcoming_vaccinations(horses_df, n=15):
    rows = []
    for _ in range(n):
        h = horses_df.sample(1).iloc[0]
        rows.append({
            "cheval_id": h["id"],
            "cheval_nom": h["nom"],
            "vaccin": random.choice(["Grippe équine", "Tétanos", "Rhinopneumonie", "Rage"]),
            "date_prevue": _rand_date(days_back=0, days_forward=30),
            "veterinaire": random.choice(["Dr. Alaoui", "Dr. Benkirane", "Dr. Idrissi", "Dr. Squalli"]),
        })
    df = pd.DataFrame(rows).sort_values("date_prevue")
    return df


def generate_competitions(horses_df, n=80):
    rows = []
    for _ in range(n):
        h = horses_df.sample(1).iloc[0]
        place = random.randint(1, 12)
        rows.append({
            "cheval_id": h["id"],
            "cheval_nom": h["nom"],
            "competition": random.choice(COMPETITIONS),
            "date": _rand_date(days_back=365, days_forward=0),
            "classement": place,
            "podium": place <= 3,
        })
    return pd.DataFrame(rows).sort_values("date", ascending=False)


def generate_iot_readings(horses_df, hours=24):
    """Séries temporelles simulées de capteurs pour un sous-ensemble de chevaux."""
    sample = horses_df.sample(min(8, len(horses_df)), random_state=1)
    now = datetime.now()
    rows = []
    for _, h in sample.iterrows():
        base_temp = 37.8 + random.uniform(-0.3, 0.3)
        for hidx in range(hours):
            t = now - timedelta(hours=hours - hidx)
            rows.append({
                "cheval_id": h["id"],
                "cheval_nom": h["nom"],
                "box": h["box"],
                "timestamp": t,
                "temperature_c": round(base_temp + np.sin(hidx / 3) * 0.4 + random.uniform(-0.15, 0.15), 2),
                "mouvement_score": max(0, round(50 + np.sin(hidx / 2) * 35 + random.uniform(-10, 10), 1)),
                "niveau_eau_pct": max(0, min(100, round(90 - hidx * random.uniform(0.3, 1.4), 1))),
                "qualite_air_index": round(random.uniform(60, 98), 1),
            })
    return pd.DataFrame(rows)


def generate_box_status(n=40):
    rows = []
    for i in range(1, n + 1):
        occ = random.random() < 0.85
        rows.append({
            "box": f"{random.choice(['A','B','C','D'])}-{i}",
            "haras": random.choice(HARAS),
            "occupe": occ,
            "proprete": random.choices(["Bonne", "À vérifier", "Nettoyage requis"], weights=[70, 20, 10])[0],
            "temperature_ambiante": round(random.uniform(18, 27), 1),
            "qualite_air": round(random.uniform(55, 98), 1),
        })
    return pd.DataFrame(rows)


def kpi_summary(horses_df, vet_df, box_df):
    return {
        "total_chevaux": len(horses_df),
        "chevaux_actifs": int((horses_df["statut"] == "Actif").sum() + (horses_df["statut"] == "À l'entraînement").sum()),
        "alertes_vet": int((vet_df["notes"] == "Suivi requis").sum()),
        "taux_boxes_libres": round(100 * (~box_df["occupe"]).mean(), 1),
    }
