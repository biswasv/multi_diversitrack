# diversitrack_player.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

st.set_page_config(page_title="DiversiTrack Player Portal")
st.title("DiversiTrack Player Portal")

# Initialize Firebase
if "FIREBASE_CREDENTIALS" in st.secrets:
    firebase_json = json.loads(st.secrets["FIREBASE_CREDENTIALS"])
    cred = credentials.Certificate(firebase_json)
else:
    cred = credentials.Certificate("firebase_credentials.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Ask for player's name
name = st.text_input("Enter your name to join the game:")
if not name:
    st.stop()

# Get current round
game_doc = db.collection("game").document("state").get()
if not game_doc.exists:
    st.warning("Game not started yet. Please wait for the admin.")
    st.stop()
current_round = game_doc.to_dict().get("round", 0)

st.subheader(f"📈 DiversiTrack - Round {current_round}")

# Get previous allocation if exists
player_doc = db.collection("players").document(name).get()
prev_data = player_doc.to_dict() if player_doc.exists else {}
prev_allocation = prev_data.get("allocations", {}).get(str(current_round - 1), {})

st.write("💼 Enter your asset allocation for this round:")
assets = ["Equity", "Debt", "Gold", "Real Estate", "International"]
allocation = {}
total = 0
for asset in assets:
    default = int(prev_allocation.get(asset, 0))
    val = st.number_input(asset, min_value=0, step=1000, value=default)
    allocation[asset] = val
    total += val

if total <= 0:
    st.warning("Please allocate a non-zero amount to participate.")
    st.stop()

if st.button("Submit Allocation"):
    doc_ref = db.collection("players").document(name)
    doc_data = doc_ref.get().to_dict() if doc_ref.get().exists else {}
    allocations = doc_data.get("allocations", {})
    allocations[str(current_round)] = allocation
    doc_ref.set({"name": name, "allocations": allocations}, merge=True)
    st.success(f"Allocation submitted for Round {current_round}!")
