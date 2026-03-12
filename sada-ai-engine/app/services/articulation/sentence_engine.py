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


