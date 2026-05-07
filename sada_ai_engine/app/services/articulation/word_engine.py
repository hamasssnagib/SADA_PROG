"""
Word-Level Articulation Engine
(Unified Production Version)
"""

from app.services.asr.asr_engine import transcribe_audio

from app.services.articulation.phoneme.phoneme_converter import (
    arabic_to_phoneme_sequence
)

from app.services.articulation.phoneme.phoneme_detector import (
    detect_phoneme_errors
)

from app.services.text.text_cleaner import clean_arabic_text

from app.services.validation.validation_engine import (
    validate_spoken_input
)

from app.services.validation.exercise_validator import (
    validate_exercise
)


def detect_word_level(

    y,
    sr,

    target_word,
    target_letter
):

    # -----------------------------------------------------
    # validate exercise config
    # -----------------------------------------------------

    valid, error = validate_exercise(
        target_word,
        target_letter
    )

    if not valid:

        return {

            "accuracy": 0,

            "exercise_correct": False,

            "recognized_text": None,

            "expected_phonemes": [],

            "spoken_phonemes": [],

            "target_phoneme": None,

            "target_positions": [],

            "errors": [],

            "original_text": target_word,

            "target_unit": target_word,

            "error_type": error["error_type"]
        }

    # -----------------------------------------------------
    # ASR
    # -----------------------------------------------------

    recognized_text = transcribe_audio(y, sr)

    if not recognized_text:

        return {

            "accuracy": 0,

            "exercise_correct": False,

            "recognized_text": None,

            "expected_phonemes": [],

            "spoken_phonemes": [],

            "target_phoneme": None,

            "target_positions": [],

            "errors": [],

            "original_text": target_word,

            "target_unit": target_word,

            "error_type": "no_speech_detected"
        }

    # -----------------------------------------------------
    # cleaning
    # -----------------------------------------------------

    recognized_text = clean_arabic_text(
        recognized_text
    )

    target_word = clean_arabic_text(
        target_word
    )

    target_letter = clean_arabic_text(
        target_letter
    )

    # -----------------------------------------------------
    # validation
    # -----------------------------------------------------

    valid, score, recognized_text = validate_spoken_input(

        recognized_text,
        target_word,
        target_letter,

        threshold=0.4
    )

    if not valid or score < 0.6:

        return {

            "accuracy": 0,

            "exercise_correct": False,

            "recognized_text": recognized_text,

            "expected_phonemes": [],

            "spoken_phonemes": [],

            "target_phoneme": None,

            "target_positions": [],

            "errors": [],

            "original_text": target_word,

            "target_unit": target_word,

            "similarity_score": score,

            "error_type": "wrong_word_spoken"
        }

    # -----------------------------------------------------
    # phoneme conversion
    # -----------------------------------------------------

    expected_seq = arabic_to_phoneme_sequence(
        target_word
    )

    spoken_seq = arabic_to_phoneme_sequence(
        recognized_text
    )

    if not expected_seq or not spoken_seq:

        return {

            "accuracy": 0,

            "exercise_correct": False,

            "recognized_text": recognized_text,

            "expected_phonemes": [],

            "spoken_phonemes": [],

            "target_phoneme": None,

            "target_positions": [],

            "errors": [],

            "original_text": target_word,

            "target_unit": target_word,

            "error_type": "phoneme_conversion_error"
        }

    # -----------------------------------------------------
    # target phoneme
    # -----------------------------------------------------

    letter_seq = arabic_to_phoneme_sequence(
        target_letter
    )

    if not letter_seq:

        return {

            "accuracy": 0,

            "exercise_correct": False,

            "recognized_text": recognized_text,

            "expected_phonemes": expected_seq,

            "spoken_phonemes": spoken_seq,

            "target_phoneme": None,

            "target_positions": [],

            "errors": [],

            "original_text": target_word,

            "target_unit": target_word,

            "error_type": "target_letter_error"
        }

    target_phoneme = letter_seq[0]

    # -----------------------------------------------------
    # phoneme detection
    # -----------------------------------------------------

    detection = detect_phoneme_errors(

        expected_seq,
        spoken_seq,
        target_phoneme
    )

    # -----------------------------------------------------
    # accuracy
    # -----------------------------------------------------

    has_error = any(

        e["error_type"] is not None

        for e in detection["errors"]
    )

    if has_error:

        accuracy = 50

    else:

        accuracy = 100

    # -----------------------------------------------------
    # final unified output
    # -----------------------------------------------------

    return {

        "accuracy": accuracy,

        "exercise_correct":
            accuracy == 100,

        "recognized_text":
            recognized_text,

        "expected_phonemes":
            expected_seq,

        "spoken_phonemes":
            spoken_seq,

        "target_phoneme":
            target_phoneme,

        "target_positions":
            detection["target_positions"],

        "errors":
            detection["errors"],

        "original_text":
            target_word,

        "target_unit":
            target_word,

        "similarity_score":
            score,

        "error_type": None
    }

# """
# Word-Level Articulation Engine (Final Fixed Version)
# """

# from app.services.asr.asr_engine import transcribe_audio

# from app.services.articulation.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# from app.services.articulation.phoneme.phoneme_detector import detect_phoneme_errors

# from app.services.text.text_cleaner import clean_arabic_text
# from app.services.validation.validation_engine import validate_spoken_input
# from app.services.validation.exercise_validator import validate_exercise


# def detect_word_level(
#     y,
#     sr,
#     target_word,
#     target_letter
# ):

#     # -----------------------------------------------------
#     # Step 0: validate exercise config
#     # -----------------------------------------------------
#     valid, error = validate_exercise(target_word, target_letter)

#     if not valid:
#         return {
#             "accuracy": None,
#             "error_type": error["error_type"],
#             "message": error["message"],
#             "details": {
#                 "target_word": error["target_word"],
#                 "target_letter": error["target_letter"]
#             }
#         }

#     # -----------------------------------------------------
#     # Step 1: ASR
#     # -----------------------------------------------------
#     recognized_text = transcribe_audio(y, sr)

#     if not recognized_text:
#         return {
#             "accuracy": 0,
#             "error_type": "no_speech_detected",
#             "details": {
#                 "recognized_text": None
#             }
#         }

#     # -----------------------------------------------------
#     # Step 2: cleaning
#     # -----------------------------------------------------
#     recognized_text = clean_arabic_text(recognized_text)
#     target_word = clean_arabic_text(target_word)
#     target_letter = clean_arabic_text(target_letter)

#     # -----------------------------------------------------
#     # Step 3: VALIDATION (👑 أهم تعديل هنا)
#     # -----------------------------------------------------
#     valid, score, recognized_text = validate_spoken_input(
#         recognized_text,
#         target_word,
#         target_letter,
#         threshold=0.4  # مرونة
#     )

#     # 👑 FIX 1: strict guard ضد الكلمات الغلط
#     if not valid or score < 0.6:
#         return {
#             "accuracy": 0,
#             "error_type": "wrong_word_spoken",
#             "details": {
#                 "recognized_text": recognized_text,
#                 "similarity_score": score
#             }
#         }

#     # -----------------------------------------------------
#     # Step 4: phoneme conversion
#     # -----------------------------------------------------
#     expected_seq = arabic_to_phoneme_sequence(target_word)
#     spoken_seq = arabic_to_phoneme_sequence(recognized_text)

#     if not expected_seq or not spoken_seq:
#         return {
#             "accuracy": 0,
#             "error_type": "phoneme_conversion_error",
#             "details": {
#                 "recognized_text": recognized_text
#             }
#         }

#     # -----------------------------------------------------
#     # Step 5: target phoneme
#     # -----------------------------------------------------
#     letter_seq = arabic_to_phoneme_sequence(target_letter)

#     if not letter_seq:
#         return {
#             "accuracy": 0,
#             "error_type": "target_letter_error",
#             "details": {
#                 "recognized_text": recognized_text
#             }
#         }

#     target_phoneme = letter_seq[0]

#     # -----------------------------------------------------
#     # Step 6: phoneme detection
#     # -----------------------------------------------------
#     detection = detect_phoneme_errors(
#         expected_seq,
#         spoken_seq,
#         target_phoneme
#     )

#     # -----------------------------------------------------
#     # Step 7: recompute accuracy (👑 مهم)
#     # -----------------------------------------------------
#     # total = len(detection["errors"])

#     # correct = sum(
#     #     1 for e in detection["errors"]
#     #     if e["error_type"] is None
#     # )

#     # accuracy = int((correct / total) * 100) if total > 0 else 0
#     # -----------------------------------------------------
#     # 🎯 Step 7: compute accuracy based on error_type
#     # -----------------------------------------------------

#     # لو فيه أي error → يبقى 50
#     has_error = any(e["error_type"] is not None for e in detection["errors"])

#     if has_error:
#         accuracy = 50
#     else:
#         accuracy = 100
#     # -----------------------------------------------------
#     # Step 8: final output
#     # -----------------------------------------------------
#     return {

#         "recognized_text": recognized_text,

#         "expected_phonemes": expected_seq,
#         "spoken_phonemes": spoken_seq,

#         "target_phoneme": target_phoneme,

#         "target_positions": detection["target_positions"],

#         "errors": detection["errors"],

#         "accuracy": accuracy,

#         "word_correct": accuracy == 100,

#         "error_type": None
#     }