import streamlit as st
import pandas as pd
import json
import os

# Fichier de stockage des données
DB_FILE = "election_2029_results.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"Ousmane Sonko": 0, "Bassirou Diomaye Faye": 0}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# Configuration de la page pour mobile
st.set_page_config(page_title="Sondage Sénégal 2029", layout="centered")

# Style CSS pour le design
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #008037; color: white; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px; background: white; border-top: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# Initialisation
if 'votes' not in st.session_state:
    st.session_state.votes = load_data()

st.title("🇸🇳 Élections 2029 : Votre Choix")
st.write("Sondage en temps réel pour le futur du Sénégal.")

# Système de vote
if 'has_voted' not in st.session_state:
    st.session_state.has_voted = False

if not st.session_state.has_voted:
    choix = st.radio("Sélectionnez un candidat :", list(st.session_state.votes.keys()))
    if st.button("Voter maintenant"):
        st.session_state.votes[choix] += 1
        save_data(st.session_state.votes)
        st.session_state.has_voted = True
        st.balloons()
        st.rerun()
else:
    st.success("✅ Votre vote a été enregistré avec succès !")

st.subheader("Tendances actuelles")
df = pd.DataFrame(list(st.session_state.votes.items()), columns=["Candidat", "Voix"])
total = df["Voix"].sum()

if total > 0:
    for index, row in df.iterrows():
        pct = (row["Voix"] / total) * 100
       
        color = "#008037" if index == 0 else "#e31b23"
        
        st.write(f"**{row['Candidat']}** ({int(pct)}%)")
        st.progress(int(pct))
    
    st.caption(f"Total des suffrages exprimés : {total} voix")
else:
    st.info("En attente des premiers votes...")


st.markdown(
    f"""
    <div class="footer">
        <p style="margin:0; font-size: 0.9em; color: #555;">
            Créé par <b>Babacar Sarr dev front end</b> 🚀
        </p>
    </div>
    """, unsafe_allow_html=True
)