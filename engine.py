# 📁 bhava_poem_app/engine.py

from tokenizer import tokenize_name
from data import PHONEME_BHAVA_MAP, CHAKRA_WEIGHTS, CHANDAS_SYLLABLE_COUNT, CHANDAS_TAGS
from phoneme_guess import guess_bhava_for_unknown
from ml_model.predict_bhava import predict_bhava

def process_name(name):
    phonemes = tokenize_name(name)
    scores, details, trace_log = {}, [], []
    total_score = 0

    for p in phonemes:
        if p in PHONEME_BHAVA_MAP:
            data = PHONEME_BHAVA_MAP[p]
            status = "✅ Exact"
        else:
            try:
                data = predict_bhava(p)
                status = "🔧 ML"
            except:
                data = guess_bhava_for_unknown(p)
                status = "⚠️ Guess"
        weight = CHAKRA_WEIGHTS.get(data["chakra"], 1.0)
        scores[data["bhava"]] = scores.get(data["bhava"], 0) + weight
        details.append({**data, "phoneme": p, "score": weight, "status": status})
        total_score += weight
        trace_log.append(f"🔤 {p} → {data['bhava']} {data.get('emoji','')} | {data['chakra']} | {data['rasa']} {status}")

    vector = {b: round(s / total_score * 100, 1) for b, s in scores.items()}
    sorted_bhavas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    dominant = [b for b, v in sorted_bhavas if v / total_score * 100 >= 33]
    secondary = [b for b, v in sorted_bhavas if v / total_score * 100 < 33]
    chakra_flow = [f"{d['chakra']} {d.get('emoji','')}" for d in details]
    rasa_blend = list(dict.fromkeys([f"{d['rasa']} {d.get('emoji','')}" for d in details]))
    emojis = {d['bhava']: d.get('emoji', '') for d in details}

    return {
        "vector": vector,
        "dominant": dominant,
        "secondary": secondary,
        "chakra_flow": chakra_flow,
        "rasa_blend": rasa_blend,
        "trace": trace_log,
        "emojis": emojis
    }

def count_syllables(line):
    return len([c for c in line if c in "अआइईउऊऋॠऌॡएऐओऔअंअः"])

def generate_poem(dominant_bhavas, secondary_bhavas, script_mode):
    from transliterate import transliterate_text
    from transliterate import sanscript
    lines = []
    for bhava in dominant_bhavas:
        if bhava in CHANDAS_TAGS:
            tag, stanzas, meter = CHANDAS_TAGS[bhava]
            expected = CHANDAS_SYLLABLE_COUNT.get(meter, None)
            for l in stanzas:
                sylls = count_syllables(l)
                if script_mode == "Devanagari":
                    lines.append(f"**{l}** _(syllables: {sylls}/{expected})_")
                elif script_mode == "IAST":
                    iast = transliterate_text(l, sanscript.DEVANAGARI, sanscript.IAST)
                    lines.append(f"*{iast}* _(syllables: {sylls}/{expected})_")
                elif script_mode == "IPA":
                    from sanskrit_transliteration.ipa import devanagari_to_ipa
                    ipa = devanagari_to_ipa(l)
                    lines.append(f"`{ipa}` _(syllables: {sylls}/{expected})_")
    if script_mode == "Devanagari":
        lines.append("**नित्यम् विजयते भावः।** 🌟")
    elif script_mode == "IAST":
        lines.append("*nityam vijayate bhāvaḥ* 🌟")
    elif script_mode == "IPA":
        lines.append("`nɪt̪jəm ʋɪd͡ʑəjət̪e bʱɑːʋəɦ` 🌟")
    return "\n".join(lines)
