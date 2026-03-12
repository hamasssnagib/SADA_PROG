"""
Sentence-Level Articulation Engine (Smart Version)

Pipeline:

1) audio → ASR
2) clean recognized text
3) detect closest word in sentence
4) validate spoken word
5) convert words → phoneme sequences
6) detect articulation errors
"""

from difflib import SequenceMatcher

from app.services.asr.asr_engine import transcribe_audio

from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
from app.services.phoneme.phoneme_detector import detect_phoneme_errors

from app.services.text.text_cleaner import clean_arabic_text
from app.services.text.word_validator import validate_spoken_word
from app.services.exercise_validation.exercise_validator import validate_exercise

# ---------------------------------------------------------
# similarity between words
# ---------------------------------------------------------

def similarity(a, b):

    return SequenceMatcher(None, a, b).ratio()


# ---------------------------------------------------------
# find closest word in spoken sentence
# ---------------------------------------------------------

def find_target_word(spoken_sentence, target_word):

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
    #validate backend input if the target word and letter are correctly configured
    valid, error = validate_exercise(target_word, target_letter)

    if not valid:

        return {

            "accuracy": None,

            "error_type": error["error_type"],

            "message": error["message"],

            "target_word": error["target_word"],
            "target_letter": error["target_letter"]
        }
    # -----------------------------------------------------
    # Step 1
    # speech → text
    # -----------------------------------------------------

    recognized_sentence = transcribe_audio(y, sr)

    if not recognized_sentence:

        return {

            "accuracy": 0,

            "error_type": "no_speech_detected",

            "recognized_sentence": None
        }

    # -----------------------------------------------------
    # Step 2
    # clean text
    # -----------------------------------------------------

    recognized_sentence = clean_arabic_text(recognized_sentence)
    target_word = clean_arabic_text(target_word)

    # -----------------------------------------------------
    # Step 3
    # find closest word
    # -----------------------------------------------------

    best_word, score = find_target_word(

        recognized_sentence,
        target_word
    )

    if not best_word:

        return {

            "accuracy": 0,

            "error_type": "target_word_not_found",

            "recognized_sentence": recognized_sentence
        }

    # -----------------------------------------------------
    # Step 4
    # validate spoken word
    # -----------------------------------------------------

    valid, val_score, best_word = validate_spoken_word(

        best_word,
        target_word,
        target_letter
    )

    if not valid:

        return {

            "accuracy": 0,

            "error_type": "wrong_word_spoken",

            "recognized_sentence": recognized_sentence,

            "detected_word": best_word,

            "similarity_score": val_score
        }

    # -----------------------------------------------------
    # Step 5
    # phoneme conversion
    # -----------------------------------------------------

    expected_seq = arabic_to_phoneme_sequence(target_word)
    spoken_seq = arabic_to_phoneme_sequence(best_word)

    if not expected_seq or not spoken_seq:

        return {

            "accuracy": 0,

            "error_type": "phoneme_conversion_error",

            "recognized_sentence": recognized_sentence
        }

    # -----------------------------------------------------
    # Step 6
    # target phoneme
    # -----------------------------------------------------

    letter_seq = arabic_to_phoneme_sequence(target_letter)

    if not letter_seq:

        return {

            "accuracy": 0,

            "error_type": "target_letter_error",

            "recognized_sentence": recognized_sentence
        }

    target_phoneme = letter_seq[0]

    # -----------------------------------------------------
    # Step 7
    # phoneme detection
    # -----------------------------------------------------

    detection = detect_phoneme_errors(

        expected_seq,
        spoken_seq,
        target_phoneme
    )

    # -----------------------------------------------------
    # Step 8
    # return result
    # -----------------------------------------------------

    return {

        "recognized_sentence": recognized_sentence,

        "detected_word": best_word,

        "expected_phonemes": expected_seq,
        "spoken_phonemes": spoken_seq,

        "target_phoneme": target_phoneme,

        "target_positions": detection["target_positions"],

        "errors": detection["errors"],

        "accuracy": detection["accuracy"],

        "word_correct": detection["word_correct"]
    }






# """
# Sentence-Level Articulation Engine (Final Version)

# Pipeline:

# 1) audio → ASR
# 2) clean recognized text
# 3) detect closest word in sentence
# 4) convert words → phoneme sequences
# 5) detect articulation errors using phoneme_detector
# """

# from difflib import SequenceMatcher

# from app.services.asr.asr_engine import transcribe_audio
# from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# from app.services.phoneme.phoneme_detector import detect_phoneme_errors
# from app.services.text.text_cleaner import clean_arabic_text


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

#     # -----------------------------------------------------
#     # Step 1
#     # speech → text
#     # -----------------------------------------------------

#     recognized_sentence = transcribe_audio(y, sr)

#     if not recognized_sentence:

#         return {
#             "accuracy": 0,
#             "error_type": "no_speech_detected",
#             "recognized_sentence": None
#         }

#     # -----------------------------------------------------
#     # Step 2
#     # clean text
#     # -----------------------------------------------------

#     recognized_sentence = clean_arabic_text(recognized_sentence)
#     target_word = clean_arabic_text(target_word)

#     # -----------------------------------------------------
#     # Step 3
#     # find closest word
#     # -----------------------------------------------------

#     best_word, score = find_target_word(
#         recognized_sentence,
#         target_word
#     )

#     if score < 0.45:

#         return {
#             "accuracy": 0,
#             "error_type": "target_word_not_found",
#             "recognized_sentence": recognized_sentence
#         }

#     # -----------------------------------------------------
#     # Step 4
#     # phoneme conversion
#     # -----------------------------------------------------

#     expected_seq = arabic_to_phoneme_sequence(target_word)

#     spoken_seq = arabic_to_phoneme_sequence(best_word)

#     if not expected_seq or not spoken_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "phoneme_conversion_error",
#             "recognized_sentence": recognized_sentence
#         }

#     # -----------------------------------------------------
#     # Step 5
#     # target phoneme
#     # -----------------------------------------------------

#     letter_seq = arabic_to_phoneme_sequence(target_letter)

#     if not letter_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "target_letter_error",
#             "recognized_sentence": recognized_sentence
#         }

#     target_phoneme = letter_seq[0]

#     # -----------------------------------------------------
#     # Step 6
#     # phoneme detection
#     # -----------------------------------------------------

#     detection = detect_phoneme_errors(
#         expected_seq,
#         spoken_seq,
#         target_phoneme
#     )

#     # -----------------------------------------------------
#     # Step 7
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

#         "accuracy": detection["accuracy"]
#     }




# """
# Sentence-Level Articulation Engine (Final Version)

# Pipeline:

# 1) audio → ASR
# 2) detect closest word in sentence
# 3) convert words → phoneme sequences
# 4) detect articulation errors using phoneme_detector
# """

# from difflib import SequenceMatcher

# from app.services.asr.asr_engine import transcribe_audio
# from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# from app.services.phoneme.phoneme_detector import detect_phoneme_errors
# from app.services.text.text_cleaner import clean_arabic_text


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

#     # -----------------------------------------------------
#     # Step 1
#     # speech → text
#     # -----------------------------------------------------

#     recognized_sentence = transcribe_audio(y, sr)

#     if not recognized_sentence:

#         return {
#             "accuracy": 0,
#             "error_type": "no_speech_detected",
#             "recognized_sentence": None
#         }

#     # -----------------------------------------------------
#     # Step 2
#     # find closest word
#     # -----------------------------------------------------

#     best_word, score = find_target_word(
#         recognized_sentence,
#         target_word
#     )

#     if score < 0.45:

#         return {
#             "accuracy": 0,
#             "error_type": "target_word_not_found",
#             "recognized_sentence": recognized_sentence
#         }

#     # -----------------------------------------------------
#     # Step 3
#     # phoneme conversion
#     # -----------------------------------------------------

#     expected_seq = arabic_to_phoneme_sequence(target_word)

#     spoken_seq = arabic_to_phoneme_sequence(best_word)

#     if not expected_seq or not spoken_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "phoneme_conversion_error",
#             "recognized_sentence": recognized_sentence
#         }

#     # -----------------------------------------------------
#     # Step 4
#     # target phoneme
#     # -----------------------------------------------------

#     letter_seq = arabic_to_phoneme_sequence(target_letter)

#     if not letter_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "target_letter_error",
#             "recognized_sentence": recognized_sentence
#         }

#     target_phoneme = letter_seq[0]

#     # -----------------------------------------------------
#     # Step 5
#     # phoneme detection
#     # -----------------------------------------------------

#     detection = detect_phoneme_errors(
#         expected_seq,
#         spoken_seq,
#         target_phoneme
#     )

#     # -----------------------------------------------------
#     # Step 6
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

#         "accuracy": detection["accuracy"]
#     }











# """
# Sentence-Level Articulation Engine (Robust)

# Pipeline:

# 1) Whisper transcription
# 2) Fuzzy detection of target word
# 3) Convert target word → phoneme sequence
# 4) Extract phoneme stream
# 5) Normalize phoneme stream
# 6) Detect phoneme using context detector
# 7) Classify articulation error
# """

# import uuid
# import os
# import soundfile as sf
# from difflib import SequenceMatcher

# from app.models_loader import whisper_model, allosaurus_model

# from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# from app.services.phoneme.phoneme_detector import evaluate_phoneme_alignment, normalize_stream
# from app.services.phoneme.phoneme_confusions import detect_confusion


# # ---------------------------------------------------------
# # Whisper transcription
# # ---------------------------------------------------------

# def transcribe_audio(y, sr):

#     temp_file = f"temp_{uuid.uuid4().hex}.wav"
#     sf.write(temp_file, y, sr)

#     try:

#         segments, _ = whisper_model.transcribe(
#             temp_file,
#             language="ar"
#         )

#         text = " ".join([seg.text for seg in segments])

#         return text.strip()

#     finally:

#         if os.path.exists(temp_file):
#             os.remove(temp_file)


# # ---------------------------------------------------------
# # Phoneme stream extraction
# # ---------------------------------------------------------

# def infer_phoneme_stream(y, sr):

#     temp_file = f"temp_{uuid.uuid4().hex}.wav"
#     sf.write(temp_file, y, sr)

#     try:

#         result = allosaurus_model.recognize(temp_file)

#         return result.strip().split()

#     finally:

#         if os.path.exists(temp_file):
#             os.remove(temp_file)


# # ---------------------------------------------------------
# # Similarity between words
# # ---------------------------------------------------------

# def similarity(a, b):

#     return SequenceMatcher(None, a, b).ratio()


# # ---------------------------------------------------------
# # Find closest word in sentence
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
# # Convert Arabic right index
# # ---------------------------------------------------------

# def convert_index_from_right(word, index_from_right):

#     return len(word) - 1 - index_from_right


# # ---------------------------------------------------------
# # Main sentence articulation
# # ---------------------------------------------------------

# def detect_sentence_level(
#     y,
#     sr,
#     target_sentence,
#     target_word,
#     index_from_right
# ):

#     # -----------------------------------------------------
#     # Step 1: transcription
#     # -----------------------------------------------------

#     spoken_sentence = transcribe_audio(y, sr)

#     if not spoken_sentence:

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": None,
#             "spoken_phoneme": None,
#             "confusion_type": None
#         }

#     # -----------------------------------------------------
#     # Step 2: fuzzy word detection
#     # -----------------------------------------------------

#     best_word, score = find_target_word(
#         spoken_sentence,
#         target_word
#     )

#     if score < 0.45:

#         return {
#             "accuracy": 0,
#             "error_type": "target_word_not_found",
#             "expected_phoneme": None,
#             "spoken_phoneme": None,
#             "confusion_type": None
#         }

#     # -----------------------------------------------------
#     # Step 3: phoneme sequence
#     # -----------------------------------------------------

#     target_seq = arabic_to_phoneme_sequence(target_word)

#     if not target_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "conversion_error",
#             "expected_phoneme": None,
#             "spoken_phoneme": None,
#             "confusion_type": None
#         }

#     # -----------------------------------------------------
#     # Step 4: convert index
#     # -----------------------------------------------------

#     target_index = convert_index_from_right(
#         target_word,
#         index_from_right
#     )

#     if target_index < 0 or target_index >= len(target_seq):

#         return {
#             "accuracy": 0,
#             "error_type": "index_error",
#             "expected_phoneme": None,
#             "spoken_phoneme": None,
#             "confusion_type": None
#         }

#     # -----------------------------------------------------
#     # Step 5: phoneme stream
#     # -----------------------------------------------------

#     phoneme_stream = infer_phoneme_stream(y, sr)

#     if not phoneme_stream:

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": None,
#             "spoken_phoneme": None,
#             "confusion_type": None
#         }

#     phoneme_stream = normalize_stream(phoneme_stream)

#     # -----------------------------------------------------
#     # Step 6: alignment
#     # -----------------------------------------------------

#     alignment = evaluate_phoneme_alignment(
#         phoneme_stream,
#         target_seq,
#         target_index
#     )

#     if alignment["status"] == "no_attempt":

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": None,
#             "spoken_phoneme": None,
#             "confusion_type": None
#         }

#     expected = alignment["expected_phoneme"]
#     spoken = alignment["spoken_phoneme"]
#     error_type = alignment["error_type"]

#     score = alignment["score"]

#     accuracy = int(score * 100)

#     if error_type == "substitution":

#         accuracy = min(accuracy, 30)

#     elif error_type == "omission":

#         accuracy = 0

#     elif error_type is None and accuracy < 80:

#         error_type = "distortion"

#     confusion = detect_confusion(expected, spoken)

#     return {
#         "accuracy": accuracy,
#         "error_type": error_type,
#         "expected_phoneme": expected,
#         "spoken_phoneme": spoken,
#         "confusion_type": confusion
#     }









# """
# Sentence-Level Articulation Engine

# Pipeline:

# 1) Whisper transcription (context only)
# 2) Find target word using fuzzy matching
# 3) Convert target word → phoneme sequence
# 4) Extract phoneme stream from audio
# 5) Align phoneme sequence inside stream
# 6) Compare expected vs spoken phoneme
# """

# import uuid
# import os
# import soundfile as sf
# from difflib import SequenceMatcher

# from app.models_loader import whisper_model, allosaurus_model

# from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# from app.services.phoneme.phoneme_detector import evaluate_phoneme_alignment
# from app.services.phoneme.phoneme_confusions import detect_confusion

# # ---------------------------------------------------------
# # Whisper transcription
# # ---------------------------------------------------------

# def transcribe_audio(y, sr):

#     temp_file = f"temp_{uuid.uuid4().hex}.wav"
#     sf.write(temp_file, y, sr)

#     try:

#         segments, _ = whisper_model.transcribe(
#             temp_file,
#             language="ar"
#         )

#         text = " ".join([seg.text for seg in segments])

#         return text

#     finally:

#         if os.path.exists(temp_file):
#             os.remove(temp_file)


# # ---------------------------------------------------------
# # Phoneme stream extraction
# # ---------------------------------------------------------

# def infer_phoneme_stream(y, sr):

#     temp_file = f"temp_{uuid.uuid4().hex}.wav"
#     sf.write(temp_file, y, sr)

#     try:

#         result = allosaurus_model.recognize(temp_file)

#         return result.strip().split()

#     finally:

#         if os.path.exists(temp_file):
#             os.remove(temp_file)


# # ---------------------------------------------------------
# # Similarity between words
# # ---------------------------------------------------------

# def similarity(a, b):

#     return SequenceMatcher(None, a, b).ratio()


# # ---------------------------------------------------------
# # Find closest word in sentence
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
# # Convert Arabic right index
# # ---------------------------------------------------------

# def convert_index_from_right(word, index_from_right):

#     return len(word) - 1 - index_from_right


# # ---------------------------------------------------------
# # Main sentence articulation
# # ---------------------------------------------------------

# def detect_sentence_level(
#     y,
#     sr,
#     target_sentence,
#     target_word,
#     index_from_right
# ):

#     # -----------------------------------------------------
#     # Step 1: transcription
#     # -----------------------------------------------------

#     spoken_sentence = transcribe_audio(y, sr)

#     if not spoken_sentence:

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": None,
#             "spoken_phoneme": None
#         }

#     # -----------------------------------------------------
#     # Step 2: fuzzy word detection
#     # -----------------------------------------------------

#     best_word, score = find_target_word(
#         spoken_sentence,
#         target_word
#     )

#     if score < 0.4:

#         return {
#             "accuracy": 0,
#             "error_type": "target_word_not_found",
#             "expected_phoneme": None,
#             "spoken_phoneme": None
#         }

#     # -----------------------------------------------------
#     # Step 3: phoneme sequence
#     # -----------------------------------------------------

#     target_seq = arabic_to_phoneme_sequence(target_word)

#     if not target_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "conversion_error",
#             "expected_phoneme": None,
#             "spoken_phoneme": None
#         }

#     # -----------------------------------------------------
#     # Step 4: convert index
#     # -----------------------------------------------------

#     target_index = convert_index_from_right(
#         target_word,
#         index_from_right
#     )

#     if target_index < 0 or target_index >= len(target_seq):

#         return {
#             "accuracy": 0,
#             "error_type": "index_error",
#             "expected_phoneme": None,
#             "spoken_phoneme": None
#         }

#     # -----------------------------------------------------
#     # Step 5: phoneme stream
#     # -----------------------------------------------------

#     phoneme_stream = infer_phoneme_stream(y, sr)

#     if not phoneme_stream:

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": None,
#             "spoken_phoneme": None
#         }

#     # -----------------------------------------------------
#     # Step 6: alignment
#     # -----------------------------------------------------

#     alignment = evaluate_phoneme_alignment(
#         phoneme_stream,
#         target_seq,
#         target_index
#     )

#     if alignment["status"] == "no_attempt":

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": None,
#             "spoken_phoneme": None
#         }

#     expected = alignment["expected_phoneme"]
#     spoken = alignment["spoken_phoneme"]
#     error_type = alignment["error_type"]

#     score = alignment["score"]

#     accuracy = int(score * 100)

#     if error_type == "substitution":

#         accuracy = min(accuracy, 30)

#     elif error_type == "omission":

#         accuracy = 0

#     elif error_type is None and accuracy < 80:

#         error_type = "distortion"

#     return {
#         "accuracy": accuracy,
#         "error_type": error_type,
#         "expected_phoneme": expected,
#         "spoken_phoneme": spoken
#     }
    
    
    
    
    
    
    
    
    
#     # """
# # Sentence-Level Articulation Engine (Production Version)

# # Handles:
# # - no_attempt
# # - substitution
# # - omission
# # - distortion
# # - success
# # """

# # import uuid
# # import os
# # import soundfile as sf
# # from difflib import SequenceMatcher

# # from app.models_loader import whisper_model, allosaurus_model
# # from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# # from app.services.phoneme.alignment_engine import find_best_alignment
# # from app.services.articulation.isolation_engine import spectral_validation


# # # ---------------------------------------------------------
# # # Helper: similarity ratio
# # # ---------------------------------------------------------

# # def similarity(a, b):
# #     return SequenceMatcher(None, a, b).ratio()


# # # ---------------------------------------------------------
# # # Whisper transcription
# # # ---------------------------------------------------------

# # def transcribe_audio(y, sr):

# #     temp_file = f"temp_{uuid.uuid4().hex}.wav"
# #     sf.write(temp_file, y, sr)

# #     try:
# #         segments, _ = whisper_model.transcribe(temp_file, language="ar")
# #         return " ".join([seg.text for seg in segments])
# #     finally:
# #         if os.path.exists(temp_file):
# #             os.remove(temp_file)


# # # ---------------------------------------------------------
# # # Allosaurus phoneme stream
# # # ---------------------------------------------------------

# # def infer_full_phoneme_stream(y, sr):

# #     temp_file = f"temp_{uuid.uuid4().hex}.wav"
# #     sf.write(temp_file, y, sr)

# #     try:
# #         result = allosaurus_model.recognize(temp_file)
# #         return result.strip().split()
# #     finally:
# #         if os.path.exists(temp_file):
# #             os.remove(temp_file)


# # # ---------------------------------------------------------
# # # Main Sentence-Level Detection
# # # ---------------------------------------------------------

# # def detect_sentence_level(y, sr,
# #                           target_sentence,
# #                           target_word,
# #                           index_from_right):

# #     # -----------------------------------------------------
# #     # Step 1: Whisper sentence transcription
# #     # -----------------------------------------------------

# #     whisper_text = transcribe_audio(y, sr)
# #     spoken_words = whisper_text.split()

# #     # -----------------------------------------------------
# #     # Step 2: Fuzzy search for target word
# #     # -----------------------------------------------------

# #     best_score = 0

# #     for word in spoken_words:
# #         score = similarity(word, target_word)
# #         if score > best_score:
# #             best_score = score

# #     if best_score < 0.5:
# #         return {
# #             "accuracy": 0,
# #             "error_type": "no_attempt",
# #             "expected_phoneme": None,
# #             "spoken_phoneme": None
# #         }

# #     # -----------------------------------------------------
# #     # Step 3: Convert target word → phoneme sequence
# #     # -----------------------------------------------------

# #     target_seq = arabic_to_phoneme_sequence(target_word)

# #     if not target_seq:
# #         return {
# #             "accuracy": 0,
# #             "error_type": "conversion_error",
# #             "expected_phoneme": None,
# #             "spoken_phoneme": None
# #         }

# #     # -----------------------------------------------------
# #     # Step 4: Extract full phoneme stream
# #     # -----------------------------------------------------

# #     full_stream = infer_full_phoneme_stream(y, sr)

# #     if not full_stream:
# #         return {
# #             "accuracy": 0,
# #             "error_type": "no_attempt",
# #             "expected_phoneme": None,
# #             "spoken_phoneme": None
# #         }

# #     # -----------------------------------------------------
# #     # Step 5: Alignment
# #     # -----------------------------------------------------

# #     start_index, score, window = find_best_alignment(
# #         full_stream,
# #         target_seq
# #     )

# #     if score < 0.5:
# #         return {
# #             "accuracy": 0,
# #             "error_type": "no_attempt",
# #             "expected_phoneme": None,
# #             "spoken_phoneme": None
# #         }

# #     # -----------------------------------------------------
# #     # Step 6: Convert right-based index using PHONEME length
# #     # -----------------------------------------------------

# #     index_from_left = len(target_seq) - 1 - index_from_right

# #     if index_from_left < 0 or index_from_left >= len(target_seq):
# #         return {
# #             "accuracy": 0,
# #             "error_type": "index_error",
# #             "expected_phoneme": None,
# #             "spoken_phoneme": None
# #         }

# #     expected_phoneme = target_seq[index_from_left]

# #     # Handle omission safely
# #     if index_from_left >= len(window):
# #         return {
# #             "accuracy": 0,
# #             "error_type": "omission",
# #             "expected_phoneme": expected_phoneme,
# #             "spoken_phoneme": None
# #         }

# #     spoken_phoneme = window[index_from_left]

# #     # -----------------------------------------------------
# #     # Step 7: Substitution
# #     # -----------------------------------------------------

# #     if spoken_phoneme != expected_phoneme:
# #         return {
# #             "accuracy": 0,
# #             "error_type": "substitution",
# #             "expected_phoneme": expected_phoneme,
# #             "spoken_phoneme": spoken_phoneme
# #         }

# #     # -----------------------------------------------------
# #     # Step 8: Distortion (acoustic check)
# #     # -----------------------------------------------------

# #     if not spectral_validation(y, sr, expected_phoneme):
# #         return {
# #             "accuracy": 70,
# #             "error_type": "distortion",
# #             "expected_phoneme": expected_phoneme,
# #             "spoken_phoneme": spoken_phoneme
# #         }

# #     # -----------------------------------------------------
# #     # Success
# #     # -----------------------------------------------------

# #     return {
# #         "accuracy": 100,
# #         "error_type": None,
# #         "expected_phoneme": expected_phoneme,
# #         "spoken_phoneme": spoken_phoneme
# #     }





# # # """
# # # Sentence-Level Articulation Engine

# # # Pipeline:

# # # 1) Transcribe full sentence using Whisper
# # # 2) Detect target word inside sentence (fuzzy match)
# # # 3) If target word not detected → no_attempt
# # # 4) If detected → run phoneme-level alignment
# # # 5) Extract target phoneme using right-based index
# # # 6) Compare expected vs spoken
# # # 7) Validate acoustically
# # # """

# # # import uuid
# # # import os
# # # import soundfile as sf
# # # from difflib import SequenceMatcher

# # # from app.models_loader import whisper_model, allosaurus_model
# # # from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# # # from app.services.phoneme.alignment_engine import find_best_alignment
# # # from app.services.articulation.isolation_engine import spectral_validation


# # # # ---------------------------------------------------------
# # # # Helper: Text Similarity
# # # # Used for fuzzy word matching inside sentence
# # # # ---------------------------------------------------------
# # # def similarity(a, b):
# # #     return SequenceMatcher(None, a, b).ratio()


# # # # ---------------------------------------------------------
# # # # Step 1: Whisper Transcription
# # # # ---------------------------------------------------------
# # # def transcribe_audio(y, sr):

# # #     temp_file = f"temp_{uuid.uuid4().hex}.wav"
# # #     sf.write(temp_file, y, sr)

# # #     try:
# # #         segments, _ = whisper_model.transcribe(temp_file, language="ar")
# # #         text = " ".join([seg.text for seg in segments])
# # #         return text
# # #     finally:
# # #         if os.path.exists(temp_file):
# # #             os.remove(temp_file)


# # # # ---------------------------------------------------------
# # # # Step 2: Extract phoneme stream from audio
# # # # ---------------------------------------------------------
# # # def infer_full_phoneme_stream(y, sr):

# # #     temp_file = f"temp_{uuid.uuid4().hex}.wav"
# # #     sf.write(temp_file, y, sr)

# # #     try:
# # #         result = allosaurus_model.recognize(temp_file)
# # #         return result.strip().split()
# # #     finally:
# # #         if os.path.exists(temp_file):
# # #             os.remove(temp_file)


# # # # ---------------------------------------------------------
# # # # Main Sentence-Level Function
# # # # ---------------------------------------------------------
# # # def detect_sentence_level(y, sr, target_sentence,
# # #                           target_word,
# # #                           index_from_right):
# # #     """
# # #     Evaluates articulation inside a sentence context.

# # #     Parameters:
# # #         y : waveform
# # #         sr : sample rate
# # #         target_sentence : full sentence (reference)
# # #         target_word : word to evaluate
# # #         index_from_right : right-based letter index

# # #     Returns:
# # #         structured articulation result
# # #     """

# # #     # -----------------------------------------------------
# # #     # Transcribe full spoken sentence
# # #     # -----------------------------------------------------
# # #     whisper_text = transcribe_audio(y, sr)

# # #     spoken_words = whisper_text.split()

# # #     # -----------------------------------------------------
# # #     # Fuzzy search for target word inside spoken sentence
# # #     # -----------------------------------------------------
# # #     best_match = None
# # #     best_score = 0

# # #     for word in spoken_words:
# # #         score = similarity(word, target_word)
# # #         if score > best_score:
# # #             best_score = score
# # #             best_match = word

# # #     # If similarity too low → target word not spoken
# # #     if best_score < 0.5:
# # #         return {
# # #             "accuracy": 0,
# # #             "error_type": "no_attempt",
# # #             "expected_phoneme": None,
# # #             "spoken_phoneme": None
# # #         }

# # #     # -----------------------------------------------------
# # #     # Convert target word to phoneme sequence
# # #     # -----------------------------------------------------
# # #     target_seq = arabic_to_phoneme_sequence(target_word)

# # #     if not target_seq:
# # #         return {
# # #             "accuracy": 0,
# # #             "error_type": "conversion_error",
# # #             "expected_phoneme": None,
# # #             "spoken_phoneme": None
# # #         }

# # #     # -----------------------------------------------------
# # #     # Extract phoneme stream from audio
# # #     # -----------------------------------------------------
# # #     full_stream = infer_full_phoneme_stream(y, sr)

# # #     if not full_stream:
# # #         return {
# # #             "accuracy": 0,
# # #             "error_type": "no_attempt",
# # #             "expected_phoneme": None,
# # #             "spoken_phoneme": None
# # #         }

# # #     # -----------------------------------------------------
# # #     # Dynamic alignment
# # #     # -----------------------------------------------------
# # #     start_index, score, window = find_best_alignment(
# # #         full_stream,
# # #         target_seq
# # #     )

# # #     if score < 0.5:
# # #         return {
# # #             "accuracy": 0,
# # #             "error_type": "no_attempt",
# # #             "expected_phoneme": None,
# # #             "spoken_phoneme": None
# # #         }

# # #     # -----------------------------------------------------
# # #     # Convert Arabic right-based index
# # #     # -----------------------------------------------------
# # #     index_from_left = len(target_word) - 1 - index_from_right

# # #     if index_from_left < 0 or index_from_left >= len(target_seq):
# # #         return {
# # #             "accuracy": 0,
# # #             "error_type": "index_error",
# # #             "expected_phoneme": None,
# # #             "spoken_phoneme": None
# # #         }

# # #     expected_phoneme = target_seq[index_from_left]
# # #     spoken_phoneme = window[index_from_left]

# # #     # -----------------------------------------------------
# # #     # Compare phonemes
# # #     # -----------------------------------------------------
# # #     if spoken_phoneme != expected_phoneme:
# # #         return {
# # #             "accuracy": 0,
# # #             "error_type": "substitution",
# # #             "expected_phoneme": expected_phoneme,
# # #             "spoken_phoneme": spoken_phoneme
# # #         }

# # #     # -----------------------------------------------------
# # #     # Spectral validation
# # #     # -----------------------------------------------------
# # #     if not spectral_validation(y, sr, expected_phoneme):
# # #         return {
# # #             "accuracy": 70,
# # #             "error_type": "distortion",
# # #             "expected_phoneme": expected_phoneme,
# # #             "spoken_phoneme": spoken_phoneme
# # #         }

# # #     # -----------------------------------------------------
# # #     # Success
# # #     # -----------------------------------------------------
# # #     return {
# # #         "accuracy": 100,
# # #         "error_type": None,
# # #         "expected_phoneme": expected_phoneme,
# # #         "spoken_phoneme": spoken_phoneme
# # #     }