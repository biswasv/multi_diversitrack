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

st.title("🎮 DiversiTrack Player Console")

name = st.text_input("Enter your name:")
if not name:
    st.stop()

# Get current round from Firestore
round_doc = db.collection("game").document("state").get().to_dict()
current_round = round_doc.get("round", 1) if round_doc else 1
st.markdown(f"### 📈 Round {current_round}")

# Let player input score
score = st.number_input("Enter your score for this round", min_value=0, step=1)

if st.button("🚀 Submit Score"):
    db.collection("players").document(name).set({
        "name": name,
        "score": score
    })
    st.success("Score submitted!")