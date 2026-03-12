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
# """
# Phoneme Converter (Robust Arabic Version)

# Converts Arabic words into normalized phoneme sequences
# compatible with Allosaurus phoneme outputs.
# """

# import epitran
# import re

# epi = epitran.Epitran('ara-Arab')


# # --------------------------------------------------
# # Normalize Arabic text
# # --------------------------------------------------

# def normalize_arabic(word):

#     """
#     Removes Arabic diacritics and normalizes characters.
#     """

#     word = re.sub(r"[ًٌٍَُِّْـ]", "", word)

#     # normalize variants
#     word = word.replace("أ", "ا")
#     word = word.replace("إ", "ا")
#     word = word.replace("آ", "ا")

#     # remove ta marbuta
#     word = word.replace("ة", "")

#     return word


# # --------------------------------------------------
# # Normalize IPA symbols
# # --------------------------------------------------

# def normalize_ipa(ipa_text):

#     ipa_text = ipa_text.replace("ː", "")

#     ipa_text = ipa_text.replace("ṣ", "sˤ")
#     ipa_text = ipa_text.replace("ḍ", "dˤ")
#     ipa_text = ipa_text.replace("ṭ", "tˤ")
#     ipa_text = ipa_text.replace("ẓ", "ðˤ")

#     ipa_text = ipa_text.replace("ˈ", "")
#     ipa_text = ipa_text.replace("ˌ", "")

#     return ipa_text


# # --------------------------------------------------
# # Remove vowels
# # --------------------------------------------------

# def remove_vowels(ipa_text):

#     vowels_pattern = r"[aeiouɪʊəɛæɑɒ]"

#     return re.sub(vowels_pattern, "", ipa_text)


# # --------------------------------------------------
# # Tokenize IPA correctly
# # --------------------------------------------------

# def tokenize_ipa(ipa_text):

#     tokens = []
#     i = 0

#     while i < len(ipa_text):

#         # emphatic consonants
#         if i + 1 < len(ipa_text) and ipa_text[i + 1] == "ˤ":

#             tokens.append(ipa_text[i] + "ˤ")
#             i += 2

#         else:

#             tokens.append(ipa_text[i])
#             i += 1

#     return tokens


# # --------------------------------------------------
# # Main function
# # --------------------------------------------------

# def arabic_to_phoneme_sequence(word):

#     """
#     Converts Arabic word → phoneme sequence
#     """

#     word = normalize_arabic(word)

#     ipa = epi.transliterate(word)

#     ipa = normalize_ipa(ipa)

#     ipa = remove_vowels(ipa)

#     phoneme_list = tokenize_ipa(ipa)

#     return phoneme_list


# # --------------------------------------------------
# # Helper (for router)
# # --------------------------------------------------

# def arabic_letter_to_ipa(letter):

#     seq = arabic_to_phoneme_sequence(letter)

#     if not seq:
#         return None

#     return seq[0]










# # Phoneme Conversion Layer

# # Converts Arabic text into normalized phoneme sequences
# # compatible with phoneme recognition models.

# # Pipeline:
# # 1) Arabic word
# # 2) IPA transliteration
# # 3) Normalize IPA
# # 4) Remove vowels
# # 5) Tokenize phonemes
# # 6) Return phoneme sequence

# # Used by:
# # - word_engine
# # - sentence_engine
# # """

# # import epitran
# # import re

# # # --------------------------------------------------
# # # Initialize Arabic transliterator
# # # --------------------------------------------------

# # epi = epitran.Epitran("ara-Arab")

# # # --------------------------------------------------
# # # Vowel list (to remove for articulation comparison)
# # # --------------------------------------------------

# # VOWELS = {
# #     "a", "e", "i", "o", "u",
# #     "ə", "ɪ", "ʊ",
# #     "ɑ", "æ"
# # }

# # # --------------------------------------------------
# # # Normalize IPA symbols
# # # Ensures compatibility with phoneme models
# # # --------------------------------------------------

# # def normalize_ipa(ipa_text: str) -> str:
# #     """
# #     Normalize IPA symbols to unified format.
# #     """

# #     ipa_text = ipa_text.replace("ː", "")

# #     ipa_text = ipa_text.replace("ṣ", "sˤ")
# #     ipa_text = ipa_text.replace("ḍ", "dˤ")
# #     ipa_text = ipa_text.replace("ṭ", "tˤ")
# #     ipa_text = ipa_text.replace("ẓ", "ðˤ")

# #     ipa_text = ipa_text.replace("ˈ", "")
# #     ipa_text = ipa_text.replace("ˌ", "")

# #     return ipa_text


# # # --------------------------------------------------
# # # Remove vowels
# # # Example:
# # # samaka → smk
# # # --------------------------------------------------

# # def remove_vowels(phoneme_list):

# #     cleaned = []

# #     for p in phoneme_list:
# #         if p not in VOWELS:
# #             cleaned.append(p)

# #     return cleaned


# # # --------------------------------------------------
# # # Tokenize IPA correctly
# # # Handles emphatic consonants (sˤ dˤ etc)
# # # --------------------------------------------------

# # def tokenize_ipa(ipa_text: str):

# #     tokens = []

# #     i = 0

# #     while i < len(ipa_text):

# #         if i + 1 < len(ipa_text) and ipa_text[i + 1] == "ˤ":

# #             tokens.append(ipa_text[i] + "ˤ")
# #             i += 2

# #         else:

# #             tokens.append(ipa_text[i])
# #             i += 1

# #     return tokens


# # # --------------------------------------------------
# # # Remove duplicates caused by long phonemes
# # # Example:
# # # s s s m m k → s m k
# # # --------------------------------------------------

# # def compress_phonemes(seq):

# #     if not seq:
# #         return seq

# #     compressed = [seq[0]]

# #     for p in seq[1:]:
# #         if p != compressed[-1]:
# #             compressed.append(p)

# #     return compressed


# # # --------------------------------------------------
# # # Main conversion function
# # # --------------------------------------------------

# # def arabic_to_phoneme_sequence(word: str, remove_vowel=True):

# #     """
# #     Converts Arabic word to phoneme sequence.

# #     Example:

# #     سمكة
# #     ↓
# #     s a m a k a
# #     ↓
# #     s m k
# #     """

# #     # Step 1: transliterate
# #     ipa = epi.transliterate(word)

# #     # Step 2: normalize
# #     ipa = normalize_ipa(ipa)

# #     # Step 3: tokenize
# #     phoneme_list = tokenize_ipa(ipa)
    
# #     phoneme_list = [
# #     p for p in phoneme_list
# #     if p not in ["ة","ا","ى","ي","و"]
# #         ]


# #     # Step 4: remove vowels
# #     if remove_vowel:
# #         phoneme_list = remove_vowels(phoneme_list)

# #     # Step 5: compress duplicates
# #     phoneme_list = compress_phonemes(phoneme_list)

# #     return phoneme_list





# # # """
# # # Phoneme Conversion Layer

# # # Converts Arabic text into normalized IPA sequence
# # # compatible with Allosaurus output.

# # # Used by:
# # # - Word Engine
# # # - Sentence Engine
# # # """

# # # import epitran
# # # import re

# # # # Initialize Arabic transliterator
# # # epi = epitran.Epitran('ara-Arab')


# # # # --------------------------------------------------
# # # # Normalize IPA to match Allosaurus style
# # # # --------------------------------------------------

# # # def normalize_ipa(ipa_text: str) -> str:
# # #     """
# # #     Cleans IPA output and unifies symbols
# # #     to match Allosaurus phoneme format.
# # #     """

# # #     # Remove vowel length marks
# # #     ipa_text = ipa_text.replace("ː", "")

# # #     # Normalize emphatics to Allosaurus style
# # #     ipa_text = ipa_text.replace("ṣ", "sˤ")
# # #     ipa_text = ipa_text.replace("ḍ", "dˤ")
# # #     ipa_text = ipa_text.replace("ṭ", "tˤ")
# # #     ipa_text = ipa_text.replace("ẓ", "ðˤ")

# # #     # Remove stress markers if any
# # #     ipa_text = ipa_text.replace("ˈ", "")
# # #     ipa_text = ipa_text.replace("ˌ", "")

# # #     return ipa_text


# # # # --------------------------------------------------
# # # # Remove short vowels (optional)
# # # # --------------------------------------------------

# # # def remove_vowels(ipa_text: str) -> str:
# # #     """
# # #     Removes short vowels to focus on consonant accuracy.
# # #     """

# # #     vowels_pattern = r"[aeiouɪʊə]"
# # #     return re.sub(vowels_pattern, "", ipa_text)


# # # # --------------------------------------------------
# # # # Tokenize IPA correctly (handles emphatics)
# # # # --------------------------------------------------

# # # def tokenize_ipa(ipa_text: str) -> list:
# # #     """
# # #     Splits IPA string into phoneme tokens.
# # #     Keeps emphatic consonants together (sˤ, dˤ, etc).
# # #     """

# # #     tokens = []
# # #     i = 0

# # #     while i < len(ipa_text):
# # #         # Handle emphatic marker
# # #         if i + 1 < len(ipa_text) and ipa_text[i + 1] == "ˤ":
# # #             tokens.append(ipa_text[i] + "ˤ")
# # #             i += 2
# # #         else:
# # #             tokens.append(ipa_text[i])
# # #             i += 1

# # #     return tokens


# # # # --------------------------------------------------
# # # # Main Conversion Function
# # # # --------------------------------------------------

# # # def arabic_to_phoneme_sequence(word: str, remove_vowel=True) -> list:
# # #     """
# # #     Converts Arabic word to phoneme sequence list.

# # #     Steps:
# # #     1) Transliterate using Epitran
# # #     2) Normalize IPA
# # #     3) Optionally remove vowels
# # #     4) Tokenize correctly
# # #     """

# # #     ipa = epi.transliterate(word)

# # #     ipa = normalize_ipa(ipa)

# # #     if remove_vowel:
# # #         ipa = remove_vowels(ipa)

# # #     phoneme_list = tokenize_ipa(ipa)

# # #     return phoneme_list







# # # # """
# # # # Phoneme Conversion Layer

# # # # Converts Arabic text into normalized IPA sequence
# # # # compatible with Allosaurus output.

# # # # Used by:
# # # # - Word Engine
# # # # - Sentence Engine
# # # # """

# # # # import epitran
# # # # import re

# # # # # Initialize Arabic transliterator
# # # # epi = epitran.Epitran('ara-Arab')


# # # # # --------------------------------------------------
# # # # # Normalize IPA to match Allosaurus style
# # # # # --------------------------------------------------
# # # # def normalize_ipa(ipa_text):
# # # #     """
# # # #     Cleans IPA output and unifies symbols
# # # #     to match Allosaurus phoneme format.
# # # #     """

# # # #     # Remove long vowel markers
# # # #     ipa_text = ipa_text.replace("ː", "")

# # # #     # Normalize emphatics if needed
# # # #     ipa_text = ipa_text.replace("ṣ", "sˤ")
# # # #     ipa_text = ipa_text.replace("ḍ", "dˤ")
# # # #     ipa_text = ipa_text.replace("ṭ", "tˤ")
# # # #     ipa_text = ipa_text.replace("ẓ", "ðˤ")

# # # #     return ipa_text


# # # # # --------------------------------------------------
# # # # # Remove vowels (optional for articulation focus)
# # # # # --------------------------------------------------
# # # # def remove_vowels(ipa_text):
# # # #     """
# # # #     Removes short vowels to focus on consonant accuracy.
# # # #     Useful in articulation comparison.
# # # #     """

# # # #     vowels_pattern = r"[aeiouɪʊə]"
# # # #     return re.sub(vowels_pattern, "", ipa_text)


# # # # # --------------------------------------------------
# # # # # Main Conversion Function
# # # # # --------------------------------------------------
# # # # def arabic_to_phoneme_sequence(word, remove_vowel=True):
# # # #     """
# # # #     Converts Arabic word to phoneme sequence list.

# # # #     Steps:
# # # #     1) Transliterate using Epitran
# # # #     2) Normalize IPA
# # # #     3) Optionally remove vowels
# # # #     4) Return list of phonemes
# # # #     """

# # # #     ipa = epi.transliterate(word)

# # # #     ipa = normalize_ipa(ipa)

# # # #     if remove_vowel:
# # # #         ipa = remove_vowels(ipa)

# # # #     # Split into phoneme tokens
# # # #     phoneme_list = list(ipa)

# # # #     return phoneme_list