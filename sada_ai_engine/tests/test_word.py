import os

from app.services.global_preprocess.audio_preprocess import preprocess_audio
from app.services.articulation.articulation_engine import detect_articulation


# ------------------------------------------
# 🎧 TEST FILES (كلمات)
# ------------------------------------------

TEST_FILES = [
    {
        "name": "سا correct",
        "path": "tests/test_audio/سا.wav",
        "target_letter": "س",
        "target_word": "سا"
    },
    {
        "name": "سو distortion ",
        "path": "tests/test_audio/سو.wav",
        "target_letter": "س",
        "target_word": "سو"
    },
    {
        "name": "سي substitution ",
        "path": "tests/test_audio/سي.wav",
        "target_letter": "س",
        "target_word": "3سمكة"
    },
    # {
    #     "name": "WRONG WORD",
    #     "path": "tests/test_audio/ماما.wav",
    #     "target_letter": "س",
    #     "target_word": "سمكة"
    # },
]


# ------------------------------------------
# 🚀 RUN TEST
# ------------------------------------------

def run_test():

    print("\n🔥 TESTING WORD AUDIO 🔥\n")

    for case in TEST_FILES:

        print("=" * 50)
        print(f"🎯 {case['name']}")
        print("=" * 50)

        # 📦 load audio
        with open(case["path"], "rb") as f:
            audio_bytes = f.read()

        # 🧼 preprocess
        global_data = preprocess_audio(audio_bytes)

        # 🧠 detect articulation (WORD LEVEL)
        result = detect_articulation(
            level="word",
            global_data=global_data,
            target=case["target_letter"],
            target_word=case["target_word"]
        )

        print("\n📊 RESULT:")
        print(result)
        print("\n")


# ------------------------------------------
# ▶️ MAIN
# ------------------------------------------

if __name__ == "__main__":
    run_test()