"""
Isolation Engine (Final Version)

Evaluates articulation of a single phoneme spoken in isolation.

Pipeline

1) audio → ASR
2) ASR text → phoneme sequence
3) extract dominant phoneme
4) compare with expected phoneme
"""

from app.services.asr.asr_engine import transcribe_audio
from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
from app.services.phoneme.phoneme_confusions import detect_confusion


# ---------------------------------------------------------
# Isolation articulation detection
# ---------------------------------------------------------

def detect_isolation(y, sr, target_letter):
    
    if len(target_letter) != 1:

        return {

            "accuracy": None,

            "error_type": "invalid_target_letter",

            "message": "Isolation level requires a single letter"
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
            "expected_phoneme": None,
            "spoken_phoneme": None
        }

    # -----------------------------------------------------
    # Step 2
    # convert target letter → phoneme
    # -----------------------------------------------------

    target_seq = arabic_to_phoneme_sequence(target_letter)

    if not target_seq:

        return {
            "accuracy": 0,
            "error_type": "conversion_error",
            "expected_phoneme": None,
            "spoken_phoneme": None
        }

    expected_phoneme = target_seq[0]

    # -----------------------------------------------------
    # Step 3
    # convert spoken text → phonemes
    # -----------------------------------------------------

    spoken_seq = arabic_to_phoneme_sequence(recognized_text)

    if not spoken_seq:

        return {
            "accuracy": 0,
            "error_type": "phoneme_conversion_error",
            "expected_phoneme": expected_phoneme,
            "spoken_phoneme": None
        }

    # -----------------------------------------------------
    # Step 4
    # dominant phoneme detection
    # -----------------------------------------------------

    spoken_phoneme = spoken_seq[0]

    # -----------------------------------------------------
    # Step 5
    # comparison
    # -----------------------------------------------------

    if spoken_phoneme == expected_phoneme:

        return {
            "accuracy": 100,
            "error_type": None,
            "expected_phoneme": expected_phoneme,
            "spoken_phoneme": spoken_phoneme,
            "confusion_type": None
        }

    confusion = detect_confusion(expected_phoneme, spoken_phoneme)

    return {
        "accuracy": 0,
        "error_type": "substitution",
        "expected_phoneme": expected_phoneme,
        "spoken_phoneme": spoken_phoneme,
        "confusion_type": confusion
    }

