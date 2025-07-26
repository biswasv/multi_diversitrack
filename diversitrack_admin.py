
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

st.set_page_config(page_title="DiversiTrack Admin", layout="centered")
st.title("🚂 DiversiTrack Admin Portal")
st.subheader("🎮 Game Control Panel")

# Firebase initialization
if "FIREBASE_CREDENTIALS" in st.secrets:
    firebase_json = st.secrets["FIREBASE_CREDENTIALS"]  # Already a dict
    cred = credentials.Certificate(firebase_json)
else:
    cred = credentials.Certificate("firebase_credentials.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Round control
st.markdown("### 🔄 Game Round Controls")
round_ref = db.collection("game").document("state")
round_doc = round_ref.get()
if round_doc.exists:
    current_round = round_doc.to_dict().get("current_round", 1)
else:
    current_round = 1

st.write(f"Current Round: **{current_round}**")

col1, col2, col3 = st.columns(3)
if col1.button("▶️ Start Game"):
    round_ref.set({"current_round": 1})
    st.success("Game started at Round 1.")

if col2.button("⏭️ Next Round"):
    round_ref.set({"current_round": current_round + 1})
    st.success(f"Advanced to Round {current_round + 1}.")

if col3.button("🔁 Reset Game"):
    # Reset state and leaderboard
    round_ref.set({"current_round": 1})
    players = db.collection("players").stream()
    for p in players:
        db.collection("players").document(p.id).delete()
    st.success("Game reset and all player data cleared.")

# Player Overview
st.markdown("### 📊 Player Allocations This Round")
players_ref = db.collection("players")
players = players_ref.stream()

data = []
for p in players:
    info = p.to_dict()
    info["name"] = p.id
    data.append(info)

if data:
    df = pd.DataFrame(data)
    df = df[["name", "round", "equity", "debt", "gold", "real_estate", "international", "sip", "portfolio_value", "score"]]
    st.dataframe(df, use_container_width=True)
else:
    st.info("No players have submitted allocations yet.")

# Leaderboard
st.markdown("### 🏆 Leaderboard")
if data:
    leaderboard = pd.DataFrame(data)
    leaderboard = leaderboard.groupby("name").agg({
        "score": "max",
        "portfolio_value": "last"
    }).sort_values(by="score", ascending=False)
    st.dataframe(leaderboard)
