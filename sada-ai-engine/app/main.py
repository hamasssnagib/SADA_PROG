import soundfile as sf

from app.services.global_preprocess.audio_preprocess import preprocess_audio
from app.services.psychological_safety.acoustic_features import extract_acoustic_features
from app.services.psychological_safety.emotional_decision import emotional_decision

from app.services.articulation.articulation_preprocess import articulation_preprocess
from app.services.articulation.word_engine import detect_word_level
from app.services.phoneme.phoneme_converter import arabic_letter_to_ipa


# -------------------------------------------------
# 1️⃣ Load audio file
# -------------------------------------------------
audio_path = "test.wav"   # حطي هنا اسم ملفك
y, sr = sf.read(audio_path)

# لو الصوت stereo نحوله mono
if len(y.shape) > 1:
    y = y.mean(axis=1)


# -------------------------------------------------
# 2️⃣ Global preprocess
# -------------------------------------------------
with open(audio_path, "rb") as f:
    audio_bytes = f.read()

global_data = preprocess_audio(audio_bytes)

print("Global preprocess done.")


# -------------------------------------------------
# 3️⃣ Emotional detection (اختياري للتجربة)
# -------------------------------------------------
features = extract_acoustic_features(
    global_data["waveform"],
    global_data["sample_rate"]
)

anxiety = emotional_decision(
    features=features,
    session_count=1,
    baseline=None
)

print("Anxiety detected:", anxiety)


# -------------------------------------------------
# 4️⃣ Define word test
# -------------------------------------------------
target_word = "سمكة"
index_from_right = 0  # مثال: س


# -------------------------------------------------
# 5️⃣ Extract target IPA
# -------------------------------------------------
idx = len(target_word) - 1 - index_from_right
letter = target_word[idx]
target_ipa = arabic_letter_to_ipa(letter)


# -------------------------------------------------
# 6️⃣ Articulation preprocess
# -------------------------------------------------
enhanced = articulation_preprocess(global_data, target_ipa)
y_enh = enhanced["enhanced_waveform"]
sr_enh = enhanced["sample_rate"]

print("Articulation preprocess done.")


# -------------------------------------------------
# 7️⃣ Word detection
# -------------------------------------------------
result = detect_word_level(
    y=y_enh,
    sr=sr_enh,
    target_word=target_word,
    index_from_right=index_from_right
)

print("Final Result:")
print(result)