# 📁 bhava_poem_app/phoneme_guess.py – Fallback logic for unknown phonemes

import random
from data import PHONEME_BHAVA_MAP

# Default Bhāva pool for random fallback
DEFAULT_BHAVA_POOL = [
    {"bhava": "Śamaḥ", "chakra": "Sahasrāra", "rasa": "Śānta", "emoji": "🕊️"},
    {"bhava": "Karuṇā", "chakra": "Anāhata", "rasa": "Karuṇā", "emoji": "💙"},
    {"bhava": "Utsāhaḥ", "chakra": "Svādhiṣṭhāna", "rasa": "Vīra", "emoji": "⚔️"},
    {"bhava": "Jñānam", "chakra": "Ājñā", "rasa": "Adbhuta", "emoji": "📘"},
    {"bhava": "Rāgaḥ", "chakra": "Anāhata", "rasa": "Śṛṅgāra", "emoji": "❤️"},
    {"bhava": "Krodhaḥ", "chakra": "Maṇipūra", "rasa": "Raudra", "emoji": "😡"},
    {"bhava": "Hāsaḥ", "chakra": "Viśuddha", "rasa": "Hāsya", "emoji": "😄"}
]

def guess_bhava_for_unknown(phoneme):
    # Try first-letter match fallback
    for key in PHONEME_BHAVA_MAP:
        if phoneme[0] == key[0]:
            return PHONEME_BHAVA_MAP[key]
    return random.choice(DEFAULT_BHAVA_POOL)

def normalize_phoneme(p):
    p = p.lower()
    fallback = {
        "a": "ra", "b": "ba", "c": "cha", "d": "da", "e": "na", "f": "pha",
        "g": "ga", "h": "ha", "i": "vi", "j": "ja", "k": "ka", "l": "la",
        "m": "ma", "n": "na", "o": "so", "p": "pa", "q": "ka", "r": "ra",
        "s": "sa", "t": "ta", "u": "ru", "v": "va", "w": "va", "x": "ksha",
        "y": "ya", "z": "ja", "th": "tha", "ph": "pha", "ch": "cha",
        "sh": "śa", "ng": "ṅa", "dh": "dha", "gh": "gha"
    }
    return fallback.get(p, p)
