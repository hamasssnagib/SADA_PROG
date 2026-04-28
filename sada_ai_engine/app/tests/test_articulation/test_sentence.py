import numpy as np
import pytest

from app.services.articulation.sentence_engine import detect_sentence_level


# ---------------------------------------------------------
# Mock ASR
# ---------------------------------------------------------

@pytest.fixture
def mock_asr(monkeypatch):

    def fake_asr(y, sr):
        return "انا اكلت سمكة"

    monkeypatch.setattr(
        "app.services.articulation.sentence_engine.transcribe_audio",
        fake_asr
    )


# ---------------------------------------------------------
# 1) Success Case
# ---------------------------------------------------------

def test_sentence_success(mock_asr):

    y = np.zeros(16000)
    sr = 16000

    result = detect_sentence_level(
        y,
        sr,
        target_sentence="انا اكلت سمكة",
        target_word="سمكة",
        target_letter="س"
    )

    assert result["error_type"] is None
    assert result["accuracy"] >= 0
    assert result["detected_word"] == "سمكة"


# ---------------------------------------------------------
# 2) No Speech
# ---------------------------------------------------------

def test_sentence_no_speech(monkeypatch):

    def fake_asr(y, sr):
        return ""

    monkeypatch.setattr(
        "app.services.articulation.sentence_engine.transcribe_audio",
        fake_asr
    )

    y = np.zeros(16000)
    sr = 16000

    result = detect_sentence_level(
        y,
        sr,
        target_sentence="انا اكلت سمكة",
        target_word="سمكة",
        target_letter="س"
    )

    assert result["error_type"] == "no_speech_detected"


# ---------------------------------------------------------
# 3) Target Word Not Found
# ---------------------------------------------------------

def test_sentence_target_not_found(monkeypatch):

    def fake_asr(y, sr):
        return "انا شربت لبن"

    monkeypatch.setattr(
        "app.services.articulation.sentence_engine.transcribe_audio",
        fake_asr
    )

    y = np.zeros(16000)
    sr = 16000

    result = detect_sentence_level(
        y,
        sr,
        target_sentence="انا اكلت سمكة",
        target_word="سمكة",
        target_letter="س"
    )

    assert result["error_type"] == "target_word_not_found"


# ---------------------------------------------------------
# 4) Wrong Word Spoken
# ---------------------------------------------------------

def test_sentence_wrong_word(monkeypatch):

    def fake_asr(y, sr):
        return "انا اكلت قطة"

    monkeypatch.setattr(
        "app.services.articulation.sentence_engine.transcribe_audio",
        fake_asr
    )

    y = np.zeros(16000)
    sr = 16000

    result = detect_sentence_level(
        y,
        sr,
        target_sentence="انا اكلت سمكة",
        target_word="سمكة",
        target_letter="س"
    )

    assert result["error_type"] == "wrong_word_spoken"


# ---------------------------------------------------------
# 5) Invalid Exercise
# ---------------------------------------------------------

def test_sentence_invalid_exercise():

    y = np.zeros(16000)
    sr = 16000

    result = detect_sentence_level(
        y,
        sr,
        target_sentence="انا اكلت سمكة",
        target_word="سمكة",
        target_letter="ز"   # مش موجود
    )

    assert result["error_type"] == "invalid_target_configuration"
    assert result["accuracy"] is None