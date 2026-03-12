"""
Isolation Engine (Acoustic Version)
Evaluates articulation of a single phoneme spoken in isolation using pure DSP.
"""
# This version bypasses ASR and phoneme conversion, directly analyzing the audio signal for acoustic features.
from app.services.articulation.acoustic_isolation_detector import extract_features, detect_fricative, detect_stop, detect_liquid

def detect_isolation(y, sr, target_letter):
    
    if len(target_letter) != 1:
        return {
            "accuracy": 0,
            "error_type": "invalid_target_letter",
            "message": "Isolation level requires a single letter"
        }

    # 1. استخراج الخصائص الصوتية للإشارة (DSP)
    features = extract_features(y, sr)
    score = 0.0

    # 2. توجيه الحرف للمعادلة الفيزيائية الخاصة بيه
    if target_letter in ["س", "ص"]:
        # السين والصاد حروف احتكاكية ترددها عالي جداً
        score = detect_fricative(features, 4000, 8000) * 10

    elif target_letter in ["ش"]:
        # الشين حرف احتكاكي تردده متوسط
        score = detect_fricative(features, 3000, 7000) * 10

    elif target_letter in ["ف"]:
        score = detect_fricative(features, 2500, 6000) * 10

    elif target_letter in ["ك", "ق"]:
        score = detect_stop(features)

    elif target_letter in ["ر", "ل"]:
        score = detect_liquid(features)

    else:
        return {
            "accuracy": 0,
            "error_type": "unsupported_letter",
            "message": "هذا الحرف غير مدعوم في مستوى العزل حالياً"
        }

    # 3. حساب النسبة المئوية
    accuracy = min(int(score * 100), 100)
    
    # تحسين بسيط عشان لو الصوت واطي ميديناش صفر
    if accuracy > 0 and accuracy < 30:
        accuracy += 20 

    # 4. بناء النتيجة بنفس شكل الـ Word والـ Sentence
    if accuracy >= 60:
        error_type = None
    else:
        error_type = "isolation_failed"

    return {
        "accuracy": accuracy,
        "error_type": error_type,
        "expected_phoneme": target_letter,
        "spoken_phoneme": target_letter if accuracy >= 60 else None,
        "confusion_type": None
    }









# """
# Isolation Engine (Final Version)

# Evaluates articulation of a single phoneme spoken in isolation.

# Pipeline

# 1) audio → ASR
# 2) ASR text → phoneme sequence
# 3) extract dominant phoneme
# 4) compare with expected phoneme
# """

# from app.services.asr.asr_engine import transcribe_audio
# from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# from app.services.phoneme.phoneme_confusions import detect_confusion


# # ---------------------------------------------------------
# # Isolation articulation detection
# # ---------------------------------------------------------

# def detect_isolation(y, sr, target_letter):
    
#     if len(target_letter) != 1:

#         return {

#             "accuracy": None,

#             "error_type": "invalid_target_letter",

#             "message": "Isolation level requires a single letter"
#         }
#     # -----------------------------------------------------
#     # Step 1
#     # speech → text
#     # -----------------------------------------------------

#     recognized_text = transcribe_audio(y, sr)

#     if not recognized_text:

#         return {
#             "accuracy": 0,
#             "error_type": "no_speech_detected",
#             "expected_phoneme": None,
#             "spoken_phoneme": None
#         }

#     # -----------------------------------------------------
#     # Step 2
#     # convert target letter → phoneme
#     # -----------------------------------------------------

#     target_seq = arabic_to_phoneme_sequence(target_letter)

#     if not target_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "conversion_error",
#             "expected_phoneme": None,
#             "spoken_phoneme": None
#         }

#     expected_phoneme = target_seq[0]

#     # -----------------------------------------------------
#     # Step 3
#     # convert spoken text → phonemes
#     # -----------------------------------------------------

#     spoken_seq = arabic_to_phoneme_sequence(recognized_text)

#     if not spoken_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "phoneme_conversion_error",
#             "expected_phoneme": expected_phoneme,
#             "spoken_phoneme": None
#         }

#     # -----------------------------------------------------
#     # Step 4
#     # dominant phoneme detection
#     # -----------------------------------------------------

#     spoken_phoneme = spoken_seq[0]

#     # -----------------------------------------------------
#     # Step 5
#     # comparison
#     # -----------------------------------------------------

#     if spoken_phoneme == expected_phoneme:

#         return {
#             "accuracy": 100,
#             "error_type": None,
#             "expected_phoneme": expected_phoneme,
#             "spoken_phoneme": spoken_phoneme,
#             "confusion_type": None
#         }

#     confusion = detect_confusion(expected_phoneme, spoken_phoneme)

#     return {
#         "accuracy": 0,
#         "error_type": "substitution",
#         "expected_phoneme": expected_phoneme,
#         "spoken_phoneme": spoken_phoneme,
#         "confusion_type": confusion
#     }

