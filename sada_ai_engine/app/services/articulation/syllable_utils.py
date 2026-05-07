def extract_target_syllable(
    target_word,
    target_letter
):

    """
    Extract simple syllable containing target letter
    """

    if not target_word or not target_letter:
        return None

    index = target_word.find(target_letter)

    if index == -1:
        return None

    # -------------------------------------------------
    # Example simple extraction
    # سمكة → سم
    # -------------------------------------------------

    if index < len(target_word) - 1:
        return target_word[index:index + 2]

    return target_word[index]