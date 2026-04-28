# ---------------------------------------------
# Mock dependencies
# ---------------------------------------------
from app.services.validation.validation_engine import validate_spoken_input


def mock_clean_arabic_text(text):
    return text.strip()

def mock_arabic_to_phoneme_sequence(text):
    # تحويل بسيط: كل حرف phoneme
    return list(text)


# inject mocks
clean_arabic_text = mock_clean_arabic_text
arabic_to_phoneme_sequence = mock_arabic_to_phoneme_sequence


# ---------------------------------------------
# TEST FUNCTION
# ---------------------------------------------
def test_validate_spoken_input():

    # -------------------------------
    # 1️⃣ Exact match
    # -------------------------------
    valid, score, spoken = validate_spoken_input(
        spoken_text="سلام",
        target_text="سلام"
    )

    assert valid == True
    assert score == 1.0


    # -------------------------------
    # 2️⃣ Similar text (above threshold)
    # -------------------------------
    valid, score, spoken = validate_spoken_input(
        spoken_text="سلا",
        target_text="سلام",
        threshold=0.3
    )

    assert valid == True
    assert score > 0.3


    # -------------------------------
    # 3️⃣ Different text (below threshold)
    # -------------------------------
    valid, score, spoken = validate_spoken_input(
        spoken_text="كتاب",
        target_text="سلام",
        threshold=0.5
    )

    assert valid == False


    # -------------------------------
    # 4️⃣ Empty spoken input
    # -------------------------------
    valid, score, spoken = validate_spoken_input(
        spoken_text="",
        target_text="سلام"
    )

    assert valid == False
    assert score == 0


    # -------------------------------
    # 5️⃣ With phoneme validation (valid)
    # -------------------------------
    valid, score, spoken = validate_spoken_input(
        spoken_text="سلام",
        target_text="سلام",
        target_letter="س"
    )

    assert valid == True


    # -------------------------------
    # 6️⃣ Phoneme missing in target
    # -------------------------------
    valid, score, spoken = validate_spoken_input(
        spoken_text="سلام",
        target_text="لام",
        target_letter="س"
    )

    assert valid == False


    # -------------------------------
    # 7️⃣ Phoneme sequence empty (edge case)
    # -------------------------------
    def mock_empty_phoneme(text):
        return []

    global arabic_to_phoneme_sequence
    arabic_to_phoneme_sequence = mock_empty_phoneme

    valid, score, spoken = validate_spoken_input(
        spoken_text="سلام",
        target_text="سلام",
        target_letter="س"
    )

    assert valid == False


    print("🔥 Validator tests passed!")


# ---------------------------------------------
# RUN TEST
# ---------------------------------------------
test_validate_spoken_input()