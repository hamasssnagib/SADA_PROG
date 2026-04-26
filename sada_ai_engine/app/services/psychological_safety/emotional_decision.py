"""
Emotional Decision Logic

Determines whether the current session shows anxiety
based on:
- Phase 1: Fixed clinical thresholds (first 3 sessions)
- Phase 2: Personalized baseline (after bootstrap phase)
"""

def emotional_decision(features, session_count, baseline=None):
    """
    Evaluates acoustic features to detect child anxiety.

    Parameters:
        features (dict): Extracted acoustic features (F0, Jitter, Shimmer, etc.)
        session_count (int): Number of completed sessions by the child
        baseline (dict or None): Personalized baseline (mean and std of F0)

    Returns:
        bool: True if anxiety is detected, False otherwise
    """

    # -------------------------------------------------
    # PHASE 1: Bootstrap (First 3 Sessions)
    # Using fixed clinical thresholds tuned for children
    # -------------------------------------------------
    if session_count < 3:
        
        # Jitter and Shimmer are percentages (e.g., 0.03 = 3%)
        # Mean F0 > 350Hz is a strong indicator of high stress/crying in children
        # HNR < 8 dB indicates loss of voice harmonics (choking/crying)
        if (
            features["mean_f0"] > 350 or
            features["jitter"] > 0.03 or
            features["shimmer"] > 0.05 or
            features["hnr"] < 8
        ):
            return True

        return False

    # -------------------------------------------------
    # PHASE 2: Personalized Baseline
    # Using Z-Score to detect abnormal shifts in the child's voice
    # -------------------------------------------------
    if baseline is not None:

        mean = baseline.get("mean_f0", 0)
        std = baseline.get("std_f0", 0)

        if std > 0:
            # Calculate Z-score to measure deviation from the child's normal pitch
            z_score = abs((features["mean_f0"] - mean) / std)

            # If the pitch deviates by more than 2 standard deviations, flag as anxiety
            if z_score > 2:
                return True

    # Return False if no anxiety indicators are triggered
    return False






# """
# Emotional Decision Logic

# Determines whether current session shows anxiety
# based on:
# - Fixed thresholds (first 3 sessions)
# - Personalized baseline (after bootstrap)
# """

# def emotional_decision(features, session_count, baseline=None):
#     """
#     Parameters:
#         features (dict): acoustic features
#         session_count (int): number of completed sessions
#         baseline (dict or None): personalized baseline

#     Returns:
#         bool → True if anxiety detected
#     """

#     # -------------------------------------------------
#     # PHASE 1: Bootstrap (First 3 Sessions)
#     # -------------------------------------------------
#     if session_count < 3:

#         if (
#             features["mean_f0"] > 400 or
#             features["jitter"] > 3 or
#             features["shimmer"] > 5 or
#             features["hnr"] < 8
#         ):
#             return True

#         return False

#     # -------------------------------------------------
#     # PHASE 2: Personalized Baseline
#     # -------------------------------------------------
#     if baseline is not None:

#         mean = baseline.get("mean_f0", 0)
#         std = baseline.get("std_f0", 0)

#         if std > 0:
#             z_score = abs((features["mean_f0"] - mean) / std)

#             if z_score > 2:
#                 return True

#     return False