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

