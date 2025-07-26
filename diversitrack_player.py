import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import random

# Firebase Init
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.title("DiversiTrack Player Portal")

# Get current round from Firebase
round_doc = db.collection("game_state").document("current_round")
round_info = round_doc.get().to_dict() if round_doc.get().exists else {"round": 1}
current_round = round_info["round"]

# Player Info
player_name = st.text_input("Enter your name:")
if "player_id" not in st.session_state:
    st.session_state.player_id = f"{player_name}_{random.randint(1000, 9999)}"

if player_name:
    st.subheader(f"Round {current_round} - Asset Allocation")
    assets = ["Equity", "Debt", "Gold", "Real Estate", "International"]
    allocation = {}
    total = 0

    for asset in assets:
        val = st.number_input(f"{asset}", min_value=0, step=10000, key=asset)
        allocation[asset] = val
        total += val

    if total != 1000000:
        st.error("Total must be ₹10,00,000 to proceed.")
    else:
        if st.button("Submit Allocation"):
            db.collection("players").document(st.session_state.player_id).set({
                "name": player_name,
                "round": current_round,
                "allocation": allocation
            })
            st.success("Allocation submitted. Wait for admin to proceed to next round.")

    # Display current round event (mock)
    st.subheader("Event")
    st.info(f"Round {current_round} Event: Market Shock")

    # Final score submission at last round (mock)
    if st.button("Submit Final Score"):
        db.collection("leaderboard").document(st.session_state.player_id).set({
            "Name": player_name,
            "Score": random.randint(1, 100)
        })
        st.success("Score submitted to leaderboard!")