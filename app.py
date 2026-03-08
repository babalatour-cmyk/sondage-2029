import streamlit as st
import pandas as pd
import json
import os

DB_FILE = "election_2029_results.json"

def load_data():
    initial_data = {
        "votes": {
            "**Ousmane Sonko (PASTEF)**": 2500, 
            "Bassirou Diomaye (Coalition Diomaye Président)": 12
        },
        "views": 0
    }
    
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return initial_data
    return initial_data

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

st.set_page_config(page_title="Sondage Sénégal 2029", layout="centered")

if 'db' not in st.session_state:
    st.session_state.db = load_data()

# Incrémentation invisible des vues
if 'tracked' not in st.session_state:
    st.session_state.db["views"] += 1
    save_data(st.session_state.db)
    st.session_state.tracked = True

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, 
            rgba(0, 128, 55, 0.08) 0%, 
            rgba(255, 239, 0, 0.08) 50%, 
            rgba(227, 27, 35, 0.08) 100%);
    }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px; background: white; border-top: 1px solid #ddd; z-index: 100; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #008037; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇸🇳 Élections 2029 : Sondage en Direct")

# Affichage des photos
col_s, col_d = st.columns(2)
with col_s:
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

if 'has_voted' not in st.session_state:
    st.session_state.has_voted = False

if not st.session_state.has_voted:
    choix = st.radio("Pour qui voteriez-vous ?", list(st.session_state.db["votes"].keys()))
    if st.button("Valider mon vote 🗳️"):
        st.session_state.db["votes"][choix] += 1
        save_data(st.session_state.db)
        st.session_state.has_voted = True
        
        # ANIMATIONS POUR SONKO
        if "**Ousmane Sonko (PASTEF)**" in choix:
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
    # Calcul précis du pourcentage
    pourcentage = (row["Voix"] / total_votes * 100) if total_votes > 0 else 0
    st.write(f"**{row['Candidat']}** : {pourcentage:.2f}% ({row['Voix']} voix)")
    # Barre verte pour Sonko, rouge pour Diomaye
    couleur = "green" if "**Ousmane Sonko (PASTEF)**" in row['Candidat'] else "red"
    st.progress(int(pourcentage))

if total_votes > 0:
    gagnant = df.loc[df['Voix'].idxmax()]['Candidat']
    if "**Ousmane Sonko (PASTEF)**" in gagnant:
        st.success(f"🏆 Tendance actuelle : **{gagnant}** est en tête.")
    else:
        st.info(f"🏆 Tendance actuelle : **{gagnant}** est en tête.")

# Footer
st.markdown(f'<div class="footer">Créé par <b>Babacar Sarr dev front end</b></div>', unsafe_allow_html=True)
