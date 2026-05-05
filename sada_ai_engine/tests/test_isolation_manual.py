import os
from app.services.global_preprocess.audio_preprocess import preprocess_audio
from app.services.articulation.articulation_engine import detect_articulation

# ------------------------------------------
# 🎧 حطي هنا مسارات الفايلات بتاعتك
# ------------------------------------------

TEST_FILES = [
    {
        "name": "RAA correct",
        "path": "tests/test_audio/ر.wav",
        "target": "ر"
    },
    {
        "name": "LAM correct",
        "path": "tests/test_audio/ل.wav",
        "target": "ل"
    },
    {
        "name": "SEEN correct",
        "path": "tests/test_audio/س.wav",
        "target": "س"
    },
    {
        "name": "SEEN correct",
        "path": "tests/test_audio/سمكة3.wav",
        "target": "س"
    },
]

# ------------------------------------------
# 🚀 RUN
# ------------------------------------------

def run_test():

    print("\n🔥 TESTING REAL AUDIO FILES 🔥\n")

    for case in TEST_FILES:

        print("=" * 50)
        print(f"🎯 {case['name']}")
        print("=" * 50)

        # 📦 load audio
        with open(case["path"], "rb") as f:
            audio_bytes = f.read()

        # 🧼 preprocess
        global_data = preprocess_audio(audio_bytes)

        # 🧠 run articulation
        result = detect_articulation(
            level="isolation",
            global_data=global_data,
            target=case["target"]
        )

        print("\n📊 RESULT:")
        print(result)
        print("\n")


if __name__ == "__main__":
    run_test()