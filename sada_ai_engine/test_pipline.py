import soundfile as sf

from app.services.global_preprocess.audio_preprocess import preprocess_audio

from app.services.psychological_safety.acoustic_features import extract_acoustic_features
from app.services.psychological_safety.emotional_decision import emotional_decision

from app.services.articulation.articulation_preprocess import articulation_preprocess

from app.services.asr.asr_engine import transcribe_audio

from app.services.text.text_cleaner import clean_arabic_text
from app.services.text.word_validator import validate_spoken_word

from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
from app.services.phoneme.phoneme_detector import detect_phoneme_errors


# =====================================================
# CONFIG
# =====================================================

audio_path = "أينب3.wav"

target_word = "أرنب"
target_letter = "ر"

session_count = 1

baseline_mean_f0 = None
baseline_std_f0 = None


print("\n==============================")
print("STEP 1: LOAD AUDIO")
print("==============================")

with open(audio_path, "rb") as f:
    audio_bytes = f.read()

print("Audio loaded ✔")


# =====================================================
# STEP 2
# GLOBAL PREPROCESS
# =====================================================

print("\n==============================")
print("STEP 2: GLOBAL PREPROCESS")
print("==============================")

global_data = preprocess_audio(audio_bytes)

waveform = global_data["waveform"]
sr = global_data["sample_rate"]

print("Waveform length:", len(waveform))
print("Sample rate:", sr)


# =====================================================
# STEP 3
# EMOTIONAL FEATURES
# =====================================================

print("\n==============================")
print("STEP 3: EMOTIONAL FEATURES")
print("==============================")

features = extract_acoustic_features(waveform, sr)

print("Acoustic features:")
print(features)


# =====================================================
# STEP 4
# EMOTIONAL DECISION
# =====================================================

print("\n==============================")
print("STEP 4: EMOTIONAL DECISION")
print("==============================")

baseline = None

if baseline_mean_f0 and baseline_std_f0:

    baseline = {

        "mean_f0": baseline_mean_f0,
        "std_f0": baseline_std_f0
    }

anxiety = emotional_decision(

    features=features,
    session_count=session_count,
    baseline=baseline
)

print("Anxiety detected:", anxiety)


# =====================================================
# STEP 5
# ARTICULATION PREPROCESS
# =====================================================

print("\n==============================")
print("STEP 5: ARTICULATION PREPROCESS")
print("==============================")

enhanced = articulation_preprocess(global_data)

y = enhanced["enhanced_waveform"]
sr = enhanced["sample_rate"]

print("Enhanced waveform length:", len(y))


# =====================================================
# STEP 6
# ASR
# =====================================================

print("\n==============================")
print("STEP 6: ASR")
print("==============================")

recognized_text = transcribe_audio(y, sr)

print("Recognized text:", recognized_text)


# =====================================================
# STEP 7
# TEXT CLEANING
# =====================================================

print("\n==============================")
print("STEP 7: TEXT CLEANING")
print("==============================")

clean_text = clean_arabic_text(recognized_text)

print("Clean text:", clean_text)


# =====================================================
# STEP 8
# WORD VALIDATION
# =====================================================

print("\n==============================")
print("STEP 8: WORD VALIDATION")
print("==============================")

valid, similarity_score, spoken_word = validate_spoken_word(

    clean_text,
    target_word,
    target_letter
)

print("Validation result:", valid)
print("Similarity score:", similarity_score)
print("Spoken word:", spoken_word)


if not valid:

    print("\n❌ Wrong word spoken — stopping pipeline")

    exit()


# =====================================================
# STEP 9
# PHONEME CONVERSION
# =====================================================

print("\n==============================")
print("STEP 9: PHONEME CONVERSION")
print("==============================")

expected_seq = arabic_to_phoneme_sequence(target_word)

spoken_seq = arabic_to_phoneme_sequence(spoken_word)

print("Expected phonemes:", expected_seq)
print("Spoken phonemes:", spoken_seq)


# =====================================================
# STEP 10
# TARGET PHONEME
# =====================================================

print("\n==============================")
print("STEP 10: TARGET PHONEME")
print("==============================")

target_phoneme = arabic_to_phoneme_sequence(target_letter)[0]

print("Target phoneme:", target_phoneme)


# =====================================================
# STEP 11
# PHONEME DETECTION
# =====================================================

print("\n==============================")
print("STEP 11: PHONEME DETECTION")
print("==============================")

detection = detect_phoneme_errors(

    expected_seq,
    spoken_seq,
    target_phoneme
)

print("Detection result:")
print(detection)


# =====================================================
# FINAL RESULT
# =====================================================

print("\n==============================")
print("PIPELINE FINISHED")
print("==============================")

print("Final Accuracy:", detection["accuracy"])
print("Errors:", detection["errors"])










# import soundfile as sf

# from app.services.global_preprocess.audio_preprocess import preprocess_audio
# from app.services.psychological_safety.acoustic_features import extract_acoustic_features
# from app.services.psychological_safety.emotional_decision import emotional_decision

# from app.services.articulation.articulation_preprocess import articulation_preprocess

# from app.services.asr.asr_engine import transcribe_audio

# from app.services.text.text_cleaner import clean_arabic_text

# from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# from app.services.phoneme.phoneme_detector import detect_phoneme_errors


# # =========================================
# # CONFIG
# # =========================================

# audio_path = "سلسلة3.wav"
# target_word = "سمكة"
# target_letter = "س"

# session_count = 1

# baseline = None


# # =========================================
# # STEP 1
# # LOAD AUDIO
# # =========================================

# print("\n==============================")
# print("STEP 1: LOAD AUDIO")
# print("==============================")

# with open(audio_path, "rb") as f:
#     audio_bytes = f.read()

# print("Audio loaded")


# # =========================================
# # STEP 2
# # GLOBAL PREPROCESS
# # =========================================

# print("\n==============================")
# print("STEP 2: GLOBAL PREPROCESS")
# print("==============================")

# global_data = preprocess_audio(audio_bytes)

# waveform = global_data["waveform"]
# sr = global_data["sample_rate"]

# print("Waveform length:", len(waveform))
# print("Sample rate:", sr)


# # =========================================
# # STEP 3
# # EMOTION FEATURES
# # =========================================

# print("\n==============================")
# print("STEP 3: EMOTIONAL FEATURES")
# print("==============================")

# features = extract_acoustic_features(
#     waveform,
#     sr
# )

# print("Acoustic features:")
# print(features)


# # =========================================
# # STEP 4
# # EMOTIONAL DECISION
# # =========================================

# print("\n==============================")
# print("STEP 4: EMOTIONAL DECISION")
# print("==============================")

# anxiety = emotional_decision(
#     features=features,
#     session_count=session_count,
#     baseline=baseline
# )

# print("Anxiety detected:", anxiety)


# # =========================================
# # STEP 5
# # ARTICULATION PREPROCESS
# # =========================================

# print("\n==============================")
# print("STEP 5: ARTICULATION PREPROCESS")
# print("==============================")

# enhanced = articulation_preprocess(global_data)

# y = enhanced["enhanced_waveform"]
# sr = enhanced["sample_rate"]

# print("Enhanced waveform length:", len(y))


# # =========================================
# # STEP 6
# # ASR
# # =========================================

# print("\n==============================")
# print("STEP 6: ASR")
# print("==============================")

# recognized_text = transcribe_audio(y, sr)

# print("Recognized text:", recognized_text)


# # =========================================
# # STEP 7
# # TEXT CLEANER
# # =========================================

# print("\n==============================")
# print("STEP 7: TEXT CLEANING")
# print("==============================")

# clean_text = clean_arabic_text(recognized_text)

# print("Clean text:", clean_text)


# # =========================================
# # STEP 8
# # PHONEME CONVERSION
# # =========================================

# print("\n==============================")
# print("STEP 8: PHONEME CONVERSION")
# print("==============================")

# expected_seq = arabic_to_phoneme_sequence(target_word)
# spoken_seq = arabic_to_phoneme_sequence(clean_text)

# print("Expected phonemes:", expected_seq)
# print("Spoken phonemes:", spoken_seq)


# # =========================================
# # STEP 9
# # TARGET PHONEME
# # =========================================

# print("\n==============================")
# print("STEP 9: TARGET PHONEME")
# print("==============================")

# target_seq = arabic_to_phoneme_sequence(target_letter)

# target_phoneme = target_seq[0]

# print("Target phoneme:", target_phoneme)


# # =========================================
# # STEP 10
# # PHONEME DETECTION
# # =========================================

# print("\n==============================")
# print("STEP 10: PHONEME DETECTION")
# print("==============================")

# result = detect_phoneme_errors(
#     expected_seq,
#     spoken_seq,
#     target_phoneme
# )

# print("Detection result:")
# print(result)


# print("\n==============================")
# print("PIPELINE FINISHED")
# print("==============================")