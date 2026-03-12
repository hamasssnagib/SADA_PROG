import numpy as np
import librosa


# -------------------------------------------------
# Feature extraction
# -------------------------------------------------

def extract_features(y, sr):

    S = np.abs(librosa.stft(y))

    freqs = librosa.fft_frequencies(sr=sr)

    centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()

    energy = np.mean(y**2)

    return {
        "spectrum": S,
        "freqs": freqs,
        "centroid": centroid,
        "energy": energy
    }


# -------------------------------------------------
# Fricative detector (س / ش)
# -------------------------------------------------

def detect_fricative(features, low, high):

    S = features["spectrum"]
    freqs = features["freqs"]

    band = (freqs > low) & (freqs < high)

    band_energy = S[band].mean()

    return band_energy


# -------------------------------------------------
# Stop detector (ك / ق)
# -------------------------------------------------

def detect_stop(features):

    centroid = features["centroid"]

    if centroid < 2000:
        return 0.4

    if centroid < 3500:
        return 0.7

    return 1.0


# -------------------------------------------------
# Liquid detector (ر / ل)
# -------------------------------------------------

def detect_liquid(features):

    centroid = features["centroid"]

    if centroid < 2500:
        return 0.8

    return 0.5


# -------------------------------------------------
# Main isolation detector
# -------------------------------------------------

def detect_isolation_acoustic(y, sr, target_letter):

    features = extract_features(y, sr)

    # ---------------------------------------------
    # س
    # ---------------------------------------------

    if target_letter == "س":

        energy = detect_fricative(features, 4000, 8000)

        score = min(energy * 10, 1.0)

    # ---------------------------------------------
    # ش
    # ---------------------------------------------

    elif target_letter == "ش":

        energy = detect_fricative(features, 3000, 7000)

        score = min(energy * 10, 1.0)

    # ---------------------------------------------
    # ف
    # ---------------------------------------------

    elif target_letter == "ف":

        energy = detect_fricative(features, 2500, 6000)

        score = min(energy * 10, 1.0)

    # ---------------------------------------------
    # ك
    # ---------------------------------------------

    elif target_letter == "ك":

        score = detect_stop(features)

    # ---------------------------------------------
    # ق
    # ---------------------------------------------

    elif target_letter == "ق":

        score = detect_stop(features)

    # ---------------------------------------------
    # ر
    # ---------------------------------------------

    elif target_letter == "ر":

        score = detect_liquid(features)

    # ---------------------------------------------
    # ل
    # ---------------------------------------------

    elif target_letter == "ل":

        score = detect_liquid(features)

    else:

        return {
            "accuracy": 0,
            "error_type": "unsupported_letter"
        }

    accuracy = int(score * 100)

    if accuracy >= 80:
        error = None
    elif accuracy >= 50:
        error = "distortion"
    else:
        error = "substitution"

    return {
        "accuracy": accuracy,
        "error_type": error,
        "detector": "acoustic"
    }