# import numpy as np
# import pytest

# from app.services.articulation.word_engine import detect_word_level


# # ---------------------------------------------------------
# # Mock ASR علشان نتحكم في النتيجة
# # ---------------------------------------------------------

# @pytest.fixture
# def mock_asr(monkeypatch):

#     def fake_transcribe_audio(y, sr):
#         return "سمكة"

#     monkeypatch.setattr(
#         "app.services.articulation.word_engine.transcribe_audio",
#         fake_transcribe_audio
#     )


# # ---------------------------------------------------------
# # 1) Success Case
# # ---------------------------------------------------------

# def test_word_success(mock_asr):

#     y = np.zeros(16000)
#     sr = 16000

#     result = detect_word_level(
#         y, sr,
#         target_word="سمكة",
#         target_letter="س"
#     )

#     assert result["accuracy"] >= 0
#     assert result["error_type"] is None
#     assert "expected_phonemes" in result


# # ---------------------------------------------------------
# # 2) No Speech Case
# # ---------------------------------------------------------

# def test_word_no_speech(monkeypatch):

#     def fake_asr(y, sr):
#         return ""

#     monkeypatch.setattr(
#         "app.services.articulation.word_engine.transcribe_audio",
#         fake_asr
#     )

#     y = np.zeros(16000)
#     sr = 16000

#     result = detect_word_level(
#         y, sr,
#         target_word="سمكة",
#         target_letter="س"
#     )

#     assert result["error_type"] == "no_speech_detected"


# # ---------------------------------------------------------
# # 3) Wrong Word Case
# # ---------------------------------------------------------

# def test_word_wrong_word(monkeypatch):

#     def fake_asr(y, sr):
#         return "قطة"

#     monkeypatch.setattr(
#         "app.services.articulation.word_engine.transcribe_audio",
#         fake_asr
#     )

#     y = np.zeros(16000)
#     sr = 16000

#     result = detect_word_level(
#         y, sr,
#         target_word="سمكة",
#         target_letter="س"
#     )

#     assert result["error_type"] == "wrong_word_spoken"


# # ---------------------------------------------------------
# # 4) Invalid Exercise Case
# # ---------------------------------------------------------

# def test_word_invalid_exercise():

#     y = np.zeros(16000)
#     sr = 16000

#     result = detect_word_level(
#         y, sr,
#         target_word="سمكة",
#         target_letter="ز"   # مش موجود في الكلمة
#     )

#     assert result["error_type"] == "invalid_target_configuration"
#     assert result["accuracy"] is None


import librosa

from app.services.articulation.word_engine import detect_word_level


# ---------------------------------------------------------
# 1) Success (طفل قال الكلمة صح)
# ---------------------------------------------------------

def test_word_real_success():

    y, sr = librosa.load("tests/assets/correct_word.wav", sr=16000)

    result = detect_word_level(
        y, sr,
        target_word="سمكة",
        target_letter="س"
    )

    print(result)

    assert result["accuracy"] >= 0
    assert result["error_type"] is None


# ---------------------------------------------------------
# 2) Wrong word
# ---------------------------------------------------------

def test_word_real_wrong():

    y, sr = librosa.load("tests/assets/wrong_word.wav", sr=16000)

    result = detect_word_level(
        y, sr,
        target_word="سمكة",
        target_letter="س"
    )

    print(result)

    assert result["error_type"] in [
        "wrong_word_spoken",
        "substitution"
    ]


# ---------------------------------------------------------
# 3) No speech
# ---------------------------------------------------------

def test_word_real_silence():

    y, sr = librosa.load("tests/assets/no_speech.wav", sr=16000)

    result = detect_word_level(
        y, sr,
        target_word="سمكة",
        target_letter="س"
    )

    print(result)

    assert result["error_type"] == "no_speech_detected"