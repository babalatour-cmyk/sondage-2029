import streamlit as st
import pandas as pd
import json
import os

DB_FILE = "election_2029_results.json"

# Fonction pour charger les données (Votes + Vues)
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            # S'assurer que les clés de vues existent pour les anciens fichiers
            if "views" not in data:
                data["views"] = 0
            return data
    return {
        "votes": {"Ousmane Sonko (PASTEF)": 0, "Bassirou Diomaye (Coalition Diomaye Président)": 0},
        "views": 0
    }

# Fonction pour sauvegarder
def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# Fonction pour compter une visite
def track_visit():
    if 'tracked' not in st.session_state:
        st.session_state.data["views"] += 1
        save_data(st.session_state.data)
        st.session_state.tracked = True

st.set_page_config(page_title="Sondage Sénégal 2029", layout="centered")

# Chargement des données au démarrage
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# On compte la visite
track_visit()

# --- Design CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, rgba(0, 128, 55, 0.05), rgba(255, 239, 0, 0.05), rgba(227, 27, 35, 0.05)); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px; background: white; border-top: 1px solid #ddd; z-index: 100; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇸🇳 Élections 2029 : Le Sondage")

# --- Affichage Candidats ---
col_s, col_d = st.columns(2)
with col_s:
    if os.path.exists("sonko.png"): st.image("sonko.png")
    st.write("**PASTEF**")
with col_d:
    if os.path.exists("diomaye.png"): st.image("diomaye.png")
    st.write("**Coalition Diomaye Président**")

st.divider()

# --- Système de Vote ---
if 'has_voted' not in st.session_state:
    st.session_state.has_voted = False

if not st.session_state.has_voted:
    choix = st.radio("Faites votre choix :", list(st.session_state.data["votes"].keys()))
    if st.button("Valider mon vote 🗳️"):
        st.session_state.data["votes"][choix] += 1
        save_data(st.session_state.data)
        st.session_state.has_voted = True
        st.balloons()
        st.rerun()
else:
    st.success("✅ Vote enregistré !")

# --- Résultats et Statistiques ---
st.subheader("📊 Statistiques en direct")
df = pd.DataFrame(list(st.session_state.data["votes"].items()), columns=["Candidat", "Voix"])
total_votes = df["Voix"].sum()

# Affichage des barres
for index, row in df.iterrows():
    pct = (row["Voix"] / total_votes * 100) if total_votes > 0 else 0
    st.write(f"**{row['Candidat']}** : {int(pct)}% ({row['Voix']} voix)")
    st.progress(int(pct))

st.write(f"---")
# ICI TU VOIS LE NOMBRE DE PERSONNES QUI ONT OUVERT LE LIEN
st.metric(label="Nombre total de visites sur le lien", value=st.session_state.data["views"])

# Footer
st.markdown('<div class="footer">Créé par <b>Babacar Sarr dev front end</b></div>', unsafe_allow_html=True)
