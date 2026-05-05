import os
from app.services.articulation.articulation_engine import detect_articulation
from tests.utils.audio_generator import generate_audio
import librosa
# =====================================================

# 🎯 TEST CASES (كل المسارات)

# =====================================================

TEST_CASES = [
    
# {
# "name": "Isolation - letter ر",
# "level": "isolation",
# "text": "ررر",
# "target": "ر"
# },
# {
# "name": "Isolation - letter ي",
# "level": "isolation",
# "text": "يييي",
# "target": "ر"
# },
# {
# "name": "Isolation - letter ل",
# "level": "isolation",
# "text": "للل",
# "target": "ل"
# },
# {
# "name": "Isolation - letter ي",
# "level": "isolation",
# "text": "يييي",
# "target": "ل"
# },
# {
# "name": "Isolation - letter لالغتا",
# "level": "isolation",
# "text": "لالغتا",
# "target": "ر"
# },
# {
# "name": "Isolation - letter س",
# "level": "isolation",
# "text": "سسس",
# "target": "س"
# },
# {
# "name": "Isolation - letter ث",
# "level": "isolation",
# "text": "ثثث",
# "target": "س"
# },
# {
# "name": "Isolation - letter ت",
# "level": "isolation",
# "text": "تتت",
# "target": "س"
# },
# {
# "name": "Isolation - letter لاىنالا",
# "level": "isolation",
# "text": "لاىنالا",
# "target": "س"
# },
{
"name": "Word - سا",
"level": "word",
"text": "سا",
"target": "س",
"target_word": "سا"
},
{
"name": "Word - سو",
"level": "word",
"text": "سو",
"target": "س",
"target_word": "سو"
},
{
"name": "Word - سي",
"level": "word",
"text": "سي",
"target": "س",
"target_word": "سي"
}
# ,
# {
# "name": "Word - سمكة",
# "level": "word",
# "text": "سمكة",
# "target": "س",
# "target_word": "سمكة"
# },
# {
# "name": "Word - ثمكة",
# "level": "word",
# "text": "ثمكة",
# "target": "س",
# "target_word": "سمكة"
# },
# {
# "name": "Word - تمكة",
# "level": "word",
# "text": "تمكة",
# "target": "س",
# "target_word": "سمكة"
# },
# {
# "name": "Word - سلسلة",
# "level": "word",
# "text": "سلسلة",
# "target": "س",
# "target_word": "سمكة"
# },
# {
# "name": "Word - بلال",
# "level": "word",
# "text": "بلال",
# "target": "س",
# "target_word": "سمكة"
# },
# {
# "name": "Word - سالي",
# "level": "word",
# "text": "سالي",
# "target": "س",
# "target_word": "سمكة"
# },
# {
# "name": "Sentence - انا اكلت سمكة",
# "level": "sentence",
# "text": "انا اكلت سمكة",
# "target": "س",
# "target_word": "سمكة",
# "target_sentence": "انا اكلت سمكة"
# },
# {
# "name": "Sentence - انا اكلت ثمكة",
# "level": "sentence",
# "text": "انا اكلت ثمكة",
# "target": "س",
# "target_word": "سمكة",
# "target_sentence": "انا اكلت سمكة"
# }
# ,{
# "name": "Sentence - ماما سحاب أنا",
# "level": "sentence",
# "text": "ماما سحاب أنا",
# "target": "س",
# "target_word": "سمكة",
# "target_sentence": "انا اكلت سمكة"
# }
]

# =====================================================

# 🚀 RUN TESTS

# =====================================================

def run_all_tests():

    print("\n🔥 STARTING ARTICULATION FULL TEST 🔥\n")

    for case in TEST_CASES:

        print("=" * 50)
        print(f"🎯 Running: {case['name']}")
        print("=" * 50)

        # 📦 global data (زي الحقيقي)
        audio_path = generate_audio(case["text"])

        
        from app.services.global_preprocess.audio_preprocess import preprocess_audio

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        global_data = preprocess_audio(audio_bytes)

        # 🧠 run engine
        result = detect_articulation(
            level=case["level"],
            global_data=global_data,
            target=case.get("target"),
            target_word=case.get("target_word"),
            target_sentence=case.get("target_sentence")
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