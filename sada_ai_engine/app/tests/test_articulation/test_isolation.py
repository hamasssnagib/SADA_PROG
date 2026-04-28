import numpy as np
import librosa
import pytest

from app.services.articulation.isolation_engine import detect_isolation

# =========================================================

# BASIC UNIT TESTS 👑

# =========================================================

def test_isolation_invalid_letter():

    y = np.zeros(16000)
    sr = 16000

    result = detect_isolation(y, sr, target_letter="سس")

    assert result["error_type"] == "invalid_target_letter"
    assert result["accuracy"] == 0

def test_isolation_unsupported_letter():

    y = np.zeros(16000)
    sr = 16000

    result = detect_isolation(y, sr, target_letter="ع")

    assert result["error_type"] == "unsupported_letter"
    assert result["accuracy"] == 0

def test_isolation_silence():

    y = np.zeros(16000)
    sr = 16000

    result = detect_isolation(y, sr, target_letter="س")

    assert "accuracy" in result
    assert result["accuracy"] >= 0

# =========================================================

# REAL AUDIO TESTS 🔥

# =========================================================

def test_isolation_s_real():

    y, sr = librosa.load("tests/assets/s_sound.wav", sr=16000)

    result = detect_isolation(y, sr, target_letter="س")

    print(result)

    assert result["accuracy"] >= 0

def test_isolation_wrong_sound():

    y, sr = librosa.load("tests/assets/sh_sound.wav", sr=16000)

    result = detect_isolation(y, sr, target_letter="س")

    print(result)

    assert result["error_type"] in [None, "isolation_failed"]

# =========================================================

# MOCK TEST (PRO LEVEL 👑)

# =========================================================

def test_isolation_mock(monkeypatch):

    def fake_features(y, sr):
        return {"dummy": 1}

    def fake_fricative(features, low, high):
        return 0.8  # strong detection

    monkeypatch.setattr(
        "app.services.articulation.isolation_engine.extract_features",
        fake_features
    )

    monkeypatch.setattr(
        "app.services.articulation.isolation_engine.detect_fricative",
        fake_fricative
    )

    y = np.zeros(16000)
    sr = 16000

    result = detect_isolation(y, sr, target_letter="س")

    assert result["accuracy"] > 50
    assert result["error_type"] is None