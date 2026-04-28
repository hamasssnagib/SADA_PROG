import numpy as np
import soundfile as sf
import io

from app.services.global_preprocess.audio_preprocess import preprocess_audio

def generate_audio_bytes(y, sr=16000):
    buffer = io.BytesIO()
    sf.write(buffer, y, sr, format='WAV')
    buffer.seek(0)
    return buffer.read()


def test_preprocess_audio():

    sr = 16000

    # -------------------------------
    # 1️⃣ Normal audio
    # -------------------------------
    y = np.random.randn(sr)
    audio_bytes = generate_audio_bytes(y, sr)

    result = preprocess_audio(audio_bytes)

    assert "waveform" in result
    assert "sample_rate" in result
    assert "duration" in result
    assert "rms_energy" in result
    assert "zero_crossing_rate" in result
    assert "spectral_centroid_mean" in result
    assert "speech_ratio" in result

    assert isinstance(result["waveform"], np.ndarray)
    assert result["sample_rate"] == 16000

    assert result["duration"] > 0
    assert result["rms_energy"] >= 0
    assert 0 <= result["speech_ratio"] <= 1


    # -------------------------------
    # 2️⃣ Silence audio
    # -------------------------------
    y_silence = np.zeros(sr)
    audio_bytes_silence = generate_audio_bytes(y_silence, sr)

    result_silence = preprocess_audio(audio_bytes_silence)

    assert result_silence["rms_energy"] == 0
    assert result_silence["speech_ratio"] == 0


    # -------------------------------
    # 3️⃣ Audio with silence edges
    # -------------------------------
    y_edges = np.concatenate([
        np.zeros(2000),
        np.random.randn(12000),
        np.zeros(2000)
    ])

    audio_bytes_edges = generate_audio_bytes(y_edges, sr)

    result_edges = preprocess_audio(audio_bytes_edges)

    # بعد trim المفروض duration تقل
    assert result_edges["duration"] < (len(y_edges) / sr)


    # -------------------------------
    # 4️⃣ Low energy audio
    # -------------------------------
    y_low = np.random.randn(sr) * 0.001
    audio_bytes_low = generate_audio_bytes(y_low, sr)

    result_low = preprocess_audio(audio_bytes_low)

    assert result_low["rms_energy"] < result["rms_energy"]


    print("🔥 Global preprocessing tests passed!")


# تشغيل التست
test_preprocess_audio()