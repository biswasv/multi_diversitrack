# diversitrack_admin.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

st.set_page_config(page_title="DiversiTrack Admin Portal")
st.title("DiversiTrack Admin Portal")
st.subheader("Game Control Panel")

# Initialize Firebase
if "FIREBASE_CREDENTIALS" in st.secrets:
    firebase_json = json.loads(st.secrets["FIREBASE_CREDENTIALS"])
    cred = credentials.Certificate(firebase_json)
else:
    cred = credentials.Certificate("firebase_credentials.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Display current round
game_doc = db.collection("game").document("state").get()
if game_doc.exists:
    current_round = game_doc.to_dict().get("round", 0)
    st.success(f"Current Round: {current_round}")
else:
    st.warning("Game not started yet.")
    current_round = 0

# Start new game
if st.button("Start New Game"):
    db.collection("game").document("state").set({"round": 1})
    st.success("Game started with Round 1")

# Go to next round
if current_round > 0 and st.button("Go to Next Round"):
    db.collection("game").document("state").update({"round": current_round + 1})
    st.success(f"Moved to Round {current_round + 1}")

# Show leaderboard
st.subheader("Leaderboard")
scores_ref = db.collection("scores").order_by("score", direction=firestore.Query.DESCENDING).stream()
for i, doc in enumerate(scores_ref):
    score_data = doc.to_dict()
    st.write(f"{i+1}. {score_data.get('name')} - Score: {score_data.get('score')}")
