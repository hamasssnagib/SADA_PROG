import os
from app.services.global_preprocess.audio_preprocess import preprocess_audio

# 👇 حطي هنا مسار الصوت بتاعك

AUDIO_PATH = "tests/assets/أرنب3.wav"

def run_test():

    print("\n🎧 Testing Global Preprocess...\n")

    if not os.path.exists(AUDIO_PATH):
        print("❌ File not found:", AUDIO_PATH)
        return

    # 📦 اقرأ الصوت كـ bytes
    with open(AUDIO_PATH, "rb") as f:
        audio_bytes = f.read()

    print("📦 Audio bytes size:", len(audio_bytes))

    try:
        result = preprocess_audio(audio_bytes)

        print("\n✅ SUCCESS\n")

        print("🎯 Waveform length:", len(result["waveform"]))
        print("🎯 Sample rate:", result["sample_rate"])

        print("\n📊 Features:")
        print("Duration:", result["duration"])
        print("RMS:", result["rms_energy"])
        print("ZCR:", result["zero_crossing_rate"])
        print("Spectral centroid:", result["spectral_centroid_mean"])
        print("Speech ratio:", result["speech_ratio"])

    except Exception as e:
        print("\n❌ ERROR:")
        print(str(e))

if __name__ == "__main__":
    run_test()