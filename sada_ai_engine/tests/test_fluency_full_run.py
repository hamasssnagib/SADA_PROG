import os
from app.services.global_preprocess.audio_preprocess import preprocess_audio
from app.services.fluency.fluency_engine import detect_fluency


# =====================================================
# 🎯 TEST CASES
# =====================================================

TEST_CASES = [

    {
        "name": "Normal speech",
        "path": "tests/test_audio/سمكة3.wav",
        "target_text": "انا اكلت سمكة"
    },

    {
        "name": "Repetition",
        "path": "tests/test_audio/ثلثلة3.wav",
        "target_text": "انا اكلت سمكة"
    },

    {
        "name": "Prolongation",
        "path": "tests/test_audio/أينب3.wav",
        "target_text": "انا اكلت سمكة"
    },

    # {
    #     "name": "Pauses",
    #     "path": "tests/test_audio/pauses.wav",
    #     "target_text": "انا اكلت سمكة"
    # },

    # {
    #     "name": "Wrong sentence",
    #     "path": "tests/test_audio/wrong.wav",
    #     "target_text": "انا اكلت سمكة"
    # }

]


# =====================================================
# 🚀 RUN TESTS
# =====================================================

def run_all_tests():

    print("\n🔥 STARTING FLUENCY FULL TEST 🔥\n")

    for case in TEST_CASES:

        print("=" * 50)
        print(f"🎯 Running: {case['name']}")
        print("=" * 50)

        # 📦 load audio
        with open(case["path"], "rb") as f:
            audio_bytes = f.read()

        # 🧼 preprocess
        global_data = preprocess_audio(audio_bytes)

        # 🧠 run fluency engine
        result = detect_fluency(
            global_data=global_data,
            target_text=case["target_text"]
        )

        # 📊 print result
        print("\n📊 RESULT:")
        print(result)
        print("\n")


# =====================================================
# ▶️ ENTRY POINT
# =====================================================

if __name__ == "__main__":
    run_all_tests()