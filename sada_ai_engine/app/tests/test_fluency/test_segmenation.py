import numpy as np

from app.services.fluency.segmentation import segmentation_pipeline

def test_segmentation_pipeline():

    sr = 16000

    # -------------------------------
    # 1️⃣ Normal speech with pauses
    # -------------------------------
    y = np.concatenate([
        np.random.randn(4000),   # كلام
        np.zeros(4000),          # pause
        np.random.randn(4000),   # كلام
        np.zeros(6000),          # pause أطول
        np.random.randn(4000)    # كلام
    ])

    result = segmentation_pipeline(y, sr)

    assert "intervals" in result
    assert "pause_count" in result
    assert "max_pause" in result
    assert "pauses" in result

    assert isinstance(result["intervals"], np.ndarray)
    assert isinstance(result["pauses"], list)

    # لازم يكون فيه pauses
    assert len(result["pauses"]) > 0

    # pause_count منطقي
    assert result["pause_count"] >= 0

    # max_pause منطقي
    assert result["max_pause"] >= 0


    # -------------------------------
    # 2️⃣ Continuous speech (no pauses)
    # -------------------------------
    y_continuous = np.random.randn(16000)

    result_cont = segmentation_pipeline(y_continuous, sr)

    assert result_cont["pause_count"] == 0
    assert result_cont["max_pause"] == 0


    # -------------------------------
    # 3️⃣ Silence only
    # -------------------------------
    y_silence = np.zeros(16000)

    result_silence = segmentation_pipeline(y_silence, sr)

    assert len(result_silence["intervals"]) == 0
    assert result_silence["pause_count"] == 0
    assert result_silence["max_pause"] == 0


    # -------------------------------
    # 4️⃣ Short pauses (not stuttering)
    # -------------------------------
    y_short = np.concatenate([
        np.random.randn(5000),
        np.zeros(1000),   # pause صغير
        np.random.randn(5000)
    ])

    result_short = segmentation_pipeline(y_short, sr)

    # pause صغيرة → مش counted
    assert result_short["pause_count"] == 0


    print("🔥 Segmentation tests passed!")


# تشغيل التست
test_segmentation_pipeline()