"""
Prolongation Detection

Detect extended speech segments (prolongation)
"""

import librosa


# -------------------------------------------------
# Detect prolongation
# -------------------------------------------------

# def detect_prolongation(y, sr, intervals, duration_threshold=0.7):

#     prolongation_count = 0
#     durations = []

#     for start, end in intervals:

#         duration = (end - start) / sr
#         durations.append(duration)

#         # 👑 فلترة + detection
#         if 0.2 < duration < 2.0 and duration > duration_threshold:
#             prolongation_count += 1

#     return {
#         "prolongation_count": prolongation_count,
#         "durations": durations
#     }


def detect_prolongation(y, sr, intervals, duration_threshold=0.9):

    prolongation_count = 0
    durations = []

    for start, end in intervals:

        duration = (end - start) / sr
        durations.append(duration)

        # 👑 لازم segment يكون طويل فعلاً ومش جملة
        if 0.3 < duration < 1.5 and duration > duration_threshold:
            prolongation_count += 1

    return {
        "prolongation_count": prolongation_count,
        "durations": durations
    }