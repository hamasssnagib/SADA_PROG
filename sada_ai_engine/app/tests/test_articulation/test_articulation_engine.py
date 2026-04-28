import numpy as np
import pytest

from app.services.articulation.articulation_engine import detect_articulation

# =========================================================

# Mock preprocess 👑

# =========================================================

@pytest.fixture
def mock_preprocess(monkeypatch):

    def fake_preprocess(global_data):
        return {
            "enhanced_waveform": np.zeros(16000),
            "sample_rate": 16000
        }

    monkeypatch.setattr(
        "app.services.articulation.articulation_engine.articulation_preprocess",
        fake_preprocess
    )

# =========================================================

# Mock engines 👑

# =========================================================

@pytest.fixture
def mock_engines(monkeypatch):

    monkeypatch.setattr(
        "app.services.articulation.articulation_engine.detect_isolation",
        lambda y, sr, target_letter: {
            "accuracy": 80,
            "error_type": None,
            "target_phoneme": target_letter
        }
    )

    monkeypatch.setattr(
        "app.services.articulation.articulation_engine.detect_word_level",
        lambda y, sr, target_word, target_letter: {
            "accuracy": 90,
            "error_type": None,
            "word_correct": True,
            "target_phoneme": target_letter
        }
    )

    monkeypatch.setattr(
        "app.services.articulation.articulation_engine.detect_sentence_level",
        lambda y, sr, target_sentence, target_word, target_letter: {
            "accuracy": 70,
            "error_type": None,
            "word_correct": True,
            "target_phoneme": target_letter
        }
    )

# =========================================================

# 1) Isolation Route

# =========================================================

def test_articulation_isolation(mock_preprocess, mock_engines):

    result = detect_articulation(
        level="isolation",
        global_data={},
        target="س"
    )

    assert result["mode"] == "articulation"
    assert result["accuracy"] == 80
    assert result["error_type"] is None
    assert "details" in result

# =========================================================

# 2) Word Route

# =========================================================

def test_articulation_word(mock_preprocess, mock_engines):

    result = detect_articulation(
        level="word",
        global_data={},
        target="س",
        target_word="سمكة"
    )

    assert result["accuracy"] == 90
    assert result["performance"]["word_correct"] is True

# =========================================================

# 3) Sentence Route

# =========================================================

def test_articulation_sentence(mock_preprocess, mock_engines):

    result = detect_articulation(
        level="sentence",
        global_data={},
        target="س",
        target_word="سمكة",
        target_sentence="انا اكلت سمكة"
    )

    assert result["accuracy"] == 70
    assert result["performance"]["word_correct"] is True

# =========================================================

# 4) Invalid Level

# =========================================================

def test_articulation_invalid_level(mock_preprocess):

    result = detect_articulation(
        level="invalid",
        global_data={}
    )

    assert result["error_type"] == "invalid_level"
    assert result["accuracy"] == 0

# =========================================================

# 5) Unified Output Structure 👑

# =========================================================

def test_articulation_output_structure(mock_preprocess, mock_engines):

    result = detect_articulation(
        level="word",
        global_data={},
        target="س",
        target_word="سمكة"
    )

    assert "mode" in result
    assert "accuracy" in result
    assert "performance" in result
    assert "details" in result
    assert "error_type" in result