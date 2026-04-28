import numpy as np

from app.services.fluency.prolongation_detection import detect_prolongation

def test_detect_prolongation():

    sr = 16000

    # -------------------------------
    # 1️⃣ Prolonged segments (should detect)
    # -------------------------------
    y = np.random.randn(20000)

    intervals = np.array([
        [0, 5000],     # 0.31 sec → عادي
        [6000, 15000], # 0.56 sec → عادي
        [16000, 30000] # 0.87 sec → prolongation
    ])

    result = detect_prolongation(y, sr, intervals)

    assert "prolongation_count" in result
    assert "durations" in result

    assert result["prolongation_count"] >= 1
    assert len(result["durations"]) == len(intervals)


    # -------------------------------
    # 2️⃣ All short segments (no prolongation)
    # -------------------------------
    intervals_short = np.array([
        [0, 2000],
        [3000, 5000],
        [6000, 8000]
    ])

    result_short = detect_prolongation(y, sr, intervals_short)

    assert result_short["prolongation_count"] == 0


    # -------------------------------
    # 3️⃣ Very long segments (should be ignored > 2s)
    # -------------------------------
    intervals_long = np.array([
        [0, 40000]  # 2.5 sec → out of valid range
    ])

    result_long = detect_prolongation(y, sr, intervals_long)

    assert result_long["prolongation_count"] == 0


    # -------------------------------
    # 4️⃣ Edge case (exact threshold)
    # -------------------------------
    threshold_samples = int(0.7 * sr)

    intervals_edge = np.array([
        [0, threshold_samples]  # exactly 0.7 sec
    ])

    result_edge = detect_prolongation(y, sr, intervals_edge)

    # حسب الكود (> threshold) مش >=
    assert result_edge["prolongation_count"] == 0


    print("🔥 Prolongation detection tests passed!")


# تشغيل التست
test_detect_prolongation()