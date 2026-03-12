"""
exercise_validator.py

Validates that the exercise configuration sent by the backend is correct.

Example:
target_word = "سمكة"
target_letter = "س"
"""

def validate_exercise(target_word, target_letter):

    if not target_word or not target_letter:

        return False, {

            "error_type": "invalid_exercise",

            "message": "Target word or letter missing",

            "target_word": target_word,
            "target_letter": target_letter
        }


    # -------------------------------------------------
    # Check that letter exists in word
    # -------------------------------------------------

    if target_letter not in target_word:

        return False, {

            "error_type": "invalid_target_configuration",

            "message": "Target letter not found in target word",

            "target_word": target_word,
            "target_letter": target_letter
        }


    return True, None