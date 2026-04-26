import numpy as np
import librosa
from scipy.signal import butter, lfilter


# -------------------------------------------------
# Butterworth band filter (safe)
# -------------------------------------------------

def bandpass_filter(y, sr, low=80, high=7000, order=4):

    nyq = 0.5 * sr

    low = low / nyq
    high = high / nyq

    # safety clamp
    low = max(low, 0.001)
    high = min(high, 0.999)

    if low >= high:
        return y

    b, a = butter(order, [low, high], btype="band")

    return lfilter(b, a, y)


# -------------------------------------------------
# Mild noise reduction
# -------------------------------------------------

def mild_noise_reduction(y):

    # calculate low energy threshold
    threshold = np.percentile(np.abs(y), 10)

    y_clean = y.copy()

    y_clean[np.abs(y_clean) < threshold] = 0

    return y_clean


# -------------------------------------------------
# Amplitude boost
# -------------------------------------------------

def amplitude_boost(y, boost=1.5):

    return y * boost


# -------------------------------------------------
# Safe normalization
# -------------------------------------------------

def safe_normalize(y):

    max_val = np.max(np.abs(y))

    if max_val > 0:
        y = y / max_val

    return y


# -------------------------------------------------
# Lisping Preprocess
# -------------------------------------------------

def articulation_preprocess(global_data, low_confidence=False):

    y = global_data["waveform"]
    sr = global_data["sample_rate"]

    y = y.astype(np.float32)

    # --------------------------------
    # 1️⃣ Resample to 16kHz
    # --------------------------------

    if sr != 16000:

        y = librosa.resample(
            y,
            orig_sr=sr,
            target_sr=16000
        )

        sr = 16000


    # --------------------------------
    # 2️⃣ Speech band filter
    # --------------------------------

    y = bandpass_filter(
        y,
        sr,
        low=80,
        high=7000
    )


    # --------------------------------
    # 3️⃣ Mild noise reduction
    # --------------------------------

    y = mild_noise_reduction(y)


    # --------------------------------
    # 4️⃣ Boost if child confidence low
    # --------------------------------

    if low_confidence:

        y = amplitude_boost(y, boost=1.5)


    # --------------------------------
    # 5️⃣ Final normalization
    # --------------------------------

    y = safe_normalize(y)


    return {

        "enhanced_waveform": y,
        "sample_rate": sr

    }

