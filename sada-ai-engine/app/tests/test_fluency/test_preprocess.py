import numpy as np

from app.services.fluency import fluency_preprocess

def test_fluency_preprocess():

    # -------------------------------
    # 1️⃣ Normal audio
    # -------------------------------
    y = np.random.randn(16000)
    sr = 16000

    global_data = {
        "waveform": y,
        "sample_rate": sr
    }

    result = fluency_preprocess(global_data)

    assert "waveform" in result
    assert "sample_rate" in result
    assert "valid" in result

    assert isinstance(result["waveform"], np.ndarray)
    assert result["sample_rate"] == 16000
    assert result["waveform"].size > 0
    assert np.max(np.abs(result["waveform"])) <= 1.0
    assert isinstance(result["valid"], bool)


    # -------------------------------
    # 2️⃣ Low energy (invalid case)
    # -------------------------------
    y_low = np.zeros(16000)

    global_data_low = {
        "waveform": y_low,
        "sample_rate": 16000
    }

    result_low = fluency_preprocess(global_data_low)

    assert result_low["valid"] == False


    # -------------------------------
    # 3️⃣ Different sample rate
    # -------------------------------
    y_8k = np.random.randn(8000)

    global_data_8k = {
        "waveform": y_8k,
        "sample_rate": 8000
    }

    result_8k = fluency_preprocess(global_data_8k)

    assert result_8k["sample_rate"] == 16000


    # -------------------------------
    # 4️⃣ Silence at edges
    # -------------------------------
    y_edges = np.concatenate([
        np.zeros(2000),
        np.random.randn(12000),
        np.zeros(2000)
    ])

    global_data_edges = {
        "waveform": y_edges,
        "sample_rate": 16000
    }

    result_edges = fluency_preprocess(global_data_edges)

    # لازم يكون اتقص شوية من الأطراف
    assert len(result_edges["waveform"]) < len(y_edges)


    print("🔥 Fluency preprocessing tests passed!")


# تشغيل التست
test_fluency_preprocess()