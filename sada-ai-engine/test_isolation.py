import soundfile as sf

from app.services.global_preprocess.audio_preprocess import preprocess_audio
from app.services.articulation.articulation_preprocess import articulation_preprocess
from app.services.articulation.isolation_engine import detect_isolation


audio_path = "iso_s.wav"
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
print("STEP 4: ISOLATION DETECTION")
print("==============================")

result = detect_isolation(
    y=y,
    sr=sr,
    target_letter=target_letter
)

print("\nResult:")
print(result)


print("\n==============================")
print("ISOLATION TEST FINISHED")
print("==============================")