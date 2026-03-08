import streamlit as st
import pandas as pd
import json
import os

DB_FILE = "election_2029_results.json"

# Fonction pour charger les données proprement
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            # Si le fichier a l'ancienne structure (juste un dictionnaire de votes)
            if "Ousmane Sonko (PASTEF)" in data:
                return {
                    "votes": data,
                    "views": 0
                }
            return data
    return {
        "votes": {"Ousmane Sonko (PASTEF)": 0, "Bassirou Diomaye (Coalition Diomaye Président)": 0},
        "views": 0
    }

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

st.set_page_config(page_title="Sondage Sénégal 2029", layout="centered")

# Chargement des données
if 'db' not in st.session_state:
    st.session_state.db = load_data()

# Compteur de visites INVISIBLE
if 'tracked' not in st.session_state:
    st.session_state.db["views"] += 1
    save_data(st.session_state.db)
    st.session_state.tracked = True

# --- Style CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, 
            rgba(0, 128, 55, 0.08) 0%, 
            rgba(255, 239, 0, 0.08) 50%, 
            rgba(227, 27, 35, 0.08) 100%);
    }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px; background: white; border-top: 1px solid #ddd; z-index: 100; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇸🇳 Élections 2029 : Le Sondage")

# --- Affichage des Candidats ---
col_s, col_d = st.columns(2)
with col_s:
    if os.path.exists("sonko.png"): st.image("sonko.png")
    elif os.path.exists("sonko.jpg"): st.image("sonko.jpg")
    st.write("**PASTEF**")
with col_d:
    if os.path.exists("diomaye.png"): st.image("diomaye.png")
    elif os.path.exists("diomaye.jpg"): st.image("diomaye.jpg")
    st.write("**Coalition Diomaye Président**")

st.divider()

# --- Système de vote ---
if 'has_voted' not in st.session_state:
    st.session_state.has_voted = False

if not st.session_state.has_voted:
    # On n'affiche QUE les clés présentes dans "votes"
    choix = st.radio("Faites votre choix :", list(st.session_state.db["votes"].keys()))
    if st.button("Valider mon vote 🗳️"):
        st.session_state.db["votes"][choix] += 1
        save_data(st.session_state.db)
        st.session_state.has_voted = True
        st.balloons()
        st.rerun()
else:
    st.success("Merci ! Votre vote a été enregistré.")

# --- Résultats (Views supprimées de l'affichage) ---
st.subheader("📊 Résultats en direct")
df = pd.DataFrame(list(st.session_state.db["votes"].items()), columns=["Candidat", "Voix"])
total_votes = df["Voix"].sum()

if total_votes > 0:
    for index, row in df.iterrows():
        pct = (row["Voix"] / total_votes) * 100
        st.write(f"**{row['Candidat']}** : {int(pct)}% ({row['Voix']} voix)")
        st.progress(int(pct))
else:
    st.write("En attente des premiers votes...")

# Footer
st.markdown(f'<div class="footer">Créé par <b>Babacar Sarr dev front end</b></div>', unsafe_allow_html=True)
