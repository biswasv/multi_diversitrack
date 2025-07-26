# diversitrack_admin.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

st.set_page_config(page_title="DiversiTrack Admin Portal")
st.title("DiversiTrack Admin Portal")
st.subheader("🎛️ Game Control Panel")

# Initialize Firebase
if "FIREBASE_CREDENTIALS" in st.secrets:
    firebase_json = json.loads(st.secrets["FIREBASE_CREDENTIALS"])
    cred = credentials.Certificate(firebase_json)
else:
    cred = credentials.Certificate("firebase_credentials.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

game_ref = db.collection("game").document("state")
game_data = game_ref.get().to_dict() if game_ref.get().exists else {}

# Display current round
current_round = game_data.get("round", 0)
st.markdown(f"### 📈 Current Round: {current_round}")

# Button to start or advance game
if st.button("Start New Game"):
    game_ref.set({"round": 1, "started": True})
    st.success("Game started! Round 1 is live.")

if st.button("Next Round"):
    new_round = current_round + 1
    game_ref.update({"round": new_round})
    st.success(f"Advanced to Round {new_round}")

if st.button("Reset Game"):
    game_ref.set({"round": 0, "started": False})
    st.success("Game reset. Waiting to start.")

# Show all player scores (if submitted)
st.markdown("---")
st.subheader("📊 Player Submissions")
players = db.collection("players").stream()
for player in players:
    data = player.to_dict()
    name = data.get("name", "Unknown")
    allocations = data.get("allocations", {})
    st.markdown(f"**{name}**")
    for rnd, alloc in allocations.items():
        st.markdown(f"- Round {rnd}: {alloc}")
