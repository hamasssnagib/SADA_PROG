"""
Articulation Engine (Unified Production Version)

Handles:
- isolation
- syllable
- word
- sentence
"""

from app.services.articulation.isolation_engine import detect_isolation

from app.services.articulation.articulation_preprocess import (
    articulation_preprocess
)


def detect_articulation(

    level,
    global_data,

    target=None,
    target_word=None,
    target_sentence=None
):

    # -------------------------------------------------
    # 🎧 articulation preprocess
    # -------------------------------------------------

    enhanced = articulation_preprocess(global_data)

    y = enhanced["enhanced_waveform"]
    sr = enhanced["sample_rate"]

    # -------------------------------------------------
    # 🎯 routing
    # -------------------------------------------------

    if level == "isolation":

        result = detect_isolation(

            y=y,
            sr=sr,

            target_letter=target
        )

    elif level == "syllable":

        from app.services.articulation.syllable_engine import (
            detect_syllable_level
        )

        result = detect_syllable_level(

            y=y,
            sr=sr,

            target_word=target_word,
            target_letter=target
        )

    elif level == "word":

        from app.services.articulation.word_engine import (
            detect_word_level
        )

        result = detect_word_level(

            y=y,
            sr=sr,

            target_word=target_word,
            target_letter=target
        )

    elif level == "sentence":

        from app.services.articulation.sentence_engine import (
            detect_sentence_level
        )

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

            "exercise_level": level,

            "accuracy": 0,

            "performance": {
                "exercise_correct": False,
                "target_phoneme": None
            },

            "details": {},

            "error_type": "invalid_level"
        }

    # -------------------------------------------------
    # 🧼 unified response
    # -------------------------------------------------

    return {

        "mode": "articulation",

        "exercise_level": level,

        "accuracy":
            result.get("accuracy", 0),

        "performance": {

            "exercise_correct":
                result.get("exercise_correct"),

            "target_phoneme":
                result.get("target_phoneme")
        },

        "details": {

            "recognized_text":
                result.get("recognized_text"),

            "expected_phonemes":
                result.get("expected_phonemes"),

            "spoken_phonemes":
                result.get("spoken_phonemes"),

            "target_phoneme":
                result.get("target_phoneme"),

            "target_positions":
                result.get("target_positions"),

            "errors":
                result.get("errors"),

            "original_text":
                result.get("original_text"),

            "target_unit":
                result.get("target_unit"),

            "similarity_score":
                result.get("similarity_score")
        },

        "error_type":
            result.get("error_type")
    }




# """
# Articulation Engine (Unified)

# Handles all articulation levels:
# - isolation
# - word
# - sentence
# """

# from app.services.articulation.isolation_engine import detect_isolation
# from app.services.articulation.articulation_preprocess import articulation_preprocess


# def detect_articulation(
#     level,
#     global_data,
#     target=None,
#     target_word=None,
#     target_sentence=None
# ):

#     # 👑 preprocess
#     enhanced = articulation_preprocess(global_data)

#     y = enhanced["enhanced_waveform"]
#     sr = enhanced["sample_rate"]

#     # ---------------------------------
#     # 🎯 ROUTING (FIXED + LAZY IMPORT)
#     # ---------------------------------

#     if level == "isolation":

#         # ❗ بدون ASR
#         result = detect_isolation(
#             y=y,
#             sr=sr,
#             target_letter=target
#         )

#     elif level == "word":

#         # 👇 lazy import → يمنع تحميل ASR في isolation
#         from app.services.articulation.word_engine import detect_word_level

#         result = detect_word_level(
#             y=y,
#             sr=sr,
#             target_word=target_word,
#             target_letter=target
#         )

#     elif level == "sentence":

#         from app.services.articulation.sentence_engine import detect_sentence_level

#         result = detect_sentence_level(
#             y=y,
#             sr=sr,
#             target_sentence=target_sentence,
#             target_word=target_word,
#             target_letter=target
#         )

#     else:
#         return {
#             "mode": "articulation",
#             "accuracy": 0,
#             "performance": {},
#             "details": {},
#             "error_type": "invalid_level"
#         }

#     # ---------------------------------
#     # 🧼 CLEAN OUTPUT (FIXED)
#     # ---------------------------------

#     # لو فيه details → استخدميه
#     if isinstance(result, dict) and "details" in result:
#         details = result["details"]
#     else:
#         details = result

#     # شيل الحاجات المكررة
#     if isinstance(details, dict):
#         details = details.copy()
#         details.pop("accuracy", None)
#         details.pop("error_type", None)

#     return {
#         "mode": "articulation",

#         "accuracy": result.get("accuracy", 0),

#         "performance": {
#             "word_correct": result.get("word_correct", None),
#             "target_phoneme": result.get("target_phoneme", None)
#         },

#         "details": details,

#         "error_type": result.get("error_type")
#     }







