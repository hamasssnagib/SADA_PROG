from fastapi.testclient import TestClient
import numpy as np
import soundfile as sf
import io

from app.api.routes.analyze_router import router
from fastapi import FastAPI

# ---------------------------------------------
# Create test app
# ---------------------------------------------
app = FastAPI()
app.include_router(router)

client = TestClient(app)


# ---------------------------------------------
# Generate fake audio file
# ---------------------------------------------
def generate_audio_file():
    y = np.random.randn(16000)
    buffer = io.BytesIO()
    sf.write(buffer, y, 16000, format='WAV')
    buffer.seek(0)
    return buffer


# ---------------------------------------------
# Mock dependencies
# ---------------------------------------------
def mock_preprocess_audio(audio_bytes):
    return {
        "waveform": np.random.randn(16000),
        "sample_rate": 16000
    }

def mock_extract_acoustic_features(y, sr):
    return {
        "mean_f0": 100,
        "jitter": 0.01,
        "shimmer": 0.02,
        "hnr": 20,
        "energy_dev": 0.5,
        "centroid": 2000,
        "duration": 1.0,
        "mfcc_summary": [0.1, 0.2]
    }

def mock_emotional_decision(features, session_count, baseline):
    return False

def mock_detect_fluency(global_data, target_text=None):
    return {
        "mode": "fluency",
        "accuracy": 80,
        "performance": {"stuttering_type": "mild", "severity": "low"},
        "details": {
            "pause_count": 2,
            "repetition_count": 1
        },
        "error_type": None
    }


# Inject mocks
import app.services.global_preprocess.audio_preprocess as gp
import app.services.psychological_safety.acoustic_features as af
import app.services.psychological_safety.emotional_decision as ed
import app.services.fluency.fluency_engine as fe

gp.preprocess_audio = mock_preprocess_audio
af.extract_acoustic_features = mock_extract_acoustic_features
ed.emotional_decision = mock_emotional_decision
fe.detect_fluency = mock_detect_fluency


# ---------------------------------------------
# TEST SUCCESS
# ---------------------------------------------
def test_analyze_success():

    audio_file = generate_audio_file()

    response = client.post(
        "/analyze",
        files={"file": ("test.wav", audio_file, "audio/wav")},
        data={
            "problem": "fluency",
            "level": "sentence",
            "level_id": 1,
            "session_number": 1,
            "attempt_number": 1,
            "session_count": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "analysis_complete"
    assert "result" in data

    result = data["result"]

    assert result["analysis"]["accuracy"] == 80
    assert result["analysis"]["block_rate"] == 2
    assert result["analysis"]["repetition_rate"] == 1


# ---------------------------------------------
# TEST INVALID FILE
# ---------------------------------------------
def test_invalid_file():

    response = client.post(
        "/analyze",
        files={"file": ("test.txt", b"not audio", "text/plain")},
        data={
            "problem": "fluency",
            "level": "sentence",
            "level_id": 1,
            "session_number": 1,
            "attempt_number": 1,
            "session_count": 1
        }
    )

    assert response.status_code == 400


# ---------------------------------------------
# TEST ANXIETY BLOCK
# ---------------------------------------------
def mock_anxiety(*args, **kwargs):
    return True

ed.emotional_decision = mock_anxiety

def test_anxiety_block():

    audio_file = generate_audio_file()

    response = client.post(
        "/analyze",
        files={"file": ("test.wav", audio_file, "audio/wav")},
        data={
            "problem": "fluency",
            "level": "sentence",
            "level_id": 1,
            "session_number": 1,
            "attempt_number": 1,
            "session_count": 5
        }
    )

    data = response.json()

    assert data["status"] == "retry_due_to_anxiety"
    assert data["analysis_blocked"] == True


print("🔥 Router tests ready!")