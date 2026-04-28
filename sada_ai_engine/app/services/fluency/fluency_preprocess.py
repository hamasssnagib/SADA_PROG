
import numpy as np
import librosa


# -------------------------------------------------
# Resample to 16kHz
# -------------------------------------------------
def resample_audio(y, sr, target_sr=16000):

    if sr != target_sr:
        y = librosa.resample(
            y,
            orig_sr=sr,
            target_sr=target_sr
        )
        sr = target_sr

    return y, sr


# -------------------------------------------------
# Safe Normalize (non-destructive)
# -------------------------------------------------
def normalize_audio(y):

    max_val = np.max(np.abs(y))

    if max_val > 0:
        y = y / max_val

    return y


# -------------------------------------------------
# VERY mild denoise (safe for fluency)
# -------------------------------------------------
def mild_denoise(y):

    # بدل ما نكسر الإشارة، نعمل attenuation بسيط جدًا
    noise_floor = np.percentile(np.abs(y), 5)

    y_clean = y.copy()
    mask = np.abs(y_clean) < noise_floor

    # نقلل مش نلغي
    y_clean[mask] *= 0.5

    return y_clean


# -------------------------------------------------
# Trim ONLY leading/trailing silence
# -------------------------------------------------
def trim_edges(y):

    yt, _ = librosa.effects.trim(y, top_db=25)
    return yt


# -------------------------------------------------
# Energy check (important for stuttering)
# -------------------------------------------------
def check_signal_validity(y):

    energy = np.mean(np.abs(y))

    if energy < 1e-4:
        return False

    return True


# -------------------------------------------------
# Main Fluency Preprocess (FINAL)
# -------------------------------------------------
def fluency_preprocess(global_data):
    """
    Preprocess audio for stuttering detection

    IMPORTANT:
    - Preserve timing
    - Avoid distortion
    """

    y = global_data["waveform"]
    sr = global_data["sample_rate"]

    y = y.astype(np.float32)

    # -----------------------------
    # 1) Resample
    # -----------------------------
    y, sr = resample_audio(y, sr)

    # -----------------------------
    # 2) Trim edges ONLY
    # -----------------------------
    y = trim_edges(y)

    # -----------------------------
    # 3) Check validity
    # -----------------------------
    is_valid = check_signal_validity(y)

    # -----------------------------
    # 4) Mild denoise (SAFE)
    # -----------------------------
    y = mild_denoise(y)

    # -----------------------------
    # 5) Normalize (LAST STEP)
    # -----------------------------
    y = normalize_audio(y)

    return {
        "waveform": y,
        "sample_rate": sr,
        "valid": is_valid
    }