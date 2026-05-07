"""
Sentence-Level Articulation Engine
(Unified Production Version)
"""

from difflib import SequenceMatcher

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


# ---------------------------------------------------------
# similarity helper
# ---------------------------------------------------------

def similarity(a, b):

    return SequenceMatcher(None, a, b).ratio()


# ---------------------------------------------------------
# find closest word
# ---------------------------------------------------------

def find_target_word(
    spoken_sentence,
    target_word
):

    words = spoken_sentence.split()

    best_word = None
    best_score = 0

    for w in words:

        score = similarity(w, target_word)

        if score > best_score:

            best_score = score
            best_word = w

    return best_word, best_score


# ---------------------------------------------------------
# sentence articulation detection
# ---------------------------------------------------------

def detect_sentence_level(

    y,
    sr,

    target_sentence,
    target_word,
    target_letter
):

    # -----------------------------------------------------
    # validate backend config
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

            "original_text": target_sentence,

            "target_unit": target_word,

            "error_type": error["error_type"]
        }

    # -----------------------------------------------------
    # ASR
    # -----------------------------------------------------

    recognized_sentence = transcribe_audio(y, sr)

    if not recognized_sentence:

        return {

            "accuracy": 0,

            "exercise_correct": False,

            "recognized_text": None,

            "expected_phonemes": [],

            "spoken_phonemes": [],

            "target_phoneme": None,

            "target_positions": [],

            "errors": [],

            "original_text": target_sentence,

            "target_unit": target_word,

            "error_type": "no_speech_detected"
        }

    # -----------------------------------------------------
    # cleaning
    # -----------------------------------------------------

    recognized_sentence = clean_arabic_text(
        recognized_sentence
    )

    target_sentence = clean_arabic_text(
        target_sentence
    )

    target_word = clean_arabic_text(
        target_word
    )

    target_letter = clean_arabic_text(
        target_letter
    )

    # -----------------------------------------------------
    # find closest word
    # -----------------------------------------------------

    best_word, score = find_target_word(

        recognized_sentence,
        target_word
    )

    if not best_word:

        return {

            "accuracy": 0,

            "exercise_correct": False,

            "recognized_text": recognized_sentence,

            "expected_phonemes": [],

            "spoken_phonemes": [],

            "target_phoneme": None,

            "target_positions": [],

            "errors": [],

            "original_text": target_sentence,

            "target_unit": target_word,

            "similarity_score": score,

            "error_type": "target_word_not_found"
        }

    # -----------------------------------------------------
    # validate detected word
    # -----------------------------------------------------

    valid, val_score, best_word = validate_spoken_input(

        best_word,
        target_word,
        target_letter,
        threshold=0.45
    )

    if not valid:

        return {

            "accuracy": 0,

            "exercise_correct": False,

            "recognized_text": recognized_sentence,

            "expected_phonemes": [],

            "spoken_phonemes": [],

            "target_phoneme": None,

            "target_positions": [],

            "errors": [],

            "original_text": target_sentence,

            "target_unit": target_word,

            "similarity_score": val_score,

            "error_type": "wrong_word_spoken"
        }

    # -----------------------------------------------------
    # phoneme conversion
    # -----------------------------------------------------

    expected_seq = arabic_to_phoneme_sequence(
        target_word
    )

    spoken_seq = arabic_to_phoneme_sequence(
        best_word
    )

    if not expected_seq or not spoken_seq:

        return {

            "accuracy": 0,

            "exercise_correct": False,

            "recognized_text": recognized_sentence,

            "expected_phonemes": [],

            "spoken_phonemes": [],

            "target_phoneme": None,

            "target_positions": [],

            "errors": [],

            "original_text": target_sentence,

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

            "recognized_text": recognized_sentence,

            "expected_phonemes": expected_seq,

            "spoken_phonemes": spoken_seq,

            "target_phoneme": None,

            "target_positions": [],

            "errors": [],

            "original_text": target_sentence,

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

    errors = detection["errors"]

    # -----------------------------------------------------
    # accuracy
    # -----------------------------------------------------

    if all(e["error_type"] is None for e in errors):

        final_accuracy = 100

    else:

        final_accuracy = 50

    # -----------------------------------------------------
    # final unified output
    # -----------------------------------------------------

    return {

        "accuracy": final_accuracy,

        "exercise_correct":
            final_accuracy == 100,

        "recognized_text":
            recognized_sentence,

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
            target_sentence,

        "target_unit":
            target_word,

        "similarity_score":
            val_score,

        "error_type": None
    }


# """
# Sentence-Level Articulation Engine (Smart Version)

# Pipeline:

# 1) audio → ASR
# 2) clean recognized text
# 3) detect closest word in sentence
# 4) validate spoken word
# 5) convert words → phoneme sequences
# 6) detect articulation errors
# """

# from difflib import SequenceMatcher

# from app.services.asr.asr_engine import transcribe_audio

# from app.services.articulation.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# from app.services.articulation.phoneme.phoneme_detector import detect_phoneme_errors

# from app.services.text.text_cleaner import clean_arabic_text
# from app.services.validation.validation_engine import validate_spoken_input
# from app.services.validation.exercise_validator import validate_exercise

# # ---------------------------------------------------------
# # similarity between words
# # ---------------------------------------------------------

# def similarity(a, b):

#     return SequenceMatcher(None, a, b).ratio()


# # ---------------------------------------------------------
# # find closest word in spoken sentence
# # ---------------------------------------------------------

# def find_target_word(spoken_sentence, target_word):

#     words = spoken_sentence.split()

#     best_word = None
#     best_score = 0

#     for w in words:

#         score = similarity(w, target_word)

#         if score > best_score:

#             best_score = score
#             best_word = w

#     return best_word, best_score


# # ---------------------------------------------------------
# # sentence articulation detection
# # ---------------------------------------------------------

# def detect_sentence_level(
#     y,
#     sr,
#     target_sentence,
#     target_word,
#     target_letter
# ):
    
#        #validate backend input if the target word and letter are correctly configured
#     valid, error = validate_exercise(target_word, target_letter)

#     if not valid:

#         return {

#             "accuracy": None,

#             "error_type": error["error_type"],

#             "message": error["message"],

#             "target_word": error["target_word"],
#             "target_letter": error["target_letter"]
#         }
#     # -----------------------------------------------------
#     # Step 1
#     # speech → text
#     # -----------------------------------------------------

#     recognized_sentence = transcribe_audio(y, sr)

#     if not recognized_sentence:

#         return {

#             "accuracy": 0,

#             "error_type": "no_speech_detected",
#                 "details": {

#                      "recognized_sentence": None
#         }
#                 }

#     # -----------------------------------------------------
#     # Step 2
#     # clean text
#     # -----------------------------------------------------

#     recognized_sentence = clean_arabic_text(recognized_sentence)
#     target_word = clean_arabic_text(target_word)
#     target_sentence = clean_arabic_text(target_sentence)

#     # -----------------------------------------------------
#     # Step 3
#     # find closest word
#     # -----------------------------------------------------

#     best_word, score = find_target_word(

#         recognized_sentence,
#         target_word
#     )

#     if not best_word:

#         return {

#             "accuracy": 0,

#             "error_type": "target_word_not_found",
#             "details": {

#                         "recognized_sentence": recognized_sentence
#         }
#             }

#     # -----------------------------------------------------
#     # Step 4
#     # validate spoken word
#     # -----------------------------------------------------

#     valid, val_score, best_word = validate_spoken_input(

#         best_word,
#         target_word,
#         target_letter,
#         threshold=0.45
#     )

#     # if not valid:

#     #     return {

#     #         "accuracy": 0,

#     #         "error_type": "wrong_word_spoken",

#     #         "recognized_sentence": recognized_sentence,

#     #         "detected_word": best_word,

#     #         "similarity_score": val_score
#     #     }
#     if not valid:

#             return {

#                 "accuracy": 0,

#                 "error_type": "wrong_word_spoken",

#                 "details": {
#                     "recognized_sentence": recognized_sentence,
#                     "detected_word": best_word,
#                     "similarity_score": val_score
#                 }
#             }

#     # -----------------------------------------------------
#     # Step 5
#     # phoneme conversion
#     # -----------------------------------------------------

#     expected_seq = arabic_to_phoneme_sequence(target_word)
#     spoken_seq = arabic_to_phoneme_sequence(best_word)

#     if not expected_seq or not spoken_seq:

#         return {

#             "accuracy": 0,

#             "error_type": "phoneme_conversion_error",
#             "details": {

#                   "recognized_sentence": recognized_sentence
#         }
#             }

#     # -----------------------------------------------------
#     # Step 6
#     # target phoneme
#     # -----------------------------------------------------

#     letter_seq = arabic_to_phoneme_sequence(target_letter)

#     if not letter_seq:

#         return {

#             "accuracy": 0,

#             "error_type": "target_letter_error",
#             "details": {
#                 "recognized_sentence": recognized_sentence,
               
#             }

           
#         }

#     target_phoneme = letter_seq[0]

#     # -----------------------------------------------------
#     # Step 7
#     # phoneme detection
#     # -----------------------------------------------------

#     detection = detect_phoneme_errors(

#         expected_seq,
#         spoken_seq,
#         target_phoneme
#     )



#     # -----------------------------------------------------
#     # 🎯 Step 8: compute accuracy from error types
#     # -----------------------------------------------------

#     errors = detection["errors"]

#     # لو كلهم None → 100
#     if all(e["error_type"] is None for e in errors):
#         final_accuracy = 100

#     # لو فيه أي error → 50
#     else:
#         final_accuracy = 50
    
#     # -----------------------------------------------------
#     # Step 8
#     # return result
#     # -----------------------------------------------------

#     return {

#         "recognized_sentence": recognized_sentence,

#         "detected_word": best_word,

#         "expected_phonemes": expected_seq,
#         "spoken_phonemes": spoken_seq,

#         "target_phoneme": target_phoneme,

#         "target_positions": detection["target_positions"],

#         "errors": detection["errors"],

#         "accuracy": final_accuracy,

#         "word_correct": final_accuracy == 100,
#         # "word_correct":detection.get("word_correct", False),
#         "error_type": None
#     }


