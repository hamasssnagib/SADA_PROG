"""
Fluency Segmentation

Split audio into speech segments and detect pauses


[segment, segment, segment]
كل segment = جزء فيه كلام
والفراغ بينهم = pause
"""

import librosa


# -------------------------------------------------
# Get speech segments
# -------------------------------------------------

def get_speech_segments(y, sr, top_db=20):
    """
    Returns speech intervals (non-silent parts)

    Output:
        [(start, end), ...] in samples
    """

    intervals = librosa.effects.split(
        y,
        top_db=top_db
    )

    return intervals


# -------------------------------------------------
# Detect pauses between segments
# -------------------------------------------------

def detect_pauses(intervals, sr):
    """
    Detect pauses between speech segments

    Output:
        pause_count
        max_pause
        pauses_list
    """

    pauses = []

    for i in range(len(intervals) - 1):

        end_current = intervals[i][1]
        start_next = intervals[i + 1][0]

        gap = start_next - end_current
        gap_sec = gap / sr

        pauses.append(gap_sec)

    pause_count = sum(1 for p in pauses if p > 0.5)
    max_pause = max(pauses) if pauses else 0

    return {
        "pause_count": pause_count,
        "max_pause": max_pause,
        "pauses": pauses
    }


# -------------------------------------------------
# Full segmentation pipeline
# -------------------------------------------------

def segmentation_pipeline(y, sr):

    intervals = get_speech_segments(y, sr)

    pause_info = detect_pauses(intervals, sr)

    return {
        "intervals": intervals,
        "pause_count": pause_info["pause_count"],
        "max_pause": pause_info["max_pause"],
        "pauses": pause_info["pauses"]
    }