from app.services.articulation.acoustic_isolation_detector import (
    detect_isolation as acoustic_detect
)


def detect_isolation(
    y,
    sr,
    target_letter
):

    # -------------------------------------------------
    # validate target
    # -------------------------------------------------

    if not target_letter:

        return {

            "accuracy": 0,

            "exercise_correct": False,

            "recognized_text": None,

            "expected_phonemes": [],

            "spoken_phonemes": [],

            "target_phoneme": None,

            "target_positions": [],

            "errors": [],

            "original_text": None,

            "target_unit": None,

            "error_type": "missing_target"
        }

    target_letter = target_letter.strip()

    if len(target_letter) != 1:

        return {

            "accuracy": 0,

            "exercise_correct": False,

            "recognized_text": None,

            "expected_phonemes": [],

            "spoken_phonemes": [],

            "target_phoneme": None,

            "target_positions": [],

            "errors": [],

            "original_text": target_letter,

            "target_unit": target_letter,

            "error_type": "invalid_target_letter"
        }

    # -------------------------------------------------
    # acoustic detection
    # -------------------------------------------------

    result = acoustic_detect(
        y,
        sr,
        target_letter
    )

    details = result.get("details", {})

    predicted = (
        details.get("predicted")
        or details.get("predicted_type")
    )

    accuracy = result.get("accuracy", 0)

    # -------------------------------------------------
    # unified response
    # -------------------------------------------------

    return {

        "accuracy": accuracy,

        "exercise_correct": accuracy == 100,

        "recognized_text": predicted,

        "expected_phonemes": [target_letter],

        "spoken_phonemes": [predicted] if predicted else [],

        "target_phoneme": target_letter,

        "target_positions": [0],

        "errors": details.get("errors", []),

        "original_text": target_letter,

        "target_unit": target_letter,

        "error_type": result.get("error_type")
    }

# from app.services.articulation.acoustic_isolation_detector import detect_isolation as acoustic_detect


# def detect_isolation(y, sr, target_letter):

#     if not target_letter:
#         return {
#             "accuracy": 0,
#             "error_type": "missing_target",
#             "details": {}
#         }

#     target_letter = target_letter.strip()

#     if len(target_letter) != 1:
#         return {
#             "accuracy": 0,
#             "error_type": "invalid_target_letter",
#             "details": {
#                 "target_letter": target_letter
#             }
#         }

#     result = acoustic_detect(y, sr, target_letter)

#     details = result.get("details", {})

#     return {
#         "accuracy": result.get("accuracy", 0),
#         "error_type": result.get("error_type"),
#         "details": {
#             "expected_phoneme": target_letter,
#             "predicted": details.get("predicted") or details.get("predicted_type"),
#             "extra": details
#         }
#     }