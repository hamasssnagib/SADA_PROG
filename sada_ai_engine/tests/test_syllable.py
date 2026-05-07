import os

from app.services.global_preprocess.audio_preprocess import preprocess_audio

from app.services.articulation.syllable_engine import (
    detect_syllable_level
)

# ------------------------------------------
# 🎧 TEST FILES
# ------------------------------------------

TEST_FILES = [

    {
        "name": "SEEN syllable correct",
        "path": "tests/test_audio/سو.wav",
        "target_word": "سو",
        "target_letter": "س"
    },

    {
        "name": "LAM syllable correct",
        "path": "tests/test_audio/سي.wav",
        "target_word": "سي",
        "target_letter": "س"
    },

    {
        "name": "RAA syllable correct",
        "path": "tests/test_audio/سلسلة3.wav",
        "target_word": "سو",
        "target_letter": "س"
    },

]

# ------------------------------------------
# 🚀 RUN TEST
# ------------------------------------------

def run_test():

    print("\n🔥 TESTING SYLLABLE ENGINE 🔥\n")

    for case in TEST_FILES:

        print("=" * 50)
        print(f"🎯 {case['name']}")
        print("=" * 50)

        # ------------------------------------------
        # 📦 load audio
        # ------------------------------------------

        with open(case["path"], "rb") as f:

            audio_bytes = f.read()

        # ------------------------------------------
        # 🧼 preprocess
        # ------------------------------------------

        global_data = preprocess_audio(audio_bytes)

        # ------------------------------------------
        # 🧠 run syllable engine
        # ------------------------------------------

        result = detect_syllable_level(

            y=global_data["waveform"],
            sr=global_data["sample_rate"],

            target_word=case["target_word"],
            target_letter=case["target_letter"]
        )

        # ------------------------------------------
        # 📊 print result
        # ------------------------------------------

        print("\n📊 RESULT:")
        print(result)
        print("\n")


# ------------------------------------------
# ▶️ START
# ------------------------------------------

if __name__ == "__main__":

    run_test()