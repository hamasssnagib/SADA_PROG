import numpy as np
import librosa

# -------------------------------------------------
# 🎯 Feature Extraction
# -------------------------------------------------

def extract_features(y, sr):

    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]

    return {
        "centroid_mean": float(np.mean(centroid)),
        "centroid_std": float(np.std(centroid)),
        "zcr_mean": float(np.mean(zcr)),
        "bandwidth_mean": float(np.mean(bandwidth)),
        "energy": float(np.mean(y ** 2)),
        "duration": float(librosa.get_duration(y=y, sr=sr))
    }


# -------------------------------------------------
# 🧠 Gate (FIXED)
# -------------------------------------------------

def is_isolation(features):

    duration = features["duration"]
    variation = features["centroid_std"]
    energy = features["energy"]

    # ❗ خليها أوسع عشان التسجيل الحقيقي
    if duration > 3.0:
        return False

    # ❗ أهم حاجة
    if variation > 1500:
        return False

    if energy < 0.0001:
        return False

    return True


# -------------------------------------------------
# 🎯 Classify sound type
# -------------------------------------------------

def classify_sound(features):

    c = features["centroid_mean"]
    z = features["zcr_mean"]

    if c > 4000:
        return "fricative_high"

    if c > 2800:
        return "fricative_low"

    if 1500 < c < 2800:
        return "liquid"

    if z > 0.07:
        return "stop"

    if c < 1500:
        return "nasal"

    return "unknown"


# -------------------------------------------------
# 🎯 Target → group
# -------------------------------------------------

def get_target_group(letter):

    if letter in ["س","ش","ز","ص"]:
        return "fricative_high"

    if letter in ["ف","ث","ه"]:
        return "fricative_low"

    if letter in ["ر","ل"]:
        return "liquid"

    if letter in ["ت","د","ك","ق","ط","ب"]:
        return "stop"

    if letter in ["م","ن"]:
        return "nasal"

    return "unknown"


# -------------------------------------------------
# 🎯 Exact Match (SMART FIX)
# -------------------------------------------------

def is_exact_match(letter, c, z):

    # --------------------------
    # س
    if letter == "س":
        return c > 4200 and z > 0.3

    # --------------------------
    # ش
    if letter == "ش":
        return 3000 < c < 4200

    # --------------------------
    # ف
    if letter == "ف":
        return 2500 < c < 3500 and z < 0.4

    # --------------------------
    # م
    if letter == "م":
        return c < 1500 and z < 0.1

    # --------------------------
    # ت
    if letter == "ت":
        return z > 0.08

    # --------------------------
    # ر و ل (مستحيل يتفصلوا بدقة)
    if letter in ["ر", "ل"]:
        return 1600 < c < 2800

    return False


# -------------------------------------------------
# 🎯 MAIN DETECTOR (FINAL)
# -------------------------------------------------

def detect_isolation(y, sr, target_letter):

    target_letter = target_letter.strip()

    if len(target_letter) != 1:
        return {
            "accuracy": 0,
            "error_type": "invalid_target_letter",
            "details": {}
        }

    features = extract_features(y, sr)

    # ❌ مش isolation
    if not is_isolation(features):
        return {
            "accuracy": 0,
            "error_type": "not_isolation_sound",
            "details": {
                "duration": features["duration"],
                "variation": features["centroid_std"]
            }
        }

    predicted_type = classify_sound(features)
    target_type = get_target_group(target_letter)

    c = features["centroid_mean"]
    z = features["zcr_mean"]

    # ---------------------------------
    # 🎯 LIQUID FIX (ر / ل)
    # ---------------------------------
    if target_letter in ["ر", "ل"]:

    # 🎯 شرط أقوى للـ ر
        if target_letter == "ر":
            if 1800 < c < 2400 and z > 0.08:
                return {
                    "accuracy": 100,
                    "error_type": None,
                    "details": {
                        "expected_phoneme": "ر",
                        "predicted": "ر",
                        "centroid": c,
                        "zcr": z
                    }
                }

        # 🎯 شرط أقوى للـ ل
        if target_letter == "ل":
            if 2000 < c < 2800 and z < 0.12:
                return {
                    "accuracy": 100,
                    "error_type": None,
                    "details": {
                        "expected_phoneme": "ل",
                        "predicted": "ل",
                        "centroid": c,
                        "zcr": z
                    }
                }

        # ⚠️ fallback (confusion)
        if 1600 < c < 2800:
            return {
                "accuracy": 50,
                "error_type": "distortion",
                "details": {
                    "expected_phoneme": target_letter,
                    "note": "liquid confusion (ر/ل)",
                    "centroid": c,
                    "zcr": z
                }
            }

        # ❌ غلط
        return {
            "accuracy": 0,
            "error_type": "substitution",
            "details": {
                "expected_phoneme": target_letter,
                "centroid": c,
                "zcr": z
            }
        }

    # ---------------------------------
    # ✅ صح 100%
    # ---------------------------------
    if is_exact_match(target_letter, c, z):
        return {
            "accuracy": 100,
            "error_type": None,
            "details": {
                "expected_phoneme": target_letter,
                "predicted": target_letter,
                "centroid": c,
                "zcr": z
            }
        }

    # ---------------------------------
    # ⚠️ distortion
    # ---------------------------------
    if predicted_type == target_type:
        return {
            "accuracy": 50,
            "error_type": "distortion",
            "details": {
                "expected_phoneme": target_letter,
                "predicted_type": predicted_type,
                "centroid": c,
                "zcr": z
            }
        }

    # ---------------------------------
    # ❌ substitution
    # ---------------------------------
    return {
        "accuracy": 0,
        "error_type": "substitution",
        "details": {
            "expected_phoneme": target_letter,
            "predicted_type": predicted_type,
            "centroid": c,
            "zcr": z
        }
    }










# import numpy as np
# import librosa

# # -------------------------------------------------
# # 🎯 Feature Extraction
# # -------------------------------------------------

# def extract_features(y, sr):

#     centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
#     zcr = librosa.feature.zero_crossing_rate(y)[0]
#     bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]

#     return {
#         "centroid_mean": float(np.mean(centroid)),
#         "centroid_std": float(np.std(centroid)),
#         "zcr_mean": float(np.mean(zcr)),
#         "bandwidth_mean": float(np.mean(bandwidth)),
#         "energy": float(np.mean(y ** 2)),
#         "duration": float(librosa.get_duration(y=y, sr=sr))
#     }


# # -------------------------------------------------
# # 🧠 Gate (Isolation vs Word)
# # -------------------------------------------------

# def is_isolation(features):

#     duration = features["duration"]
#     variation = features["centroid_std"]
#     energy = features["energy"]

#     if duration > 2.5:
#         return False

#     if variation > 2000:
#         return False

#     if energy < 0.0002:
#         return False

#     return True


# # -------------------------------------------------
# # 🎯 Classify sound type
# # -------------------------------------------------

# def classify_sound(features):

#     c = features["centroid_mean"]
#     z = features["zcr_mean"]

#     if c > 4000:
#         return "fricative_high"

#     if c > 2800:
#         return "fricative_low"

#     if 1500 < c < 2600:
#         return "liquid"

#     if z > 0.07:
#         return "stop"

#     if c < 1500:
#         return "nasal"

#     return "unknown"


# # -------------------------------------------------
# # 🎯 Target → group
# # -------------------------------------------------

# def get_target_group(letter):

#     if letter in ["س","ش","ز","ص"]:
#         return "fricative_high"

#     if letter in ["ف","ث"]:
#         return "fricative_low"

#     if letter in ["ر","ل"]:
#         return "liquid"

#     if letter in ["ت","د","ك","ق","ط"]:
#         return "stop"

#     if letter in ["م","ن"]:
#         return "nasal"

#     return "unknown"


# # -------------------------------------------------
# # 🎯 Exact Match (FIXED)
# # -------------------------------------------------

# def is_exact_match(letter, c, z):

#     if letter == "ر":
#         return 1700 < c < 2300

#     if letter == "ل":
#         return 1800 < c < 2600   # ✅ FIX

#     if letter == "س":
#         return c > 4000          # ✅ FIX

#     if letter == "ش":
#         return 2800 < c < 3800   # ✅ FIX

#     if letter == "ف":
#         return 2400 < c < 3300

#     if letter == "م":
#         return c < 1500

#     if letter == "ت":
#         return z > 0.07          # ✅ FIX

#     return False




# # -------------------------------------------------
# # 🎯 MAIN DETECTOR
# # -------------------------------------------------

# def detect_isolation(y, sr, target_letter):

#     target_letter = target_letter.strip()

#     if len(target_letter) != 1:
#         return {
#             "accuracy": 0,
#             "error_type": "invalid_target_letter",
#             "details": {}
#         }

#     features = extract_features(y, sr)

#     # ❌ مش Isolation
#     if not is_isolation(features):
#         return {
#             "accuracy": 0,
#             "error_type": "not_isolation_sound",
#             "details": {
#                 "duration": features["duration"],
#                 "variation": features["centroid_std"]
#             }
#         }

#     predicted_type = classify_sound(features)
#     target_type = get_target_group(target_letter)

#     c = features["centroid_mean"]
#     z = features["zcr_mean"]

#     # ✅ صح 100%
#     if is_exact_match(target_letter, c, z):
#         return {
#             "accuracy": 100,
#             "error_type": None,
#             "details": {
#                 "expected_phoneme": target_letter,
#                 "predicted": target_letter,
#                 "centroid": c,
#                 "zcr": z
#             }
#         }

#     # ⚠️ distortion
#     if predicted_type == target_type:
#         return {
#             "accuracy": 50,
#             "error_type": "distortion",
#             "details": {
#                 "expected_phoneme": target_letter,
#                 "predicted_type": predicted_type,
#                 "centroid": c,
#                 "zcr": z
#             }
#         }

#     # ❌ substitution
#     return {
#         "accuracy": 0,
#         "error_type": "substitution",
#         "details": {
#             "expected_phoneme": target_letter,
#             "predicted_type": predicted_type,
#             "centroid": c,
#             "zcr": z
#         }
#     }