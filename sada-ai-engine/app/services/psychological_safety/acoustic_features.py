"""
Acoustic Emotional Feature Extraction

Extracts clinically relevant voice stability indicators
for anxiety detection.

Features:
- mean_f0
- jitter
- shimmer
- hnr
- energy deviation
"""

import numpy as np
import librosa
import parselmouth
from parselmouth.praat import call


def safe_float(value, default=0.0):
    """
    Ensures returned value is a valid float.
    Replaces NaN or None with default.
    """
    if value is None:
        return default
    if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
        return default
    return float(value)


def extract_acoustic_features(y, sr):
    """
    Extract emotional-related acoustic features.

    Parameters:
        y  -> waveform (numpy array)
        sr -> sample rate

    Returns:
        dict with acoustic indicators
    """

    # ---------------------------------------------------------
    # If signal too short, return safe defaults
    # ---------------------------------------------------------
    if len(y) < sr * 0.3:  # less than 300 ms
        return {
            "mean_f0": 0.0,
            "jitter": 0.0,
            "shimmer": 0.0,
            "hnr": 0.0,
            "energy_dev": 0.0
        }

    # ---------------------------------------------------------
    # Convert waveform to Praat Sound object
    # ---------------------------------------------------------
    sound = parselmouth.Sound(y, sr)

    # ---------------------------------------------------------
    # Fundamental Frequency (F0)
    # ---------------------------------------------------------
    pitch = call(sound, "To Pitch", 0.0, 75, 600)

    f0_values = pitch.selected_array["frequency"]
    f0_values = f0_values[f0_values > 0]  # keep only voiced frames

    if len(f0_values) > 0:
        mean_f0 = np.mean(f0_values)
    else:
        mean_f0 = 0.0

    # ---------------------------------------------------------
    # Jitter & Shimmer
    # ---------------------------------------------------------
    try:
        point_process = call(sound, "To PointProcess (periodic, cc)", 75, 600)

        jitter = call(
            point_process,
            "Get jitter (local)",
            0, 0, 0.0001, 0.02, 1.3
        )

        shimmer = call(
            [sound, point_process],
            "Get shimmer (local)",
            0, 0, 0.0001, 0.02, 1.3, 1.6
        )

    except Exception:
        # If Praat fails (unvoiced / noisy audio)
        jitter = 0.0
        shimmer = 0.0

    # ---------------------------------------------------------
    # Harmonics-to-Noise Ratio (HNR)
    # ---------------------------------------------------------
    try:
        harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
        hnr = call(harmonicity, "Get mean", 0, 0)
    except Exception:
        hnr = 0.0

    # ---------------------------------------------------------
    # Energy deviation (RMS standard deviation)
    # ---------------------------------------------------------
    rms = librosa.feature.rms(y=y)[0]
    energy_dev = np.std(rms)

    # ---------------------------------------------------------
    # Return safe numeric values
    # ---------------------------------------------------------
    return {
        "mean_f0": safe_float(mean_f0),
        "jitter": safe_float(jitter),
        "shimmer": safe_float(shimmer),
        "hnr": safe_float(hnr),
        "energy_dev": safe_float(energy_dev)
    }
    