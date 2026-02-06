# Model.py (Streamlit app)

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path

import streamlit as st  # type: ignore

st.set_page_config(page_title="Live Feedback Wall", layout="wide")

st.title("🗣️ Live Feedback Wall")
st.write(
    "Submit feedback below to appear instantly on the live wall and hear a spoken vote of thanks."
)

FEEDBACK_STORE = Path("feedback_store.json")


def load_feedbacks() -> list[dict[str, object]]:
    if not FEEDBACK_STORE.exists():
        return []
    try:
        return json.loads(FEEDBACK_STORE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_feedbacks(entries: list[dict[str, object]]) -> None:
    FEEDBACK_STORE.write_text(json.dumps(entries, indent=2), encoding="utf-8")


if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = load_feedbacks()

if "announce_name" not in st.session_state:
    st.session_state.announce_name = None

def speak_vote_of_thanks(name: str) -> None:
    message = f"Thank you, {name}, for your feedback."
    st.components.v1.html(
        f"""
        <script>
          const message = {message!r};
          const utterance = new SpeechSynthesisUtterance(message);
          utterance.rate = 1;
          utterance.pitch = 1;
          speechSynthesis.cancel();
          speechSynthesis.speak(utterance);
        </script>
        """,
        height=0,
    )


with st.form("feedback_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input("Your name", placeholder="e.g., Asha")
        feedback = st.text_area(
            "Your feedback",
            placeholder="Share your thoughts...",
            height=140,
        )
    with col2:
        rating = st.slider("Rating", min_value=1, max_value=5, value=5)
        is_public = st.checkbox("Show my feedback on the live wall", value=True)

    submitted = st.form_submit_button("Submit feedback")

if submitted:
    trimmed_name = name.strip()
    trimmed_feedback = feedback.strip()

    if not trimmed_name or not trimmed_feedback:
        st.error("Please enter both your name and feedback before submitting.")
    else:
        st.session_state.feedbacks.insert(
            0,
            {
                "name": trimmed_name,
                "feedback": trimmed_feedback,
                "rating": rating,
                "is_public": is_public,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            },
        )
        st.session_state.announce_name = trimmed_name
        save_feedbacks(st.session_state.feedbacks)
        st.success("Feedback received! 🎉")

if st.session_state.announce_name:
    speak_vote_of_thanks(st.session_state.announce_name)
    st.session_state.announce_name = None

st.markdown("---")

left, right = st.columns([3, 1])

with left:
    st.subheader("Live Feedback Feed")
    if not st.session_state.feedbacks:
        st.info("No feedback yet. Be the first to share your thoughts!")
    else:
        for entry in st.session_state.feedbacks:
            if not entry["is_public"]:
                continue
            st.markdown(
                f"""
                **{entry['name']}** · ⭐ {entry['rating']} · {entry['timestamp']}  
                {entry['feedback']}
                """
            )
            st.markdown("---")

with right:
    st.subheader("Live Stats")
    total_feedback = len(st.session_state.feedbacks)
    public_feedback = sum(1 for entry in st.session_state.feedbacks if entry["is_public"])
    avg_rating = (
        sum(entry["rating"] for entry in st.session_state.feedbacks) / total_feedback
        if total_feedback
        else 0
    )
    st.metric("Total submissions", total_feedback)
    st.metric("Public on wall", public_feedback)
    st.metric("Average rating", f"{avg_rating:.1f}" if total_feedback else "N/A")

st.caption(
    "The vote of thanks is spoken through your browser using the Web Speech API."
)
