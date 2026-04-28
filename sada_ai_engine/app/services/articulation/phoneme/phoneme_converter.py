import epitran
import re

from app.services.text.text_cleaner import clean_arabic_text

epi = epitran.Epitran("ara-Arab")


def arabic_to_phoneme_sequence(text):

    text = clean_arabic_text(text)

    ipa = epi.transliterate(text)

    ipa = ipa.replace("ː", "")

    vowels = r"[aeiouɪʊəɒɛæɑ]"

    ipa = re.sub(vowels, "", ipa)

    phonemes = list(ipa)

    return phonemes



