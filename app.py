import streamlit as st
import pandas as pd
import json
import os

DB_FILE = "election_2029_results.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"Ousmane Sonko (PASTEF)": 0, "Bassirou Diomaye (Coalition Diomaye Président)": 0}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

st.set_page_config(page_title="Sondage Sénégal 2029", layout="centered")

# CSS pour le background Drapeau Sénégal et le style
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, 
            rgba(0, 128, 55, 0.1) 0%, 
            rgba(255, 239, 0, 0.1) 50%, 
            rgba(227, 27, 35, 0.1) 100%);
    }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px; background: white; border-top: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

if 'votes' not in st.session_state:
    st.session_state.votes = load_data()

st.title("🇸🇳 Élections 2029 : Le Sondage")

# --- Affichage des Candidats avec Photos ---
col_s, col_d = st.columns(2)

with col_s:
    # Remplace par le nom exact de ton fichier image sur GitHub
    if os.path.exists("sonko.jpg"):
        st.image("sonko.jpg", caption="Ousmane Sonko")
    else:
        st.info("Photo Sonko")
    st.write("**PASTEF**")

with col_d:
    if os.path.exists("diomaye.jpg"):
        st.image("diomaye.jpg", caption="Bassirou Diomaye Faye")
    else:
        st.info("Photo Diomaye")
    st.write("**Coalition Diomaye Président**")

st.divider()

# Système de vote
if 'has_voted' not in st.session_state:
    st.session_state.has_voted = False

if not st.session_state.has_voted:
    choix = st.radio("Faites votre choix :", list(st.session_state.votes.keys()))
    if st.button("Valider mon vote 🗳️"):
        st.session_state.votes[choix] += 1
        save_data(st.session_state.votes)
        st.session_state.has_voted = True
        st.balloons()
        st.rerun()
else:
    st.success("Merci ! Votre vote a été enregistré.")

# Résultats
st.subheader("Résultats en direct")
df = pd.DataFrame(list(st.session_state.votes.items()), columns=["Candidat", "Voix"])
total = df["Voix"].sum()

if total > 0:
    for index, row in df.iterrows():
        pct = (row["Voix"] / total) * 100
        color = "#008037" if "Sonko" in row["Candidat"] else "#e31b23"
        st.write(f"**{row['Candidat']}** : {int(pct)}%")
        st.progress(int(pct))
else:
    st.write("Aucun vote pour le moment.")

# Footer
st.markdown(f'<div class="footer">Créé par <b>Babacar Sarr dev front end</b></div>', unsafe_allow_html=True)
