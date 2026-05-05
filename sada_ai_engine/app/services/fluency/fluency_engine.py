"""
Fluency Engine (Final Fixed Version 👑)

- Smart validation (مش strict زي articulation)
- يحمي من ASR الغلط
- يوازن بين النص والصوت
"""

from difflib import SequenceMatcher

from app.services.fluency.fluency_preprocess import fluency_preprocess
from app.services.fluency.segmentation import segmentation_pipeline
from app.services.fluency.repetition_detection import detect_repetition
from app.services.fluency.prolongation_detection import detect_prolongation
from app.services.fluency.fluency_decision import fluency_decision

from app.services.text.text_cleaner import clean_arabic_text
from app.services.asr.asr_engine import transcribe_audio


# ---------------------------------------------------------
# similarity helper
# ---------------------------------------------------------

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


# ---------------------------------------------------------
# Main Fluency Detection
# ---------------------------------------------------------

def detect_fluency(global_data, target_text=None):

    recognized_text = None
    weak_match = False
    sim_score = None

    # ---------------------------------------------
    # STEP 0: SMART VALIDATION 👑
    # ---------------------------------------------

    if target_text is not None:

        recognized_text = transcribe_audio(
            global_data["waveform"],
            global_data["sample_rate"]
        )

        if not recognized_text:
            return {
                "mode": "fluency",
                "accuracy": 0,
                "performance": {},
                "error_type": "no_speech_detected",
                "details": {}
            }

        # 🧼 clean
        recognized_text = clean_arabic_text(recognized_text)
        target_text = clean_arabic_text(target_text)

        # 🎯 similarity
        sim_score = similarity(recognized_text, target_text)

        # ---------------------------------------------
        # ❌ بعيد خالص → stop
        # ---------------------------------------------
        if sim_score < 0.4:
            return {
                "mode": "fluency",
                "accuracy": 0,
                "performance": {},
                "error_type": "wrong_task",
                "details": {
                    "recognized_text": recognized_text,
                    "similarity_score": sim_score
                }
            }

        # ---------------------------------------------
        # ⚠️ weak match (نكمل بس نقلل score)
        # ---------------------------------------------
        if sim_score < 0.6:
            weak_match = True

    # ---------------------------------------------
    # STEP 1: Preprocess
    # ---------------------------------------------

    fluency_data = fluency_preprocess(global_data)

    y = fluency_data["waveform"]
    sr = fluency_data["sample_rate"]

    # ---------------------------------------------
    # STEP 2: Segmentation + pauses
    # ---------------------------------------------

    seg = segmentation_pipeline(y, sr)

    intervals = seg["intervals"]
    pause_count = seg["pause_count"]
    max_pause = seg["max_pause"]

    # ---------------------------------------------
    # STEP 3: Repetition
    # ---------------------------------------------

    rep = detect_repetition(y, sr, intervals)
    repetition_count = rep["repetition_count"]

    # ---------------------------------------------
    # STEP 4: Prolongation
    # ---------------------------------------------

    prol = detect_prolongation(y, sr, intervals)
    prolongation_count = prol["prolongation_count"]

    # ---------------------------------------------
    # STEP 5: Decision
    # ---------------------------------------------

    decision = fluency_decision(
        repetition_count=repetition_count,
        pause_count=pause_count,
        max_pause=max_pause,
        prolongation_count=prolongation_count
    )

    accuracy = decision["fluency_score"]

    # ---------------------------------------------
    # 👑 FINAL SCORE ADJUSTMENT
    # ---------------------------------------------

    # ⚠️ لو النص مش مضبوط قوي → قلل السكور
    if target_text is not None and weak_match:
        accuracy = min(accuracy, 60)

    # ⚠️ لو similarity متوسطة → قلل أكتر
    if target_text is not None and sim_score is not None and sim_score < 0.5:
        accuracy = min(accuracy, 50)

    # ---------------------------------------------
    # FINAL OUTPUT
    # ---------------------------------------------

    return {

        "mode": "fluency",

        "accuracy": accuracy,

        "performance": {
            "stuttering_type": decision["stuttering_type"],
            "severity": decision["severity"]
        },

        "details": {
            "recognized_text": recognized_text if target_text else None,
            "similarity_score": sim_score,
            "repetition_count": repetition_count,
            "pause_count": pause_count,
            "max_pause": float(max_pause),
            "prolongation_count": prolongation_count
        },

        "error_type": None
    }# """Input: waveform + sample_rate





# ↓
# preprocess
# ↓
# segmentation
# ↓
# repetition
# ↓
# prolongation
# ↓
# decision
# ↓
# Output structured"""

# """
# Fluency Engine (Final Version)

# End-to-End Stuttering Detection
# """

# from app.services.fluency.fluency_preprocess import fluency_preprocess
# from app.services.fluency.segmentation import segmentation_pipeline
# from app.services.fluency.repetition_detection import detect_repetition
# from app.services.fluency.prolongation_detection import detect_prolongation
# from app.services.fluency.fluency_decision import fluency_decision
# from app.services.validation.validation_engine import validate_spoken_input
# from app.services.asr.asr_engine import transcribe_audio




# # ---------------------------------------------------------
# # Main Fluency Detection
# # ---------------------------------------------------------

# def detect_fluency(global_data,target_text=None):
    
#     recognized_text = None
#     # ---------------------------------------------
#     # STEP 0: VALIDATION 👑
#     # ---------------------------------------------

#     if target_text is not None:  # ممكن تبقى كلمة أو جملة

#         recognized_text = transcribe_audio(
#             global_data["waveform"],
#             global_data["sample_rate"]
#         )

#         valid, score, recognized_text = validate_spoken_input(
#             recognized_text,
#             target_text,
#             threshold=0.2  # for fluency, we can be more lenient on the similarity score since timing is more important than exact wording
#         )

#         if not valid:

#             return {
#                 "mode": "fluency",
#                 "accuracy": 0,
#                 "performance": {},
#                 "error_type": "wrong_task",
#                 "details": {
#                     "recognized_text": recognized_text,
#                     "similarity_score": score
#                 }
#             }
        

#     # ---------------------------------------------
#     # STEP 1: Preprocess
#     # ---------------------------------------------

#     fluency_data = fluency_preprocess(global_data)

#     y = fluency_data["waveform"]
#     sr = fluency_data["sample_rate"]

#     # ---------------------------------------------
#     # STEP 2: Segmentation + pauses
#     # ---------------------------------------------

#     seg = segmentation_pipeline(y, sr)

#     intervals = seg["intervals"]
#     pause_count = seg["pause_count"]
#     max_pause = seg["max_pause"]

#     # ---------------------------------------------
#     # STEP 3: Repetition
#     # ---------------------------------------------

#     rep = detect_repetition(y, sr, intervals)

#     repetition_count = rep["repetition_count"]

#     # ---------------------------------------------
#     # STEP 4: Prolongation
#     # ---------------------------------------------

#     prol = detect_prolongation(y, sr, intervals)

#     prolongation_count = prol["prolongation_count"]

#     # ---------------------------------------------
#     # STEP 5: Decision
#     # ---------------------------------------------

#     decision = fluency_decision(
#         repetition_count=repetition_count,
#         pause_count=pause_count,
#         max_pause=max_pause,
#         prolongation_count=prolongation_count
#     )

#     # ---------------------------------------------
#     # FINAL OUTPUT
#     # ---------------------------------------------

#     return {

#     "mode": "fluency",

#     "accuracy": decision["fluency_score"],

#     "performance": {

#         "stuttering_type": decision["stuttering_type"],
#         "severity": decision["severity"]
#     },

#     "details": {
#         "recognized_text": recognized_text if target_text else None,
#         "repetition_count": repetition_count,
#         "pause_count": pause_count,
#         "max_pause": max_pause,
#         "prolongation_count": prolongation_count
#     },

#     "error_type": None
# }
    