"""
Repetition Detection (Audio-based)

Detect repeated speech segments using MFCC similarity
"""

import librosa
import numpy as np
from scipy.spatial.distance import cosine


# -------------------------------------------------
# Extract MFCC feature
# -------------------------------------------------

def extract_mfcc(y, sr):

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    return np.mean(mfcc, axis=1)


# -------------------------------------------------
# Similarity between segments
# -------------------------------------------------

def segment_similarity(seg1, seg2, sr):

    mfcc1 = extract_mfcc(seg1, sr)
    mfcc2 = extract_mfcc(seg2, sr)

    sim = 1 - cosine(mfcc1, mfcc2)

    return sim


# -------------------------------------------------
# Detect repetition
# -------------------------------------------------

def detect_repetition(y, sr, intervals, sim_threshold=0.8):

    repetition_count = 0
    similarities = []

    for i in range(len(intervals) - 1):

        start1, end1 = intervals[i]
        start2, end2 = intervals[i + 1]

        seg1 = y[start1:end1]
        seg2 = y[start2:end2]

        # 👑 حساب duration
        dur1 = (end1 - start1) / sr
        dur2 = (end2 - start2) / sr

        # 🔥 الفلترة هنا 👇
        if not (0.1 < dur1 < 1.5 and 0.1 < dur2 < 1.5):
            continue

        # skip very small segments (زيادة أمان)
        if len(seg1) < 500 or len(seg2) < 500:
            continue

        sim = segment_similarity(seg1, seg2, sr)
        similarities.append(sim)

        if sim > sim_threshold:
            repetition_count += 1

    return {
        "repetition_count": repetition_count,
        "similarities": similarities
    }