import streamlit as st
import json
import io
from firebase_admin import credentials, firestore, initialize_app

# Load Firebase credentials from Streamlit secrets
firebase_json = json.loads(st.secrets["FIREBASE_CREDENTIALS"])
cred = credentials.Certificate(io.StringIO(json.dumps(firebase_json)))

# Initialize Firebase
if not firestore._apps:
    initialize_app(cred)
db = firestore.client()

st.title("🎛️ DiversiTrack Admin Panel")

if "current_round" not in st.session_state:
    st.session_state.current_round = 1

round_in_db = db.collection("game").document("state")
data = round_in_db.get().to_dict()

if data:
    st.session_state.current_round = data.get("round", 1)

new_round = st.number_input("Set Current Round", min_value=1, max_value=50, value=st.session_state.current_round)
if st.button("✅ Update Round for All Players"):
    round_in_db.set({"round": int(new_round)})
    st.success(f"Round updated to {new_round}!")

st.markdown("---")
st.subheader("🏆 Leaderboard")
players = db.collection("players").stream()
leaderboard = []
for p in players:
    d = p.to_dict()
    leaderboard.append((d.get("name", "Unknown"), d.get("score", 0)))

leaderboard.sort(key=lambda x: x[1], reverse=True)
for i, (name, score) in enumerate(leaderboard, 1):
    st.write(f"**{i}. {name}** — 💰 Score: `{score}`")