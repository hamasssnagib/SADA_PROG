"""
Emotional Decision Logic

Determines whether current session shows anxiety
based on:
- Fixed thresholds (first 3 sessions)
- Personalized baseline (after bootstrap)
"""

def emotional_decision(features, session_count, baseline=None):
    """
    Parameters:
        features (dict): acoustic features
        session_count (int): number of completed sessions
        baseline (dict or None): personalized baseline

    Returns:
        bool → True if anxiety detected
    """

    # -------------------------------------------------
    # PHASE 1: Bootstrap (First 3 Sessions)
    # -------------------------------------------------
    if session_count < 3:

        if (
            features["mean_f0"] > 400 or
            features["jitter"] > 3 or
            features["shimmer"] > 5 or
            features["hnr"] < 8
        ):
            return True

        return False

    # -------------------------------------------------
    # PHASE 2: Personalized Baseline
    # -------------------------------------------------
    if baseline is not None:

        mean = baseline.get("mean_f0", 0)
        std = baseline.get("std_f0", 0)

        if std > 0:
            z_score = abs((features["mean_f0"] - mean) / std)

            if z_score > 2:
                return True

    return False