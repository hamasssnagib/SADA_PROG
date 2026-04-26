"""
Articulation Engine (Unified)

Handles all articulation levels:
- isolation
- word
- sentence
"""

from app.services.articulation.isolation_engine import detect_isolation
from app.services.articulation.word_engine import detect_word_level
from app.services.articulation.sentence_engine import detect_sentence_level
from app.services.articulation.articulation_preprocess import articulation_preprocess

def detect_articulation(
    level,
    global_data,
    target=None,
    target_word=None,
    target_sentence=None
):
    
    
    # 👑 articulation-specific preprocess
    enhanced = articulation_preprocess(global_data)

    y = enhanced["enhanced_waveform"]
    sr = enhanced["sample_rate"]

    if level == "isolation":

        result = detect_isolation(
            y=y,
            sr=sr,
            target_letter=target
        )

    elif level == "word":

        result = detect_word_level(
            y=y,
            sr=sr,
            target_word=target_word,
            target_letter=target
        )

    elif level == "sentence":

        result = detect_sentence_level(
            y=y,
            sr=sr,
            target_sentence=target_sentence,
            target_word=target_word,
            target_letter=target
        )

    else:
        return {
            "mode": "articulation",
            "accuracy": 0,
            "performance": {},
            "details": {},
            "error_type": "invalid_level"
        }

    # ---------------------------------------------
    # UNIFIED OUTPUT 👑
    # ---------------------------------------------

    return {

        "mode": "articulation",

        "accuracy": result.get("accuracy", 0),

        "performance": {

            "word_correct": result.get("word_correct"),
            "target_phoneme": result.get("target_phoneme"),
        },

        "details": result,

        "error_type": result.get("error_type")
    }