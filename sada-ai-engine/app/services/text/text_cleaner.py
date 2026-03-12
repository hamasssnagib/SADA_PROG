# import re


# def clean_arabic_text(text):

#     if not text:
#         return "" 

#     text = text.strip()

#     # remove tashkeel
#     text = re.sub(r"[ًٌٍَُِّْـ]", "", text)

#     # remove non arabic chars
#     text = re.sub(r"[^\u0600-\u06FF\s]", "", text)

#     # normalize taa marbuta
#     text = text.replace("ة", "ه")

#     # remove extra spaces
#     text = re.sub(r"\s+", " ", text)

#     return text






import re


def clean_arabic_text(text):

    if not text:
        return ""

    # ---------------------------------
    # Trim spaces
    # ---------------------------------
    text = text.strip()

    # ---------------------------------
    # Remove Arabic diacritics
    # ---------------------------------
    text = re.sub(r"[ًٌٍَُِّْـ]", "", text)

    # ---------------------------------
    # Normalize Arabic letters
    # ---------------------------------
    text = re.sub(r"[إأآا]", "ا", text)
    text = re.sub(r"ى", "ي", text)
    text = re.sub(r"ؤ", "و", text)
    text = re.sub(r"ئ", "ي", text)

    # ---------------------------------
    # Remove punctuation / non-Arabic
    # ---------------------------------
    text = re.sub(r"[^\u0600-\u06FF\s]", "", text)

    # ---------------------------------
    # Remove "ال" at start of words
    # ---------------------------------
    words = text.split()

    normalized_words = []

    for w in words:

        if w.startswith("ال") and len(w) > 3:
            w = w[2:]

        normalized_words.append(w)

    text = " ".join(normalized_words)

    # ---------------------------------
    # Remove extra spaces
    # ---------------------------------
    text = re.sub(r"\s+", " ", text)

    return text.strip()