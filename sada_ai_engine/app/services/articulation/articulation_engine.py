"""
Articulation Engine (Unified)

Handles all articulation levels:
- isolation
- word
- sentence
"""

from app.services.articulation.isolation_engine import detect_isolation
from app.services.articulation.articulation_preprocess import articulation_preprocess


def detect_articulation(
    level,
    global_data,
    target=None,
    target_word=None,
    target_sentence=None
):

    # 👑 preprocess
    enhanced = articulation_preprocess(global_data)

    y = enhanced["enhanced_waveform"]
    sr = enhanced["sample_rate"]

    # ---------------------------------
    # 🎯 ROUTING (FIXED + LAZY IMPORT)
    # ---------------------------------

    if level == "isolation":

        # ❗ بدون ASR
        result = detect_isolation(
            y=y,
            sr=sr,
            target_letter=target
        )

    elif level == "word":

        # 👇 lazy import → يمنع تحميل ASR في isolation
        from app.services.articulation.word_engine import detect_word_level

        result = detect_word_level(
            y=y,
            sr=sr,
            target_word=target_word,
            target_letter=target
        )

    elif level == "sentence":

        from app.services.articulation.sentence_engine import detect_sentence_level

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

    # ---------------------------------
    # 🧼 CLEAN OUTPUT (FIXED)
    # ---------------------------------

    # لو فيه details → استخدميه
    if isinstance(result, dict) and "details" in result:
        details = result["details"]
    else:
        details = result

    # شيل الحاجات المكررة
    if isinstance(details, dict):
        details = details.copy()
        details.pop("accuracy", None)
        details.pop("error_type", None)

    return {
        "mode": "articulation",

        "accuracy": result.get("accuracy", 0),

        "performance": {
            "word_correct": result.get("word_correct", None),
            "target_phoneme": result.get("target_phoneme", None)
        },

        "details": details,

        "error_type": result.get("error_type")
    }








# """
# Articulation Engine (Unified)

# Handles all articulation levels:
# - isolation
# - word
# - sentence
# """

# from app.services.articulation.isolation_engine import detect_isolation
# from app.services.articulation.word_engine import detect_word_level
# from app.services.articulation.sentence_engine import detect_sentence_level
# from app.services.articulation.articulation_preprocess import articulation_preprocess

# def detect_articulation(
#     level,
#     global_data,
#     target=None,
#     target_word=None,
#     target_sentence=None
# ):
    
    
#     # 👑 articulation-specific preprocess
#     enhanced = articulation_preprocess(global_data)

#     y = enhanced["enhanced_waveform"]
#     sr = enhanced["sample_rate"]

#     if level == "isolation":

#         result = detect_isolation(
#             y=y,
#             sr=sr,
#             target_letter=target
#         )

#     elif level == "word":

#         result = detect_word_level(
#             y=y,
#             sr=sr,
#             target_word=target_word,
#             target_letter=target
#         )

#     elif level == "sentence":

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

#     # ---------------------------------------------
#     # UNIFIED OUTPUT 👑
#     # ---------------------------------------------
#     # we unify the output format for all levels to make it easier for the frontend to consume
    
#     if "details" in result:
#         details = result["details"].copy()
#     else:
#         details = result.copy()
#     # details = result.get("details", result ) # in case details is not provided, we use the whole result as details (for backward compatibility)
#     details.pop("accuracy", None)
#     details.pop("error_type", None)
    
    
#     return {

#         "mode": "articulation",

#         "accuracy": result.get("accuracy", 0),

#         "performance": {

#             "word_correct": result.get("word_correct",None),
#             "target_phoneme": result.get("target_phoneme",None)
#         },
        

#         "details": details,

#         "error_type": result.get("error_type")
#     }