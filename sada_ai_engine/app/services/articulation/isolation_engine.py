from app.services.articulation.acoustic_isolation_detector import detect_isolation as acoustic_detect


def detect_isolation(y, sr, target_letter):

    if not target_letter:
        return {
            "accuracy": 0,
            "error_type": "missing_target",
            "details": {}
        }

    target_letter = target_letter.strip()

    if len(target_letter) != 1:
        return {
            "accuracy": 0,
            "error_type": "invalid_target_letter",
            "details": {
                "target_letter": target_letter
            }
        }

    result = acoustic_detect(y, sr, target_letter)

    details = result.get("details", {})

    return {
        "accuracy": result.get("accuracy", 0),
        "error_type": result.get("error_type"),
        "details": {
            "expected_phoneme": target_letter,
            "predicted": details.get("predicted") or details.get("predicted_type"),
            "extra": details
        }
    }