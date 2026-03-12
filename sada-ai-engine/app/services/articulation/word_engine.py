"""
Word-Level Articulation Engine (Smart Version)

Pipeline

1) audio → ASR
2) clean recognized text
3) validate spoken word (smart validator)
4) convert words → phoneme sequence
5) detect target phoneme errors
"""

from app.services.asr.asr_engine import transcribe_audio

from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
from app.services.phoneme.phoneme_detector import detect_phoneme_errors

from app.services.text.text_cleaner import clean_arabic_text
from app.services.text.word_validator import validate_spoken_word
from app.services.exercise_validation.exercise_validator import validate_exercise

# ---------------------------------------------------------
# Word articulation detection
# ---------------------------------------------------------

def detect_word_level(
    y,
    sr,
    target_word,
    target_letter
):


#validate backend input first if the target word and letter are valid for the exercise, if not return error without processing the audio
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

    recognized_text = transcribe_audio(y, sr)

    if not recognized_text:

        return {
            "accuracy": 0,
            "error_type": "no_speech_detected",
            "recognized_text": None
        }

    # -----------------------------------------------------
    # Step 2
    # clean text
    # -----------------------------------------------------

    recognized_text = clean_arabic_text(recognized_text)
    target_word = clean_arabic_text(target_word)

    # -----------------------------------------------------
    # Step 3
    # validate spoken word
    # -----------------------------------------------------

    valid, score, recognized_text = validate_spoken_word(

        recognized_text,
        target_word,
        target_letter
    )

    if not valid:

        return {

            "accuracy": 0,

            "error_type": "wrong_word_spoken",

            "recognized_text": recognized_text,

            "similarity_score": score
        }

    # -----------------------------------------------------
    # Step 4
    # phoneme conversion
    # -----------------------------------------------------

    expected_seq = arabic_to_phoneme_sequence(target_word)
    spoken_seq = arabic_to_phoneme_sequence(recognized_text)

    if not expected_seq or not spoken_seq:

        return {

            "accuracy": 0,

            "error_type": "phoneme_conversion_error",

            "recognized_text": recognized_text
        }

    # -----------------------------------------------------
    # Step 5
    # target phoneme
    # -----------------------------------------------------

    letter_seq = arabic_to_phoneme_sequence(target_letter)

    if not letter_seq:

        return {

            "accuracy": 0,

            "error_type": "target_letter_error",

            "recognized_text": recognized_text
        }

    target_phoneme = letter_seq[0]

    # -----------------------------------------------------
    # Step 6
    # detect phoneme errors
    # -----------------------------------------------------

    detection = detect_phoneme_errors(

        expected_seq,
        spoken_seq,
        target_phoneme
    )

    # -----------------------------------------------------
    # Step 7
    # return result
    # -----------------------------------------------------

    return {

        "recognized_text": recognized_text,

        "expected_phonemes": expected_seq,
        "spoken_phonemes": spoken_seq,

        "target_phoneme": target_phoneme,

        "target_positions": detection["target_positions"],

        "errors": detection["errors"],

        "accuracy": detection["accuracy"],

        "word_correct": detection["word_correct"]
    }






# """
# Word-Level Articulation Engine (Final Version)

# Pipeline

# 1) audio → ASR
# 2) clean recognized text
# 3) convert words → phoneme sequence
# 4) detect target phoneme errors
# 5) return articulation analysis
# """

# from app.services.asr.asr_engine import transcribe_audio
# from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# from app.services.phoneme.phoneme_detector import detect_phoneme_errors
# from app.services.text.text_cleaner import clean_arabic_text


# # ---------------------------------------------------------
# # Word articulation detection
# # ---------------------------------------------------------

# def detect_word_level(
#     y,
#     sr,
#     target_word,
#     target_letter
# ):

#     # -----------------------------------------------------
#     # Step 1
#     # speech → text
#     # -----------------------------------------------------

#     recognized_text = transcribe_audio(y, sr)

#     if not recognized_text:

#         return {
#             "accuracy": 0,
#             "error_type": "no_speech_detected",
#             "recognized_text": None
#         }

#     # -----------------------------------------------------
#     # Step 2
#     # clean text
#     # -----------------------------------------------------

#     recognized_text = clean_arabic_text(recognized_text)
#     target_word = clean_arabic_text(target_word)

#     # -----------------------------------------------------
#     # Step 3
#     # convert words → phonemes
#     # -----------------------------------------------------

#     expected_seq = arabic_to_phoneme_sequence(target_word)

#     spoken_seq = arabic_to_phoneme_sequence(recognized_text)

#     if not expected_seq or not spoken_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "phoneme_conversion_error",
#             "recognized_text": recognized_text
#         }

#     # -----------------------------------------------------
#     # Step 4
#     # convert target letter → phoneme
#     # -----------------------------------------------------

#     target_letter_seq = arabic_to_phoneme_sequence(target_letter)

#     if not target_letter_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "target_letter_error",
#             "recognized_text": recognized_text
#         }

#     target_phoneme = target_letter_seq[0]

#     # -----------------------------------------------------
#     # Step 5
#     # detect phoneme errors
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

#         "recognized_text": recognized_text,

#         "expected_phonemes": expected_seq,
#         "spoken_phonemes": spoken_seq,

#         "target_phoneme": target_phoneme,

#         "target_positions": detection["target_positions"],

#         "errors": detection["errors"],

#         "accuracy": detection["accuracy"]
#     }








# """
# Word-Level Articulation Engine (Final Version)

# Pipeline

# 1) audio → ASR
# 2) recognized text → phoneme sequence
# 3) target word → phoneme sequence
# 4) detect target phoneme errors
# 5) return articulation analysis
# """

# from app.services.asr.asr_engine import transcribe_audio
# from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# from app.services.phoneme.phoneme_detector import detect_phoneme_errors
# from app.services.text.text_cleaner import clean_arabic_text


# # ---------------------------------------------------------
# # Word articulation detection
# # ---------------------------------------------------------

# def detect_word_level(
#     y,
#     sr,
#     target_word,
#     target_letter
# ):

#     # -----------------------------------------------------
#     # Step 1
#     # speech → text
#     # -----------------------------------------------------

#     recognized_text = transcribe_audio(y, sr)

#     if not recognized_text:

#         return {
#             "accuracy": 0,
#             "error_type": "no_speech_detected",
#             "recognized_text": None
#         }

#     # -----------------------------------------------------
#     # Step 2
#     # convert words → phonemes
#     # -----------------------------------------------------

#     expected_seq = arabic_to_phoneme_sequence(target_word)

#     spoken_seq = arabic_to_phoneme_sequence(recognized_text)

#     if not expected_seq or not spoken_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "phoneme_conversion_error",
#             "recognized_text": recognized_text
#         }

#     # -----------------------------------------------------
#     # Step 3
#     # convert target letter → phoneme
#     # -----------------------------------------------------

#     target_letter_seq = arabic_to_phoneme_sequence(target_letter)

#     if not target_letter_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "target_letter_error",
#             "recognized_text": recognized_text
#         }

#     target_phoneme = target_letter_seq[0]

#     # -----------------------------------------------------
#     # Step 4
#     # detect phoneme errors
#     # -----------------------------------------------------

#     detection = detect_phoneme_errors(
#         expected_seq,
#         spoken_seq,
#         target_phoneme
#     )

#     # -----------------------------------------------------
#     # Step 5
#     # return result
#     # -----------------------------------------------------

#     return {

#         "recognized_text": recognized_text,

#         "expected_phonemes": expected_seq,
#         "spoken_phonemes": spoken_seq,

#         "target_phoneme": target_phoneme,

#         "target_positions": detection["target_positions"],

#         "errors": detection["errors"],

#         "accuracy": detection["accuracy"]
#     }

# """
# Word-Level Articulation Engine (Index-Free Version)

# Pipeline:

# 1) Convert Arabic word → phoneme sequence
# 2) Convert target letter → phoneme
# 3) Extract phoneme stream from audio
# 4) Normalize phoneme stream
# 5) Search for all positions of target phoneme inside word
# 6) Evaluate alignment for each position
# 7) Choose best match
# 8) Classify articulation error
# """

# import uuid
# import os
# import soundfile as sf

# from app.models_loader import allosaurus_model

# from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# from app.services.phoneme.phoneme_detector import evaluate_phoneme_alignment, normalize_stream
# from app.services.phoneme.phoneme_confusions import detect_confusion


# # ---------------------------------------------------------
# # Extract phoneme stream
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
# # Find all positions of phoneme inside word
# # Handles repeated letters
# # ---------------------------------------------------------

# def find_target_positions(target_seq, target_phoneme):

#     positions = []

#     for i, p in enumerate(target_seq):

#         if p == target_phoneme:
#             positions.append(i)

#     return positions


# # ---------------------------------------------------------
# # Evaluate all possible positions
# # ---------------------------------------------------------

# def evaluate_multiple_positions(stream, target_seq, target_phoneme):

#     positions = find_target_positions(target_seq, target_phoneme)

#     best_result = None
#     best_score = -1

#     for pos in positions:

#         result = evaluate_phoneme_alignment(
#             stream,
#             target_seq,
#             pos
#         )

#         if result["score"] > best_score:

#             best_score = result["score"]
#             best_result = result

#     return best_result


# # ---------------------------------------------------------
# # Main Word Detection
# # ---------------------------------------------------------

# def detect_word_level(
#     y,
#     sr,
#     target_word,
#     target_letter
# ):

#     # -----------------------------------------------------
#     # Step 1: Convert word → phoneme sequence
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
#     # Step 2: Convert target letter → phoneme
#     # -----------------------------------------------------

#     letter_seq = arabic_to_phoneme_sequence(target_letter)

#     if not letter_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "target_letter_conversion_error",
#             "expected_phoneme": None,
#             "spoken_phoneme": None
#         }

#     target_phoneme = letter_seq[0]

#     # -----------------------------------------------------
#     # Step 3: Extract phoneme stream
#     # -----------------------------------------------------

#     phoneme_stream = infer_phoneme_stream(y, sr)

#     if not phoneme_stream:

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": target_phoneme,
#             "spoken_phoneme": None
#         }

#     # -----------------------------------------------------
#     # Step 4: Normalize stream
#     # -----------------------------------------------------

#     phoneme_stream = normalize_stream(phoneme_stream)

#     if not phoneme_stream:

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": target_phoneme,
#             "spoken_phoneme": None
#         }

#     # -----------------------------------------------------
#     # Step 5: Evaluate all candidate positions
#     # -----------------------------------------------------

#     alignment = evaluate_multiple_positions(
#         phoneme_stream,
#         target_seq,
#         target_phoneme
#     )

#     if alignment is None:

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": target_phoneme,
#             "spoken_phoneme": None
#         }

#     if alignment["score"] < 0.5:

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": target_phoneme,
#             "spoken_phoneme": None
#         }

#     expected = alignment["expected_phoneme"]
#     spoken = alignment["spoken_phoneme"]
#     error_type = alignment["error_type"]
#     score = alignment["score"]

#     accuracy = int(score * 100)

#     # -----------------------------------------------------
#     # Error classification
#     # -----------------------------------------------------

#     if error_type == "substitution":

#         accuracy = min(accuracy, 30)

#     elif error_type == "omission":

#         accuracy = 0

#     elif error_type is None:

#         if accuracy < 80:
#             error_type = "distortion"

#     # -----------------------------------------------------
#     # Confusion detection
#     # -----------------------------------------------------

#     confusion = detect_confusion(expected, spoken)

#     return {
#         "accuracy": accuracy,
#         "error_type": error_type,
#         "expected_phoneme": expected,
#         "spoken_phoneme": spoken,
#         "confusion_type": confusion
#     }










# # """
# # Word-Level Articulation Engine (Robust Version)

# # Pipeline:

# # 1) Convert Arabic word → phoneme sequence
# # 2) Extract phoneme stream from audio (Allosaurus)
# # 3) Normalize phoneme stream
# # 4) Detect phoneme using context alignment
# # 5) Handle repeated phoneme cases
# # 6) Classify articulation error
# # """

# # import uuid
# # import os
# # import soundfile as sf

# # from app.models_loader import allosaurus_model
# # from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# # from app.services.phoneme.phoneme_detector import evaluate_phoneme_alignment
# # from app.services.phoneme.phoneme_confusions import detect_confusion

# # # ---------------------------------------------------------
# # # Extract phoneme stream from audio
# # # ---------------------------------------------------------

# # def infer_phoneme_stream(y, sr):

# #     temp_file = f"temp_{uuid.uuid4().hex}.wav"
# #     sf.write(temp_file, y, sr)

# #     try:

# #         result = allosaurus_model.recognize(temp_file)

# #         phoneme_stream = result.strip().split()

# #         return phoneme_stream

# #     finally:

# #         if os.path.exists(temp_file):
# #             os.remove(temp_file)


# # # ---------------------------------------------------------
# # # Normalize phoneme stream
# # # Removes vowels and unstable symbols
# # # ---------------------------------------------------------

# # def normalize_stream(stream):

# #     vowels = {
# #         "a","e","i","o","u",
# #         "ɒ","ə","ɪ","ʊ","ɛ","æ","ɑ"
# #     }

# #     cleaned = []

# #     for p in stream:

# #         if p in vowels:
# #             continue

# #         # remove length marks
# #         p = p.replace("ː","")

# #         cleaned.append(p)

# #     return cleaned


# # # ---------------------------------------------------------
# # # Convert Arabic right index → phoneme index
# # # ---------------------------------------------------------

# # def convert_index_from_right(word, index_from_right):

# #     """
# #     Arabic indexing example:

# #     سمكة

# #     right index:
# #     0 = ة
# #     1 = ك
# #     2 = م
# #     3 = س
# #     """

# #     return len(word) - 1 - index_from_right


# # # ---------------------------------------------------------
# # # Main Word Detection
# # # ---------------------------------------------------------

# # def detect_word_level(
# #     y,
# #     sr,
# #     target_word,
# #     index_from_right
# # ):

# #     # -----------------------------------------------------
# #     # Step 1: Convert word → phoneme sequence
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
# #     # Step 2: Convert index
# #     # -----------------------------------------------------

# #     target_index = convert_index_from_right(
# #         target_word,
# #         index_from_right
# #     )

# #     if target_index < 0 or target_index >= len(target_seq):

# #         return {
# #             "accuracy": 0,
# #             "error_type": "index_error",
# #             "expected_phoneme": None,
# #             "spoken_phoneme": None
# #         }

# #     expected_phoneme = target_seq[target_index]

# #     # -----------------------------------------------------
# #     # Step 3: Extract phoneme stream
# #     # -----------------------------------------------------

# #     phoneme_stream = infer_phoneme_stream(y, sr)

# #     if not phoneme_stream:

# #         return {
# #             "accuracy": 0,
# #             "error_type": "no_attempt",
# #             "expected_phoneme": expected_phoneme,
# #             "spoken_phoneme": None
# #         }

# #     # -----------------------------------------------------
# #     # Step 4: Normalize phoneme stream
# #     # -----------------------------------------------------

# #     phoneme_stream = normalize_stream(phoneme_stream)

# #     if not phoneme_stream:

# #         return {
# #             "accuracy": 0,
# #             "error_type": "no_attempt",
# #             "expected_phoneme": expected_phoneme,
# #             "spoken_phoneme": None
# #         }

# #     # -----------------------------------------------------
# #     # Step 5: Alignment detection
# #     # -----------------------------------------------------

# #     alignment_result = evaluate_phoneme_alignment(
# #         phoneme_stream,
# #         target_seq,
# #         target_index
# #     )

# #     # -----------------------------------------------------
# #     # Reject if word likely not spoken
# #     # -----------------------------------------------------

# #     if alignment_result["status"] == "no_attempt":

# #         return {
# #             "accuracy": 0,
# #             "error_type": "no_attempt",
# #             "expected_phoneme": expected_phoneme,
# #             "spoken_phoneme": None
# #         }

# #     if alignment_result["score"] < 0.5:

# #         return {
# #             "accuracy": 0,
# #             "error_type": "no_attempt",
# #             "expected_phoneme": expected_phoneme,
# #             "spoken_phoneme": None
# #         }

# #     spoken_phoneme = alignment_result["spoken_phoneme"]
# #     error_type = alignment_result["error_type"]
# #     score = alignment_result["score"]

# #     accuracy = int(score * 100)

# #     # -----------------------------------------------------
# #     # Step 6: Error classification
# #     # -----------------------------------------------------

# #     if error_type == "substitution":

# #         accuracy = min(accuracy, 30)

# #     elif error_type == "omission":

# #         accuracy = 0

# #     elif error_type is None:

# #         if accuracy < 80:
# #             error_type = "distortion"

# #     # -----------------------------------------------------
# #     # Final result
# #     # -----------------------------------------------------
# #     confusion = detect_confusion(expected_phoneme, spoken_phoneme)
# #     return {
# #         "accuracy": accuracy,
# #         "error_type": error_type,
# #         "expected_phoneme": expected_phoneme,
# #         "spoken_phoneme": spoken_phoneme
# #     }   





# # # """
# # # Word-Level Articulation Engine

# # # Pipeline:

# # # 1) Convert target word → phoneme sequence
# # # 2) Extract phoneme stream from audio
# # # 3) Align target phoneme sequence inside stream
# # # 4) Locate target phoneme index
# # # 5) Compare expected vs spoken phoneme
# # # 6) Detect articulation error
# # # """

# # # import uuid
# # # import os
# # # import soundfile as sf

# # # from app.models_loader import allosaurus_model

# # # from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# # # from app.services.phoneme.alignment_engine import evaluate_phoneme_alignment


# # # # ---------------------------------------------------------
# # # # Extract phoneme stream from audio
# # # # ---------------------------------------------------------

# # # def infer_phoneme_stream(y, sr):

# # #     temp_file = f"temp_{uuid.uuid4().hex}.wav"
# # #     sf.write(temp_file, y, sr)

# # #     try:

# # #         result = allosaurus_model.recognize(temp_file)

# # #         phoneme_stream = result.strip().split()

# # #         return phoneme_stream

# # #     finally:

# # #         if os.path.exists(temp_file):
# # #             os.remove(temp_file)


# # # # ---------------------------------------------------------
# # # # Convert Arabic right-based index
# # # # ---------------------------------------------------------

# # # def convert_index_from_right(word, index_from_right):

# # #     """
# # #     Arabic indexing:

# # #     سمكة

# # #     right index:
# # #     0 = ة
# # #     1 = ك
# # #     2 = م
# # #     3 = س
# # #     """

# # #     return len(word) - 1 - index_from_right


# # # # ---------------------------------------------------------
# # # # Main word articulation function
# # # # ---------------------------------------------------------

# # # def detect_word_level(
# # #     y,
# # #     sr,
# # #     target_word,
# # #     index_from_right
# # # ):

# # #     """
# # #     Evaluates articulation of target phoneme inside word.
# # #     """

# # #     # -----------------------------------------------------
# # #     # Step 1: convert target word to phoneme sequence
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
# # #     # Step 2: convert index
# # #     # -----------------------------------------------------

# # #     target_index = convert_index_from_right(
# # #         target_word,
# # #         index_from_right
# # #     )

# # #     if target_index < 0 or target_index >= len(target_seq):

# # #         return {
# # #             "accuracy": 0,
# # #             "error_type": "index_error",
# # #             "expected_phoneme": None,
# # #             "spoken_phoneme": None
# # #         }

# # #     # -----------------------------------------------------
# # #     # Step 3: extract phoneme stream from audio
# # #     # -----------------------------------------------------

# # #     phoneme_stream = infer_phoneme_stream(y, sr)

    
# # #     # Normalize phoneme stream (remove vowels)

      
# # #     vowels = {"a","e","i","o","u","ɒ","ə","ɪ","ʊ","ɛ"}

# # #     phoneme_stream = [
# # #         p for p in phoneme_stream
# # #         if p not in vowels
# # #     ]
    
# # #     if not phoneme_stream:

# # #         return {
# # #             "accuracy": 0,
# # #             "error_type": "no_attempt",
# # #             "expected_phoneme": None,
# # #             "spoken_phoneme": None
# # #         }

# # #     # -----------------------------------------------------
# # #     # Step 4: alignment analysis
# # #     # -----------------------------------------------------

# # #     alignment_result = evaluate_phoneme_alignment(
# # #         phoneme_stream,
# # #         target_seq,
# # #         target_index
# # #     )


# # #     # Reject weak alignments (word likely not spoken)

# # #     if alignment_result["score"] < 0.5:

# # #         return {
# # #             "accuracy": 0,
# # #             "error_type": "no_attempt",
# # #             "expected_phoneme": None,
# # #             "spoken_phoneme": None
# # #         }
        
        
        
# # #     if alignment_result["status"] == "no_attempt":

# # #         return {
# # #             "accuracy": 0,
# # #             "error_type": "no_attempt",
# # #             "expected_phoneme": None,
# # #             "spoken_phoneme": None
# # #         }

# # #     expected = alignment_result["expected_phoneme"]
# # #     spoken = alignment_result["spoken_phoneme"]
# # #     error_type = alignment_result["error_type"]

# # #     # -----------------------------------------------------
# # #     # Step 5: accuracy calculation
# # #     # -----------------------------------------------------

# # #     score = alignment_result["score"]

# # #     accuracy = int(score * 100)

# # #     # -----------------------------------------------------
# # #     # Step 6: classification
# # #     # -----------------------------------------------------

# # #     if error_type == "substitution":

# # #         accuracy = min(accuracy, 30)

# # #     elif error_type == "omission":

# # #         accuracy = 0

# # #     elif error_type is None:

# # #         if accuracy < 80:
# # #             error_type = "distortion"

# # #     # -----------------------------------------------------
# # #     # Final result
# # #     # -----------------------------------------------------

# # #     return {
# # #         "accuracy": accuracy,
# # #         "error_type": error_type,
# # #         "expected_phoneme": expected,
# # #         "spoken_phoneme": spoken
# # #     }








# # # # """
# # # # Word-Level Articulation Engine (Production Version)

# # # # Handles:
# # # # - no_attempt
# # # # - substitution
# # # # - omission
# # # # - distortion
# # # # - success
# # # # """

# # # # import uuid
# # # # import os
# # # # import soundfile as sf

# # # # from app.models_loader import whisper_model, allosaurus_model
# # # # from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# # # # from app.services.phoneme.alignment_engine import find_best_alignment
# # # # from app.services.articulation.isolation_engine import spectral_validation


# # # # # ---------------------------------------------------------
# # # # # Extract full phoneme stream using Allosaurus
# # # # # ---------------------------------------------------------

# # # # def infer_full_phoneme_stream(y, sr):

# # # #     temp_file = f"temp_{uuid.uuid4().hex}.wav"
# # # #     sf.write(temp_file, y, sr)

# # # #     try:
# # # #         result = allosaurus_model.recognize(temp_file)
# # # #         return result.strip().split()
# # # #     finally:
# # # #         if os.path.exists(temp_file):
# # # #             os.remove(temp_file)


# # # # # ---------------------------------------------------------
# # # # # Main Word-Level Detection
# # # # # ---------------------------------------------------------

# # # # def detect_word_level(y, sr, target_word, index_from_right):

# # # #     # -----------------------------------------------------
# # # #     # Step 1: Convert word to phoneme sequence
# # # #     # -----------------------------------------------------

# # # #     target_seq = arabic_to_phoneme_sequence(target_word)

# # # #     if not target_seq:
# # # #         return {
# # # #             "accuracy": 0,
# # # #             "error_type": "conversion_error",
# # # #             "expected_phoneme": None,
# # # #             "spoken_phoneme": None
# # # #         }

# # # #     # -----------------------------------------------------
# # # #     # Step 2: Whisper lexical soft check
# # # #     # -----------------------------------------------------

# # # #     temp_file = f"temp_{uuid.uuid4().hex}.wav"
# # # #     sf.write(temp_file, y, sr)

# # # #     try:
# # # #         segments, _ = whisper_model.transcribe(temp_file, language="ar")
# # # #         whisper_text = " ".join([seg.text for seg in segments])
# # # #     finally:
# # # #         if os.path.exists(temp_file):
# # # #             os.remove(temp_file)

# # # #     # Soft check only — do not reject

# # # #     # -----------------------------------------------------
# # # #     # Step 3: Allosaurus full phoneme stream
# # # #     # -----------------------------------------------------

# # # #     full_stream = infer_full_phoneme_stream(y, sr)

# # # #     if not full_stream:
# # # #         return {
# # # #             "accuracy": 0,
# # # #             "error_type": "no_attempt",
# # # #             "expected_phoneme": None,
# # # #             "spoken_phoneme": None
# # # #         }

# # # #     # -----------------------------------------------------
# # # #     # Step 4: Dynamic alignment
# # # #     # -----------------------------------------------------

# # # #     start_index, score, window = find_best_alignment(
# # # #         full_stream,
# # # #         target_seq
# # # #     )

# # # #     if score < 0.5:
# # # #         return {
# # # #             "accuracy": 0,
# # # #             "error_type": "no_attempt",
# # # #             "expected_phoneme": None,
# # # #             "spoken_phoneme": None
# # # #         }

# # # #     # -----------------------------------------------------
# # # #     # Step 5: Convert right index based on PHONEME length
# # # #     # -----------------------------------------------------

# # # #     index_from_left = len(target_seq) - 1 - index_from_right

# # # #     if index_from_left < 0 or index_from_left >= len(target_seq):
# # # #         return {
# # # #             "accuracy": 0,
# # # #             "error_type": "index_error",
# # # #             "expected_phoneme": None,
# # # #             "spoken_phoneme": None
# # # #         }

# # # #     # -----------------------------------------------------
# # # #     # Step 6: Extract expected + spoken safely
# # # #     # -----------------------------------------------------

# # # #     expected_phoneme = target_seq[index_from_left]

# # # #     if index_from_left >= len(window):
# # # #         return {
# # # #             "accuracy": 0,
# # # #             "error_type": "omission",
# # # #             "expected_phoneme": expected_phoneme,
# # # #             "spoken_phoneme": None
# # # #         }

# # # #     spoken_phoneme = window[index_from_left]

# # # #     # -----------------------------------------------------
# # # #     # Step 7: Compare
# # # #     # -----------------------------------------------------

# # # #     if spoken_phoneme != expected_phoneme:
# # # #         return {
# # # #             "accuracy": 0,
# # # #             "error_type": "substitution",
# # # #             "expected_phoneme": expected_phoneme,
# # # #             "spoken_phoneme": spoken_phoneme
# # # #         }

# # # #     # -----------------------------------------------------
# # # #     # Step 8: Spectral validation (distortion check)
# # # #     # -----------------------------------------------------

# # # #     if not spectral_validation(y, sr, expected_phoneme):
# # # #         return {
# # # #             "accuracy": 70,
# # # #             "error_type": "distortion",
# # # #             "expected_phoneme": expected_phoneme,
# # # #             "spoken_phoneme": spoken_phoneme
# # # #         }

# # # #     # -----------------------------------------------------
# # # #     # SUCCESS
# # # #     # -----------------------------------------------------

# # # #     return {
# # # #         "accuracy": 100,
# # # #         "error_type": None,
# # # #         "expected_phoneme": expected_phoneme,
# # # #         "spoken_phoneme": spoken_phoneme
# # # #     }






# # # # # """
# # # # # Word-Level Articulation Engine

# # # # # Pipeline Overview:

# # # # # 1) Convert target Arabic word → phoneme sequence
# # # # # 2) Run Whisper to check if child said the intended word
# # # # # 3) Run Allosaurus to get full phoneme stream from audio
# # # # # 4) Use alignment_engine to find best match of target word inside stream
# # # # # 5) Locate target phoneme inside aligned window
# # # # # 6) Compare expected vs spoken phoneme
# # # # # 7) Run spectral validation if needed
# # # # # 8) Return structured diagnostic result

# # # # # This engine handles:
# # # # # - substitution
# # # # # - omission
# # # # # - distortion
# # # # # - success
# # # # # """

# # # # # import uuid
# # # # # import os
# # # # # import soundfile as sf

# # # # # from app.models_loader import whisper_model, allosaurus_model
# # # # # from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# # # # # from app.services.phoneme.alignment_engine import find_best_alignment
# # # # # from app.services.articulation.isolation_engine import spectral_validation


# # # # # # ---------------------------------------------------------
# # # # # # Step 1: Extract full phoneme stream from audio
# # # # # # ---------------------------------------------------------
# # # # # def infer_full_phoneme_stream(y, sr):
# # # # #     """
# # # # #     Uses Allosaurus to convert full audio into phoneme stream.
# # # # #     """

# # # # #     temp_file = f"temp_{uuid.uuid4().hex}.wav"
# # # # #     sf.write(temp_file, y, sr)

# # # # #     try:
# # # # #         result = allosaurus_model.recognize(temp_file)
# # # # #         return result.strip().split()
# # # # #     finally:
# # # # #         if os.path.exists(temp_file):
# # # # #             os.remove(temp_file)


# # # # # # ---------------------------------------------------------
# # # # # # Step 2: Word-Level Detection
# # # # # # ---------------------------------------------------------
# # # # # def detect_word_level(y, sr, target_word, index_from_right):
# # # # #     """
# # # # #     Evaluates articulation of a specific phoneme inside a word.

# # # # #     Parameters:
# # # # #         y : waveform
# # # # #         sr : sample rate
# # # # #         target_word : Arabic word (e.g., "سمكة")
# # # # #         index_from_right : target letter index (Arabic right-based)

# # # # #     Returns:
# # # # #         structured result dictionary
# # # # #     """

# # # # #     # -----------------------------------------------------
# # # # #     # Convert Arabic word → phoneme sequence
# # # # #     # Example: "سمكة" → ["s","m","k"]
# # # # #     # -----------------------------------------------------
# # # # #     target_seq = arabic_to_phoneme_sequence(target_word)

# # # # #     # If conversion fails, abort
# # # # #     if not target_seq:
# # # # #         return {
# # # # #             "accuracy": 0,
# # # # #             "error_type": "conversion_error",
# # # # #             "expected_phoneme": None,
# # # # #             "spoken_phoneme": None
# # # # #         }

# # # # #     # -----------------------------------------------------
# # # # #     # Run Whisper for lexical sanity check
# # # # #     # Ensures child roughly said the intended word
# # # # #     # -----------------------------------------------------
# # # # #     temp_file = f"temp_whisper.wav"
# # # # #     sf.write(temp_file, y, sr)

# # # # #     segments, _ = whisper_model.transcribe(temp_file, language="ar")
# # # # #     whisper_text = " ".join([seg.text for seg in segments])

# # # # #     if os.path.exists(temp_file):
# # # # #         os.remove(temp_file)

# # # # #     # NOTE:
# # # # #     # We DO NOT reject based on Whisper.
# # # # #     # We only use it as a soft check.
# # # # #     # Phoneme alignment is the real decision layer.


# # # # #     # -----------------------------------------------------
# # # # #     # Extract phoneme stream from full audio
# # # # #     # -----------------------------------------------------
# # # # #     full_stream = infer_full_phoneme_stream(y, sr)

# # # # #     if not full_stream:
# # # # #         return {
# # # # #             "accuracy": 0,
# # # # #             "error_type": "no_attempt",
# # # # #             "expected_phoneme": None,
# # # # #             "spoken_phoneme": None
# # # # #         }

# # # # #     # -----------------------------------------------------
# # # # #     # Use dynamic alignment to locate best match window
# # # # #     # -----------------------------------------------------
# # # # #     start_index, score, window = find_best_alignment(
# # # # #         full_stream,
# # # # #         target_seq
# # # # #     )

# # # # #     # If similarity too low → word likely not spoken
# # # # #     if score < 0.5:
# # # # #         return {
# # # # #             "accuracy": 0,
# # # # #             "error_type": "no_attempt",
# # # # #             "expected_phoneme": None,
# # # # #             "spoken_phoneme": None
# # # # #         }

# # # # #     # -----------------------------------------------------
# # # # #     # Convert right-based index to left-based
# # # # #     # Arabic word indexing logic
# # # # #     # -----------------------------------------------------
# # # # #     index_from_left = len(target_word) - 1 - index_from_right

# # # # #     # Ensure index valid
# # # # #     if index_from_left < 0 or index_from_left >= len(target_seq):
# # # # #         return {
# # # # #             "accuracy": 0,
# # # # #             "error_type": "index_error",
# # # # #             "expected_phoneme": None,
# # # # #             "spoken_phoneme": None
# # # # #         }

# # # # #     # -----------------------------------------------------
# # # # #     # Expected phoneme from target sequence
# # # # #     # -----------------------------------------------------
# # # # #     expected_phoneme = target_seq[index_from_left]

# # # # #     # -----------------------------------------------------
# # # # #     # Spoken phoneme from aligned window
# # # # #     # -----------------------------------------------------
# # # # #     spoken_phoneme = window[index_from_left]

# # # # #     # -----------------------------------------------------
# # # # #     # Compare phonemes
# # # # #     # -----------------------------------------------------
# # # # #     if spoken_phoneme != expected_phoneme:
# # # # #         return {
# # # # #             "accuracy": 0,
# # # # #             "error_type": "substitution",
# # # # #             "expected_phoneme": expected_phoneme,
# # # # #             "spoken_phoneme": spoken_phoneme
# # # # #         }

# # # # #     # -----------------------------------------------------
# # # # #     # Spectral validation for distortion detection
# # # # #     # -----------------------------------------------------
# # # # #     if not spectral_validation(y, sr, expected_phoneme):
# # # # #         return {
# # # # #             "accuracy": 70,
# # # # #             "error_type": "distortion",
# # # # #             "expected_phoneme": expected_phoneme,
# # # # #             "spoken_phoneme": spoken_phoneme
# # # # #         }

# # # # #     # -----------------------------------------------------
# # # # #     # Full success
# # # # #     # -----------------------------------------------------
# # # # #     return {
# # # # #         "accuracy": 100,
# # # # #         "error_type": None,
# # # # #         "expected_phoneme": expected_phoneme,
# # # # #         "spoken_phoneme": spoken_phoneme
# # # # #     }






# # # # # # """
# # # # # # Word-Level Articulation Engine

# # # # # # Uses:
# # # # # # - Faster-Whisper (text inference)
# # # # # # - Allosaurus (phoneme inference)
# # # # # # - Spectral validation
# # # # # # - Error classification
# # # # # # """

# # # # # # import uuid
# # # # # # import os
# # # # # # import soundfile as sf
# # # # # # import numpy as np
# # # # # # import librosa

# # # # # # from app.models_loader import whisper_model, allosaurus_model


# # # # # # # ---------------------------------------------------
# # # # # # # Arabic → IPA mapping
# # # # # # # ---------------------------------------------------
# # # # # # ARABIC_TO_IPA = {
# # # # # #     "س": "s",
# # # # # #     "ر": "r",
# # # # # #     "ك": "k",
# # # # # #     "ز": "z",
# # # # # #     "ش": "ʃ",
# # # # # #     "ث": "θ",
# # # # # #     "ذ": "ð",
# # # # # #     "ص": "sˤ",
# # # # # #     "ض": "dˤ",
# # # # # #     "ط": "tˤ",
# # # # # #     "ظ": "ðˤ",
# # # # # #     "ف": "f",
# # # # # #     "خ": "x",
# # # # # #     "غ": "ɣ"
# # # # # # }


# # # # # # # ---------------------------------------------------
# # # # # # # Whisper transcription (faster-whisper)
# # # # # # # ---------------------------------------------------
# # # # # # def whisper_transcribe(y, sr):

# # # # # #     temp_file = f"temp_{uuid.uuid4().hex}.wav"
# # # # # #     sf.write(temp_file, y, sr)

# # # # # #     try:
# # # # # #         segments, info = whisper_model.transcribe(
# # # # # #             temp_file,
# # # # # #             language="ar"
# # # # # #         )

# # # # # #         text = ""
# # # # # #         confidences = []

# # # # # #         for segment in segments:
# # # # # #             text += segment.text
# # # # # #             confidences.append(segment.avg_logprob)

# # # # # #         confidence = float(np.mean(confidences)) if confidences else 0

# # # # # #         return text.strip(), confidence

# # # # # #     finally:
# # # # # #         if os.path.exists(temp_file):
# # # # # #             os.remove(temp_file)


# # # # # # # ---------------------------------------------------
# # # # # # # Allosaurus phoneme inference
# # # # # # # ---------------------------------------------------
# # # # # # def infer_phonemes(y, sr):

# # # # # #     temp_file = f"temp_{uuid.uuid4().hex}.wav"
# # # # # #     sf.write(temp_file, y, sr)

# # # # # #     try:
# # # # # #         result = allosaurus_model.recognize(temp_file)
# # # # # #         phonemes = result.strip().split()
# # # # # #         return phonemes
# # # # # #     finally:
# # # # # #         if os.path.exists(temp_file):
# # # # # #             os.remove(temp_file)


# # # # # # # ---------------------------------------------------
# # # # # # # Extract target phoneme by position
# # # # # # # ---------------------------------------------------
# # # # # # def extract_target_char(expected_word, target_position):

# # # # # #     if target_position == "initial":
# # # # # #         return expected_word[0]

# # # # # #     if target_position == "final":
# # # # # #         return expected_word[-1]

# # # # # #     if target_position == "medial":
# # # # # #         return expected_word[len(expected_word)//2]

# # # # # #     return expected_word[0]


# # # # # # # ---------------------------------------------------
# # # # # # # Spectral validation
# # # # # # # ---------------------------------------------------
# # # # # # def spectral_validation(y, sr, target_ipa):

# # # # # #     centroid = np.mean(
# # # # # #         librosa.feature.spectral_centroid(y=y, sr=sr)
# # # # # #     )

# # # # # #     rms = librosa.feature.rms(y=y)[0]
# # # # # #     peak_energy = np.max(rms)

# # # # # #     # Fricatives
# # # # # #     if target_ipa in ["s", "z", "ʃ", "θ", "ð", "f", "x", "ɣ"]:
# # # # # #         return centroid > 2800

# # # # # #     # Emphatics
# # # # # #     if target_ipa in ["sˤ", "dˤ", "tˤ", "ðˤ"]:
# # # # # #         return centroid > 2000

# # # # # #     # Stops
# # # # # #     if target_ipa in ["k", "q", "t", "d", "b"]:
# # # # # #         return peak_energy > 0.04

# # # # # #     # Liquids
# # # # # #     if target_ipa in ["r", "l"]:
# # # # # #         return centroid > 1400

# # # # # #     return True


# # # # # # # ---------------------------------------------------
# # # # # # # Main Word-Level Detection
# # # # # # # ---------------------------------------------------
# # # # # # def detect_word_level(y, sr, target_phoneme, target_position, expected_word):

# # # # # #     # Convert Arabic to IPA
# # # # # #     target_char = extract_target_char(expected_word, target_position)

# # # # # #     if target_char in ARABIC_TO_IPA:
# # # # # #         target_ipa = ARABIC_TO_IPA[target_char]
# # # # # #     else:
# # # # # #         target_ipa = target_char

# # # # # #     # 1️⃣ Whisper transcription
# # # # # #     whisper_text, whisper_conf = whisper_transcribe(y, sr)

# # # # # #     # 2️⃣ Allosaurus phoneme detection
# # # # # #     detected_phonemes = infer_phonemes(y, sr)

# # # # # #     # 3️⃣ Alignment check
# # # # # #     if target_ipa not in detected_phonemes:
# # # # # #         return {
# # # # # #             "accuracy": 0,
# # # # # #             "error_type": "substitution_or_omission",
# # # # # #             "whisper_text": whisper_text,
# # # # # #             "whisper_confidence": whisper_conf,
# # # # # #             "detected_sequence": detected_phonemes
# # # # # #         }

# # # # # #     # 4️⃣ Spectral validation
# # # # # #     if not spectral_validation(y, sr, target_ipa):
# # # # # #         return {
# # # # # #             "accuracy": 70,
# # # # # #             "error_type": "distortion",
# # # # # #             "whisper_text": whisper_text,
# # # # # #             "whisper_confidence": whisper_conf,
# # # # # #             "detected_sequence": detected_phonemes
# # # # # #         }

# # # # # #     # 5️⃣ Success
# # # # # #     return {
# # # # # #         "accuracy": 100,
# # # # # #         "error_type": None,
# # # # # #         "whisper_text": whisper_text,
# # # # # #         "whisper_confidence": whisper_conf,
# # # # # #         "detected_sequence": detected_phonemes
# # # # # #     }