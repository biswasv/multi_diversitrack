import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("DiversiTrack Admin Portal")
st.subheader("Game Control Panel")

# Round controller
round_doc = db.collection("game_state").document("current_round")
round_info = round_doc.get().to_dict() if round_doc.get().exists else {"round": 1}

current_round = st.number_input("Current Round", min_value=1, step=1, value=round_info["round"])
if st.button("Update Round for All Players"):
    round_doc.set({"round": int(current_round)})
    st.success(f"Game round updated to Round {int(current_round)}.")

# View leaderboard
st.subheader("Leaderboard")
players_ref = db.collection("leaderboard")
players = players_ref.stream()
for player in players:
    st.write(player.to_dict())