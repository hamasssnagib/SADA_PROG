import app.services.psychological_safety.emotional_decision as emotional_decision
def test_emotional_decision():

    # -------------------------------
    # 1️⃣ Phase 1: Bootstrap (no anxiety)
    # -------------------------------
    features_normal = {
        "mean_f0": 200,
        "jitter": 0.01,
        "shimmer": 0.02,
        "hnr": 15
    }

    result = emotional_decision(
        features=features_normal,
        session_count=1
    )

    assert result == False


    # -------------------------------
    # 2️⃣ Phase 1: High F0 (anxiety)
    # -------------------------------
    features_high_f0 = {
        "mean_f0": 400,
        "jitter": 0.01,
        "shimmer": 0.02,
        "hnr": 15
    }

    result = emotional_decision(features_high_f0, session_count=1)

    assert result == True


    # -------------------------------
    # 3️⃣ Phase 1: High jitter (anxiety)
    # -------------------------------
    features_high_jitter = {
        "mean_f0": 200,
        "jitter": 0.05,
        "shimmer": 0.02,
        "hnr": 15
    }

    result = emotional_decision(features_high_jitter, session_count=2)

    assert result == True


    # -------------------------------
    # 4️⃣ Phase 1: Low HNR (anxiety)
    # -------------------------------
    features_low_hnr = {
        "mean_f0": 200,
        "jitter": 0.01,
        "shimmer": 0.02,
        "hnr": 5
    }

    result = emotional_decision(features_low_hnr, session_count=2)

    assert result == True


    # -------------------------------
    # 5️⃣ Phase 2: Within baseline (no anxiety)
    # -------------------------------
    baseline = {
        "mean_f0": 200,
        "std_f0": 20
    }

    features_ok = {
        "mean_f0": 220,  # داخل النطاق
        "jitter": 0.01,
        "shimmer": 0.02,
        "hnr": 15
    }

    result = emotional_decision(
        features_ok,
        session_count=5,
        baseline=baseline
    )

    assert result == False


    # -------------------------------
    # 6️⃣ Phase 2: High deviation (anxiety)
    # -------------------------------
    features_deviation = {
        "mean_f0": 300,  # بعيد جدًا عن baseline
        "jitter": 0.01,
        "shimmer": 0.02,
        "hnr": 15
    }

    result = emotional_decision(
        features_deviation,
        session_count=5,
        baseline=baseline
    )

    assert result == True


    # -------------------------------
    # 7️⃣ Phase 2: No baseline (fallback)
    # -------------------------------
    result = emotional_decision(
        features_ok,
        session_count=5,
        baseline=None
    )

    assert result == False


    # -------------------------------
    # 8️⃣ Edge case: std = 0
    # -------------------------------
    baseline_zero_std = {
        "mean_f0": 200,
        "std_f0": 0
    }

    result = emotional_decision(
        features_deviation,
        session_count=5,
        baseline=baseline_zero_std
    )

    # مفيش division → safe
    assert result == False


    print("🔥 Emotional decision tests passed!")


# تشغيل التست
test_emotional_decision()