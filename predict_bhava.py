# 📁 bhava_poem_app/ml_model/predict_bhava.py – Real-time Bhāva prediction from phoneme

import joblib
from pathlib import Path

# Load saved vectorizer and model
vectorizer = joblib.load("ml_model/vectorizer.pkl")
model = joblib.load("ml_model/bhava_classifier.pkl")

# Meta-map for Chakras and Rasas
B_MAP = {
    "Rāgaḥ": {"chakra": "Anāhata", "rasa": "Śṛṅgāra", "emoji": "❤️"},
    "Karuṇā": {"chakra": "Anāhata", "rasa": "Karuṇā", "emoji": "💙"},
    "Krodhaḥ": {"chakra": "Maṇipūra", "rasa": "Raudra", "emoji": "😡"},
    "Bhayaṁ": {"chakra": "Mūlādhāra", "rasa": "Bhayānaka", "emoji": "😱"},
    "Vīra": {"chakra": "Svādhiṣṭhāna", "rasa": "Vīra", "emoji": "⚔️"},
    "Jñānam": {"chakra": "Ājñā", "rasa": "Adbhuta", "emoji": "📘"},
    "Śamaḥ": {"chakra": "Sahasrāra", "rasa": "Śānta", "emoji": "🕊️"},
    "Bhaktiḥ": {"chakra": "Ājñā", "rasa": "Śṛṅgāra", "emoji": "🙏"},
    "Jugupsā": {"chakra": "Mūlādhāra", "rasa": "Bībhatsa", "emoji": "🤢"},
    "Vismayaḥ": {"chakra": "Ājñā", "rasa": "Adbhuta", "emoji": "🌈"},
    "Hāsaḥ": {"chakra": "Viśuddha", "rasa": "Hāsya", "emoji": "😄"},
}

def predict_bhava(phoneme: str):
    vec = vectorizer.transform([phoneme.lower()])
    bhava = model.predict(vec)[0]
    meta = B_MAP.get(bhava, {"chakra": "?", "rasa": "?", "emoji": "❓"})
    return {
        "phoneme": phoneme,
        "bhava": bhava,
        "chakra": meta["chakra"],
        "rasa": meta["rasa"],
        "emoji": meta["emoji"]
    }

# CLI test
if __name__ == "__main__":
    while True:
        inp = input("🔤 Enter phoneme: ").strip()
        if not inp:
            break
        print(predict_bhava(inp))
