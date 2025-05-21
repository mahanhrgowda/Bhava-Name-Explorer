# 📁 bhava_poem_app/tokenizer.py – Tokenize name into Sanskrit-compatible phonemes

def tokenize_name(name):
    name = name.lower()

    # Prioritized known phoneme clusters
    known = [
        "ksha", "tra", "jna", "śa", "sha", "cha", "tha", "dha", "gha", "bha",
        "ph", "th", "dh", "gh", "sh", "ch", "jh", "ng", "ny", "zh", "kh", "bh",
        "ka", "kha", "ga", "gha", "ṅa",
        "ca", "cha", "ja", "jha", "ña",
        "ṭa", "ṭha", "ḍa", "ḍha", "ṇa",
        "ta", "tha", "da", "dha", "na",
        "pa", "pha", "ba", "bha", "ma",
        "ya", "ra", "la", "va",
        "śa", "ṣa", "sa", "ha",
        "a", "ā", "i", "ī", "u", "ū", "ṛ", "ṝ", "e", "ai", "o", "au"
    ]

    known.sort(key=lambda x: -len(x))  # match longest first
    idx, tokens = 0, []

    while idx < len(name):
        matched = False
        for k in known:
            if name[idx:idx+len(k)] == k:
                tokens.append(k)
                idx += len(k)
                matched = True
                break
        if not matched:
            tokens.append(name[idx])
            idx += 1

    return tokens
