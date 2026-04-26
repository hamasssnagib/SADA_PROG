from difflib import SequenceMatcher

from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
from app.services.text.text_cleaner import clean_arabic_text


# ---------------------------------------------------------
# similarity
# ---------------------------------------------------------

def similarity(a, b):

    return SequenceMatcher(None, a, b).ratio()


# ---------------------------------------------------------
# find phoneme positions
# ---------------------------------------------------------

def find_phoneme_positions(seq, phoneme):

    positions = []

    for i, p in enumerate(seq):

        if p == phoneme:

            positions.append(i)

    return positions


# ---------------------------------------------------------
# main validator
# ---------------------------------------------------------

def validate_spoken_word(

    spoken_word,
    target_word,
    target_letter
):

    # ----------------------------------------
    # clean text
    # ----------------------------------------

    spoken_word = clean_arabic_text(spoken_word)
    target_word = clean_arabic_text(target_word)

    if not spoken_word:

        return False, 0, spoken_word


    # ----------------------------------------
    # similarity check
    # ----------------------------------------

    score = similarity(spoken_word, target_word)

    if score < 0.35:

        return False, score, spoken_word


    # ----------------------------------------
    # phoneme sequences
    # ----------------------------------------

    target_seq = arabic_to_phoneme_sequence(target_word)
    spoken_seq = arabic_to_phoneme_sequence(spoken_word)

    if not target_seq or not spoken_seq:

        return False, score, spoken_word


    # ----------------------------------------
    # target phoneme
    # ----------------------------------------

    letter_seq = arabic_to_phoneme_sequence(target_letter)

    if not letter_seq:

        return False, score, spoken_word


    target_phoneme = letter_seq[0]


    # ----------------------------------------
    # check phoneme positions
    # ----------------------------------------

    target_positions = find_phoneme_positions(

        target_seq,
        target_phoneme
    )

    spoken_positions = find_phoneme_positions(

        spoken_seq,
        target_phoneme
    )


    # ----------------------------------------
    # allow missing phoneme
    # (child may substitute it)
    # ----------------------------------------

    if not target_positions:

        return False, score, spoken_word


    return True, score, spoken_word
