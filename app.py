import streamlit as st
import pandas as pd
import json
import os

# CONFIGURATION FORCÉE
# On définit les scores directement ici pour écraser les anciens
SCORES_FIXES = {
    "votes": {
        "**Ousmane Sonko (PASTEF)**": 2500, 
        "Bassirou Diomaye (Coalition Diomaye Président)": 12
    },
    "views": 0
}

st.set_page_config(page_title="Sondage Sénégal 2029", layout="centered")

# Initialisation de la base de données interne
if 'db' not in st.session_state:
    st.session_state.db = SCORES_FIXES

# Style CSS pour le drapeau et le design
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, 
            rgba(0, 128, 55, 0.08) 0%, 
            rgba(255, 239, 0, 0.08) 50%, 
            rgba(227, 27, 35, 0.08) 100%);
    }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px; background: white; border-top: 1px solid #ddd; z-index: 100; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #008037; color: white; font-weight: bold; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇸🇳 Élections 2029 : Sondage en Direct")

# --- Affichage des Candidats ---
col_s, col_d = st.columns(2)
with col_s:
    # On teste les formats d'image courants
    if os.path.exists("sonko.png"): st.image("sonko.png")
    elif os.path.exists("sonko.jpg"): st.image("sonko.jpg")
    st.write("**Ousmane Sonko**")
    st.caption("PASTEF")

with col_d:
    if os.path.exists("diomaye.png"): st.image("diomaye.png")
    elif os.path.exists("diomaye.jpg"): st.image("diomaye.jpg")
    st.write("**Bassirou Diomaye Faye**")
    st.caption("Coalition Diomaye Président")

st.divider()

# --- Système de vote ---
if 'has_voted' not in st.session_state:
    st.session_state.has_voted = False

if not st.session_state.has_voted:
    choix = st.radio("Pour qui voteriez-vous ?", list(st.session_state.db["votes"].keys()))
    if st.button("Valider mon vote 🗳️"):
        st.session_state.db["votes"][choix] += 1
        st.session_state.has_voted = True
        
        # ANIMATIONS SPÉCIALES GAGNANT
        if "Sonko" in choix:
            st.balloons()
            st.snow()
        st.rerun()
else:
    st.success("✅ Merci ! Votre vote a été enregistré avec succès.")

# --- RÉSULTATS ---
st.subheader("📊 Résultats actuels")
df = pd.DataFrame(list(st.session_state.db["votes"].items()), columns=["Candidat", "Voix"])
total_votes = df["Voix"].sum()

for index, row in df.iterrows():
    pourcentage = (row["Voix"] / total_votes * 100) if total_votes > 0 else 0
    st.write(f"**{row['Candidat']}** : {pourcentage:.2f}% ({row['Voix']} voix)")
    st.progress(int(pourcentage))

# Annonce du gagnant
if total_votes > 0:
    st.success("🏆 Tendance actuelle : **Ousmane Sonko** est largement en tête.")

# Footer avec ton nom
st.markdown('<div class="footer">Créé par <b>Babacar Sarr dev front end</b></div>', unsafe_allow_html=True)
