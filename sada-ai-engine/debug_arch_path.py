"""
Full System Test

Tests:
- audio preprocessing
- emotional detection
- articulation preprocessing
- word articulation detection
"""

import soundfile as sf

from app.services.global_preprocess.audio_preprocess import preprocess_audio
from app.services.psychological_safety.acoustic_features import extract_acoustic_features
from app.services.psychological_safety.emotional_decision import emotional_decision

from app.services.articulation.articulation_preprocess import articulation_preprocess
from app.services.articulation.word_engine import detect_word_level


# --------------------------------------
# CONFIG
# --------------------------------------

audio_path = "سمكة.wav"        # غيري هنا
target_word = "سمكة"
index_from_right = 3           # س


# --------------------------------------
# LOAD AUDIO
# --------------------------------------

print("\nLoading audio...")

with open(audio_path, "rb") as f:
    audio_bytes = f.read()

print("Audio loaded")


# --------------------------------------
# GLOBAL PREPROCESS
# --------------------------------------

print("\nRunning global preprocess...")

global_data = preprocess_audio(audio_bytes)

waveform = global_data["waveform"]
sample_rate = global_data["sample_rate"]

print("Waveform length:", len(waveform))
print("Sample rate:", sample_rate)


# --------------------------------------
# EMOTIONAL FEATURES
# --------------------------------------

print("\nExtracting acoustic features...")

features = extract_acoustic_features(
    waveform,
    sample_rate
)

print("Acoustic features:", features)


# --------------------------------------
# EMOTIONAL DECISION
# --------------------------------------

print("\nRunning emotional decision...")

anxiety = emotional_decision(
    features=features,
    session_count=1,
    baseline=None
)

print("Anxiety detected:", anxiety)


# --------------------------------------
# ARTICULATION PREPROCESS
# --------------------------------------

print("\nRunning articulation preprocess...")

enhanced = articulation_preprocess(global_data)

y = enhanced["enhanced_waveform"]
sr = enhanced["sample_rate"]

print("Enhanced waveform ready")


# --------------------------------------
# WORD ARTICULATION
# --------------------------------------

print("\nRunning word articulation engine...")

result = detect_word_level(
    y=y,
    sr=sr,
    target_word=target_word,
    index_from_right=index_from_right
)

print("\n========== FINAL RESULT ==========")
print(result)