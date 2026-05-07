from app.services.articulation.word_engine import detect_word_level

from app.services.articulation.syllable_utils import (
    extract_target_syllable
)


def detect_syllable_level(
    y,
    sr,
    target_word,
    target_letter
):

    # ---------------------------------------------
    # extract syllable from word
    # ---------------------------------------------

    syllable = extract_target_syllable(
        target_word,
        target_letter
    )

    if not syllable:

        return {
            "accuracy": 0,
            "error_type": "syllable_extraction_error",
            "details": {
                "target_word": target_word,
                "target_letter": target_letter
            }
        }

    # ---------------------------------------------
    # reuse word engine
    # ---------------------------------------------

    result = detect_word_level(
        y=y,
        sr=sr,
        target_word=syllable,
        target_letter=target_letter
    )

    # ---------------------------------------------
    # enrich result
    # ---------------------------------------------

    result["mode"] = "articulation"
    result["exercise_level"] = "syllable"

    result["details"] = {
        **result.get("details", {}),
        "original_word": target_word,
        "target_syllable": syllable
    }

    return result