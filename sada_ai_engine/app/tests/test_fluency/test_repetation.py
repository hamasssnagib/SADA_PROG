import numpy as np

from app.services.fluency.repetition_detection import detect_repetition

def test_detect_repetition():

    sr = 16000

    # -------------------------------
    # 1️⃣ Repeated segments (should detect)
    # -------------------------------
    base_segment = np.random.randn(4000)

    y_repeat = np.concatenate([
        base_segment,
        np.zeros(1000),
        base_segment,   # نفس السيجنال → repetition
        np.zeros(1000),
        np.random.randn(4000)
    ])

    intervals_repeat = np.array([
        [0, 4000],
        [5000, 9000],
        [10000, 14000]
    ])

    result_repeat = detect_repetition(y_repeat, sr, intervals_repeat)

    assert "repetition_count" in result_repeat
    assert "similarities" in result_repeat

    assert result_repeat["repetition_count"] >= 1
    assert len(result_repeat["similarities"]) > 0


    # -------------------------------
    # 2️⃣ Different segments (no repetition)
    # -------------------------------
    y_diff = np.concatenate([
        np.random.randn(4000),
        np.zeros(1000),
        np.random.randn(4000),
        np.zeros(1000),
        np.random.randn(4000)
    ])

    intervals_diff = np.array([
        [0, 4000],
        [5000, 9000],
        [10000, 14000]
    ])

    result_diff = detect_repetition(y_diff, sr, intervals_diff)

    assert result_diff["repetition_count"] == 0


    # -------------------------------
    # 3️⃣ Very short segments (should skip)
    # -------------------------------
    y_short = np.random.randn(1000)

    intervals_short = np.array([
        [0, 200],
        [300, 500]
    ])

    result_short = detect_repetition(y_short, sr, intervals_short)

    assert result_short["repetition_count"] == 0


    # -------------------------------
    # 4️⃣ Long segments (should skip)
    # -------------------------------
    y_long = np.random.randn(50000)

    intervals_long = np.array([
        [0, 30000],
        [31000, 49000]
    ])

    result_long = detect_repetition(y_long, sr, intervals_long)

    assert result_long["repetition_count"] == 0


    print("🔥 Repetition detection tests passed!")


# تشغيل التست
test_detect_repetition()