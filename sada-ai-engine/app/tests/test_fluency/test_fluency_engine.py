import numpy as np

from app.services.fluency.fluency_engine import detect_fluency

# ---------------------------------------------
# Mock dependencies (عشان نعزل التست)
# ---------------------------------------------

def mock_transcribe_audio(y, sr):
    return "hello world"

def mock_validate_spoken_input(recognized, target, threshold):
    return True, 0.9, recognized

def mock_fluency_decision(repetition_count, pause_count, max_pause, prolongation_count):
    return {
        "fluency_score": 0.8,
        "stuttering_type": "mild",
        "severity": "low"
    }

# ---------------------------------------------
# Inject mocks
# ---------------------------------------------
transcribe_audio = mock_transcribe_audio
validate_spoken_input = mock_validate_spoken_input
fluency_decision = mock_fluency_decision


# ---------------------------------------------
# TEST FUNCTION
# ---------------------------------------------
def test_detect_fluency():

    sr = 16000

    # fake waveform (speech + pauses)
    y = np.concatenate([
        np.random.randn(4000),
        np.zeros(2000),
        np.random.randn(4000),
        np.zeros(3000),
        np.random.randn(4000)
    ])

    global_data = {
        "waveform": y,
        "sample_rate": sr
    }

    result = detect_fluency(global_data, target_text="hello world")

    # ---------------------------------------------
    # Assertions
    # ---------------------------------------------
    assert "mode" in result
    assert "accuracy" in result
    assert "performance" in result
    assert "details" in result
    assert "error_type" in result

    assert result["mode"] == "fluency"

    assert isinstance(result["accuracy"], float)

    assert "stuttering_type" in result["performance"]
    assert "severity" in result["performance"]

    assert "repetition_count" in result["details"]
    assert "pause_count" in result["details"]
    assert "max_pause" in result["details"]
    assert "prolongation_count" in result["details"]

    print("🔥 Fluency Engine Test Passed!")


# ---------------------------------------------
# RUN TEST
# ---------------------------------------------
test_detect_fluency()