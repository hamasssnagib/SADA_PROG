import soundfile as sf

from app.services.global_preprocess.audio_preprocess import preprocess_audio
from app.services.articulation.articulation_preprocess import articulation_preprocess

from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
from app.services.phoneme.phoneme_detector import normalize_stream, evaluate_phoneme_alignment

from app.models_loader import whisper_model, allosaurus_model


# =================================
# CONFIG
# =================================

audio_path = "ثلثلة.wav"
target_word = "سلسلة"
target_letter = "س"


print("\n==============================")
print("STEP 1: LOAD AUDIO")
print("==============================")

with open(audio_path, "rb") as f:
    audio_bytes = f.read()

global_data = preprocess_audio(audio_bytes)

waveform = global_data["waveform"]
sr = global_data["sample_rate"]

print("Waveform length:", len(waveform))
print("Sample rate:", sr)


# =================================
# STEP 2
# TARGET WORD → PHONEMES
# =================================

print("\n==============================")
print("STEP 2: TARGET WORD → PHONEMES")
print("==============================")

target_seq = arabic_to_phoneme_sequence(target_word)

print("Target word:", target_word)
print("Target phoneme sequence:", target_seq)


# =================================
# STEP 3
# TARGET LETTER → PHONEME
# =================================

print("\n==============================")
print("STEP 3: TARGET LETTER → PHONEME")
print("==============================")

letter_seq = arabic_to_phoneme_sequence(target_letter)

target_phoneme = letter_seq[0]

print("Target letter:", target_letter)
print("Target phoneme:", target_phoneme)


# =================================
# STEP 4
# WHISPER TRANSCRIPTION
# =================================

print("\n==============================")
print("STEP 4: WHISPER TRANSCRIPTION")
print("==============================")

segments, _ = whisper_model.transcribe(audio_path, language="ar")

whisper_text = " ".join([seg.text for seg in segments])

print("Whisper text:", whisper_text)


# =================================
# STEP 5
# ALLOSAURUS PHONEMES
# =================================

print("\n==============================")
print("STEP 5: ALLOSAURUS PHONEMES")
print("==============================")

result = allosaurus_model.recognize(audio_path)

phoneme_stream = result.strip().split()

print("Raw phoneme stream:")
print(phoneme_stream)


# =================================
# STEP 6
# NORMALIZED STREAM
# =================================

print("\n==============================")
print("STEP 6: NORMALIZED STREAM")
print("==============================")

normalized_stream = normalize_stream(phoneme_stream)

print("Normalized stream:")
print(normalized_stream)


# =================================
# STEP 7
# FIND TARGET POSITIONS
# =================================

print("\n==============================")
print("STEP 7: FIND TARGET POSITIONS")
print("==============================")

positions = []

for i, p in enumerate(target_seq):

    if p == target_phoneme:
        positions.append(i)

print("Target phoneme positions in word:", positions)


# =================================
# STEP 8
# ALIGNMENT TEST FOR EACH POSITION
# =================================

print("\n==============================")
print("STEP 8: ALIGNMENT TEST")
print("==============================")

best_score = -1
best_result = None

for pos in positions:

    print("\n--- Testing position:", pos)

    alignment = evaluate_phoneme_alignment(
        normalized_stream,
        target_seq,
        pos
    )

    print("Score:", alignment["score"])
    print("Expected:", alignment["expected_phoneme"])
    print("Spoken:", alignment["spoken_phoneme"])
    print("Error:", alignment["error_type"])

    if alignment["score"] > best_score:

        best_score = alignment["score"]
        best_result = alignment


# =================================
# STEP 9
# BEST RESULT
# =================================

print("\n==============================")
print("STEP 9: BEST RESULT")
print("==============================")

if best_result:

    print("Best score:", best_score)
    print("Expected phoneme:", best_result["expected_phoneme"])
    print("Spoken phoneme:", best_result["spoken_phoneme"])
    print("Error type:", best_result["error_type"])

else:

    print("No valid alignment found")


# =================================
# STEP 10
# FINAL INTERPRETATION
# =================================

print("\n==============================")
print("STEP 10: FINAL DECISION")
print("==============================")

if not best_result or best_score < 0.5:

    print("Result: WORD NOT DETECTED")

else:

    if best_result["error_type"] == "substitution":

        print("Result: SUBSTITUTION ERROR")

    elif best_result["error_type"] == "omission":

        print("Result: OMISSION ERROR")

    elif best_result["error_type"] is None:

        print("Result: CORRECT PRONUNCIATION")

    else:

        print("Result:", best_result["error_type"])