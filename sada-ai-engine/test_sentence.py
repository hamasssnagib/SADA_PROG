from app.services.global_preprocess.audio_preprocess import preprocess_audio
from app.services.articulation.articulation_preprocess import articulation_preprocess
from app.services.articulation.sentence_engine import detect_sentence_level


audio_path = "audio.wav"

target_sentence = "هذه سمكة جميلة"
target_word = "سمكة"
target_letter = "س"


print("\n==============================")
print("STEP 1: LOAD AUDIO")
print("==============================")

with open(audio_path, "rb") as f:
    audio_bytes = f.read()

print("Audio loaded")


print("\n==============================")
print("STEP 2: GLOBAL PREPROCESS")
print("==============================")

global_data = preprocess_audio(audio_bytes)

waveform = global_data["waveform"]
sr = global_data["sample_rate"]

print("Waveform length:", len(waveform))
print("Sample rate:", sr)


print("\n==============================")
print("STEP 3: ARTICULATION PREPROCESS")
print("==============================")

enhanced = articulation_preprocess(global_data)

y = enhanced["enhanced_waveform"]
sr = enhanced["sample_rate"]

print("Enhanced waveform length:", len(y))


print("\n==============================")
print("STEP 4: SENTENCE DETECTION")
print("==============================")

result = detect_sentence_level(
    y=y,
    sr=sr,
    target_sentence=target_sentence,
    target_word=target_word,
    target_letter=target_letter
)

print("\nResult:")
print(result)


print("\n==============================")
print("SENTENCE TEST FINISHED")
print("==============================")