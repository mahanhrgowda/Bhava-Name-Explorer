# 📁 bhava_poem_app/moderator.py – Suggestion Approval Panel

import json
import streamlit as st
from pathlib import Path

SUGGESTED_FILE = Path("assets/suggested_phonemes.json")
APPROVED_FILE = Path("assets/approved_phonemes.json")
REJECTED_FILE = Path("assets/rejected_phonemes.json")

st.set_page_config(page_title="🛡️ Moderator Panel", layout="centered")
st.title("🛡️ Bhāva Moderator Panel")

if not SUGGESTED_FILE.exists():
    SUGGESTED_FILE.write_text("{}")

suggestions = json.loads(SUGGESTED_FILE.read_text(encoding="utf-8"))

if not suggestions:
    st.success("✅ All suggestions reviewed.")
else:
    st.markdown(f"**Pending Suggestions: {len(suggestions)}**")

    for phon, entry in suggestions.items():
        with st.expander(f"🔤 `{phon}` → {entry['bhava']}, {entry['chakra']}, {entry['rasa']}"):
            st.caption(f"🕒 {entry.get('timestamp', 'N/A')} | 👤 {entry.get('user_id', 'anonymous')}")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"✅ Approve `{phon}`", key=f"a_{phon}"):
                    approved = json.loads(APPROVED_FILE.read_text()) if APPROVED_FILE.exists() else {}
                    approved[phon] = entry
                    APPROVED_FILE.write_text(json.dumps(approved, indent=2, ensure_ascii=False))
                    del suggestions[phon]
                    SUGGESTED_FILE.write_text(json.dumps(suggestions, indent=2, ensure_ascii=False))
                    st.experimental_rerun()
            with col2:
                if st.button(f"❌ Reject `{phon}`", key=f"r_{phon}"):
                    rejected = json.loads(REJECTED_FILE.read_text()) if REJECTED_FILE.exists() else {}
                    rejected[phon] = entry
                    REJECTED_FILE.write_text(json.dumps(rejected, indent=2, ensure_ascii=False))
                    del suggestions[phon]
                    SUGGESTED_FILE.write_text(json.dumps(suggestions, indent=2, ensure_ascii=False))
                    st.experimental_rerun()
