# 📁 bhava_poem_app/app.py – Main Streamlit UI
import streamlit as st
import pandas as pd
from engine import process_name, generate_poem
from tokenizer import tokenize_name
from data import PHONEME_BHAVA_MAP
from phoneme_guess import guess_bhava_for_unknown
from ml_model.predict_bhava import predict_bhava

st.set_page_config(page_title="Bhāva Name Explorer", layout="wide")
st.title("🔤 Bhāva Name Engine")

name = st.text_input("Enter a name:")
script_mode = st.radio("Display script:", ["Devanagari", "IAST", "IPA"], horizontal=True)

if name:
    result = process_name(name)
    st.subheader(f"✅ Bhāva Summary for '{name.title()}'")

    # Vector
    st.markdown("### 🧬 Bhāva Vector")
    st.json(result["vector"])

    # Dominant + Secondary Bhāvas
    st.markdown("### 🌈 Dominant Bhāva(s):")
    for b in result["dominant"]:
        st.markdown(f"- {b} {result['emojis'][b]}")

    if result["secondary"]:
        st.markdown("### 🔥 Secondary Bhāva(s):")
        for b in result["secondary"]:
            st.markdown(f"- {b} {result['emojis'][b]}")

    # Chakra Flow + Rasa
    st.markdown("### 🌀 Chakra Flow:")
    st.write(" → ".join(result["chakra_flow"]))

    st.markdown("### 🎭 Rasa Blend:")
    st.write(" + ".join(result["rasa_blend"]))

    # Token trace
    st.markdown("### 🔤 Phoneme Trace Table")
    rows = []
    for p in tokenize_name(name):
        row = {}
        data = PHONEME_BHAVA_MAP.get(p)
        if not data:
            try:
                data = predict_bhava(p)
                status = "🔧 ML-predicted"
            except:
                data = guess_bhava_for_unknown(p)
                status = "⚠️ Guessed"
        else:
            status = "✅ Exact"
        row.update({
            "Phoneme": p,
            "Bhāva": data["bhava"],
            "Chakra": data["chakra"],
            "Rasa": data["rasa"],
            "Emoji": data.get("emoji", ""),
            "Status": status
        })
        rows.append(row)

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    with st.expander("ℹ️ Legend: Chakra, Rasa & Status"):
        st.markdown("**Statuses**\n- ✅ Exact\n- ⚠️ Guessed\n- 🔧 ML-predicted")

    st.markdown("### 🪷 Sanskrit Poem")
    st.markdown(generate_poem(result["dominant"], result["secondary"], script_mode))
