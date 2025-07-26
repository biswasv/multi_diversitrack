import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

st.set_page_config(page_title="DiversiTrack Admin Portal", layout="centered")
st.title("🎮 DiversiTrack Admin Portal")
st.header("🛠️ Game Control Panel")

# Firebase initialization
if not firebase_admin._apps:
    if "FIREBASE_CREDENTIALS" in st.secrets:
        cred = credentials.Certificate(st.secrets["FIREBASE_CREDENTIALS"])
    else:
        cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
game_ref = db.collection("game").document("state")

# Fetch game state
state = game_ref.get().to_dict() if game_ref.get().exists else {}
current_round = state.get("round", 1)
game_started = state.get("started", False)

# Game control buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ Start Game"):
        game_ref.set({"started": True, "round": 1})
        st.success("Game started at Round 1!")

with col2:
    if st.button("⏭️ Next Round"):
        if game_started:
            game_ref.update({"round": current_round + 1})
            st.success(f"Advanced to Round {current_round + 1}!")
        else:
            st.warning("Start the game first!")

with col3:
    if st.button("🔄 Reset Game"):
        game_ref.set({"started": False, "round": 1})
        st.success("Game has been reset to Round 1.")

st.markdown("---")

# Current game status
st.subheader("📊 Game Status")
st.write(f"**Current Round:** {current_round}")
st.write(f"**Game Started:** {game_started}")

# Leaderboard & player data
def fetch_all_players():
    players = db.collection("players").stream()
    data = []
    for p in players:
        d = p.to_dict()
        name = d.get("name", "Unknown")
        allocations = d.get("allocations", {})
        score = d.get("score", 0)
        data.append({"name": name, "allocations": allocations, "score": score})
    return data

players = fetch_all_players()

st.subheader("📋 Player Allocations")
if not players:
    st.info("No players have joined yet.")
else:
    for p in players:
        st.markdown(f"**{p['name']}**  ")
        round_data = p["allocations"].get(str(current_round), {})
        st.write(round_data)

st.markdown("---")

st.subheader("🏆 Leaderboard")
leaderboard = sorted(players, key=lambda x: x.get("score", 0), reverse=True)
for rank, p in enumerate(leaderboard, 1):
    st.write(f"{rank}. {p['name']} — Score: {p.get('score', 0)}")
