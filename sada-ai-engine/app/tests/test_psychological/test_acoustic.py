import numpy as np

# ---------------------------------------------
# Mock parselmouth + praat.call
# ---------------------------------------------
class MockSound:
    def __init__(self, y, sr):
        self.y = y
        self.sr = sr

class MockPitch:
    def __init__(self):
        self.selected_array = {
            "frequency": np.array([100, 120, 110, 0, 0])
        }

class MockHarmonicity:
    pass

def mock_call(obj, command, *args):

    if command == "To Pitch":
        return MockPitch()

    if command == "To PointProcess (periodic, cc)":
        return "point_process"

    if command == "Get jitter (local)":
        return 0.01

    if command == "Get shimmer (local)":
        return 0.02

    if command == "To Harmonicity (cc)":
        return MockHarmonicity()

    if command == "Get mean":
        return 20.0

    return 0.0


# Inject mocks
import app.services.psychological_safety.acoustic_features as af

af.parselmouth.Sound = MockSound
af.call = mock_call


# ---------------------------------------------
# TEST FUNCTION
# ---------------------------------------------
def test_extract_acoustic_features():

    sr = 16000

    # -------------------------------
    # 1️⃣ Normal audio
    # -------------------------------
    y = np.random.randn(sr)

    result = af.extract_acoustic_features(y, sr)

    assert "mean_f0" in result
    assert "jitter" in result
    assert "shimmer" in result
    assert "hnr" in result
    assert "energy_dev" in result

    assert result["mean_f0"] > 0
    assert result["jitter"] >= 0
    assert result["shimmer"] >= 0
    assert result["hnr"] >= 0


    # -------------------------------
    # 2️⃣ Very short audio (< 300ms)
    # -------------------------------
    y_short = np.random.randn(int(sr * 0.2))

    result_short = af.extract_acoustic_features(y_short, sr)

    assert result_short["mean_f0"] == 0.0
    assert result_short["jitter"] == 0.0
    assert result_short["shimmer"] == 0.0
    assert result_short["hnr"] == 0.0


    # -------------------------------
    # 3️⃣ Silent audio
    # -------------------------------
    y_silence = np.zeros(sr)

    result_silence = af.extract_acoustic_features(y_silence, sr)

    # حتى لو silent، المفروض مفيش crash
    assert isinstance(result_silence["mean_f0"], float)


    # -------------------------------
    # 4️⃣ NaN safety check
    # -------------------------------
    assert not np.isnan(result["mean_f0"])
    assert not np.isnan(result["jitter"])


    print("🔥 Acoustic feature tests passed!")


# ---------------------------------------------
# RUN TEST
# ---------------------------------------------
test_extract_acoustic_features()