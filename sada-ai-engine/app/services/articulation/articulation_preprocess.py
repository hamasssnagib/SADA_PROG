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








# """
# Articulation Specialized Preprocessing 

# Adaptive preprocessing based on phoneme class.

# This module enhances signal BEFORE phoneme detection.
# It does NOT distort spectral structure.
# """

# import numpy as np
# from scipy.signal import butter, lfilter


# # -------------------------------------------------
# # Phoneme Classes (IPA Based)
# # -------------------------------------------------
# FRICATIVES = ["s", "z", "ʃ", "θ", "ð", "f", "x", "ɣ"]
# EMPHATICS = ["sˤ", "dˤ", "tˤ", "ðˤ"]
# STOPS = ["k", "q", "t", "d", "b"]
# LIQUIDS = ["r", "l"]


# # -------------------------------------------------
# # Generic Butterworth Band Filter
# # -------------------------------------------------
# def band_filter(y, sr, lowcut=None, highcut=None, order=4):
#     nyquist = 0.5 * sr

#     if lowcut and highcut:
#         low = lowcut / nyquist
#         high = highcut / nyquist
#         b, a = butter(order, [low, high], btype="band")

#     elif lowcut:
#         low = lowcut / nyquist
#         b, a = butter(order, low, btype="high")

#     elif highcut:
#         high = highcut / nyquist
#         b, a = butter(order, high, btype="low")

#     else:
#         return y

#     return lfilter(b, a, y)


# # -------------------------------------------------
# # Energy Stabilization
# # -------------------------------------------------
# def energy_boost_if_needed(y, threshold=0.02):
#     """
#     Boost signal if RMS energy is too low.
#     Prevents weak child voice from failing detection.
#     """

#     rms = np.sqrt(np.mean(y**2))

#     if rms < threshold:
#         y = y * (threshold / (rms + 1e-6))

#     return y


# # -------------------------------------------------
# # Safe Normalize
# # -------------------------------------------------
# def safe_normalize(y):
#     max_val = np.max(np.abs(y))
#     if max_val > 0:
#         y = y / max_val
#     return y


# # -------------------------------------------------
# # Main Adaptive Preprocess
# # -------------------------------------------------
# def articulation_preprocess(global_data, target_ipa=None):
#     """
#     Adaptive articulation enhancement.

#     Parameters:
#         global_data: output from global preprocess
#         target_ipa: phoneme in IPA form

#     Returns:
#         dict:
#             enhanced_waveform
#             sample_rate
#     """

#     y = global_data["waveform"]
#     sr = global_data["sample_rate"]

#     y_processed = y.copy()

#     # --------------------------------------------
#     # Strategy 1: Fricatives → High frequency focus
#     # --------------------------------------------
#     if target_ipa in FRICATIVES:
#         y_processed = band_filter(
#             y_processed,
#             sr,
#             lowcut=2500,
#             highcut=8000
#         )

#     # --------------------------------------------
#     # Strategy 2: Emphatics → Low-mid emphasis
#     # --------------------------------------------
#     elif target_ipa in EMPHATICS:
#         y_processed = band_filter(
#             y_processed,
#             sr,
#             lowcut=500,
#             highcut=4000
#         )

#     # --------------------------------------------
#     # Strategy 3: Stops → Preserve burst (mild high-pass)
#     # --------------------------------------------
#     elif target_ipa in STOPS:
#         y_processed = band_filter(
#             y_processed,
#             sr,
#             lowcut=300
#         )

#     # --------------------------------------------
#     # Strategy 4: Liquids → Formant clarity region
#     # --------------------------------------------
#     elif target_ipa in LIQUIDS:
#         y_processed = band_filter(
#             y_processed,
#             sr,
#             lowcut=300,
#             highcut=3500
#         )

#     # --------------------------------------------
#     # Energy stabilization
#     # --------------------------------------------
#     y_processed = energy_boost_if_needed(y_processed)

#     # --------------------------------------------
#     # Final normalization
#     # --------------------------------------------
#     y_processed = safe_normalize(y_processed)

#     return {
#         "enhanced_waveform": y_processed,
#         "sample_rate": sr
#     }









# """
# Articulation Specialized Preprocessing

# This module prepares the audio signal specifically
# for articulation-level phoneme analysis.

# It applies:
# 1) Optional band-pass filtering (for fricatives like /s/)
# 2) Signal normalization (secondary safety)
# 3) Ensures signal integrity before phoneme detection
# """

# import numpy as np
# from scipy.signal import butter, lfilter


# # -------------------------------------------------
# # Band-pass filter using Butterworth filter
# # -------------------------------------------------
# def bandpass_filter(y, sr, lowcut=3000, highcut=8000, order=4):
#     """
#     Apply a Butterworth band-pass filter.

#     Parameters:
#         y (np.array): input waveform
#         sr (int): sample rate
#         lowcut (int): lower cutoff frequency
#         highcut (int): upper cutoff frequency
#         order (int): filter order

#     Returns:
#         filtered waveform
#     """

#     nyquist = 0.5 * sr
#     low = lowcut / nyquist
#     high = highcut / nyquist

#     b, a = butter(order, [low, high], btype="band")
#     filtered = lfilter(b, a, y)

#     return filtered


# # -------------------------------------------------
# # Secondary normalization (safety normalization)
# # -------------------------------------------------
# def safe_normalize(y):
#     """
#     Ensures signal amplitude is within [-1, 1]
#     """

#     max_val = np.max(np.abs(y))
#     if max_val > 0:
#         y = y / max_val

#     return y


# # -------------------------------------------------
# # Main Articulation Preprocess Function
# # -------------------------------------------------
# def articulation_preprocess(global_data, target=None):
#     """
#     Prepares audio for articulation detection.

#     Parameters:
#         global_data (dict):
#             {
#                 "waveform": np.array,
#                 "sample_rate": int,
#                 ...
#             }

#         target (str):
#             target phoneme (optional)
#             used to decide filtering strategy

#     Returns:
#         dict:
#             {
#                 "enhanced_waveform": np.array,
#                 "sample_rate": int
#             }
#     """

#     y = global_data["waveform"]
#     sr = global_data["sample_rate"]

#     # -------------------------------------------------
#     # If target is fricative (like /س/)
#     # apply high-frequency band-pass filter
#     # -------------------------------------------------
#     if target in ["س", "ص", "ش", "ز", "ظ"]:
#         y_filtered = bandpass_filter(y, sr)
#     else:
#         # No special filtering for non-fricatives
#         y_filtered = y.copy()

#     # Safety normalization
#     y_filtered = safe_normalize(y_filtered)

#     return {
#         "enhanced_waveform": y_filtered,
#         "sample_rate": sr
#     }