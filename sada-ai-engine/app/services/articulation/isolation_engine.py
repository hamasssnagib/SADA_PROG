"""
Isolation Engine (Final Version)

Evaluates articulation of a single phoneme spoken in isolation.

Pipeline

1) audio → ASR
2) ASR text → phoneme sequence
3) extract dominant phoneme
4) compare with expected phoneme
"""

from app.services.asr.asr_engine import transcribe_audio
from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
from app.services.phoneme.phoneme_confusions import detect_confusion


# ---------------------------------------------------------
# Isolation articulation detection
# ---------------------------------------------------------

def detect_isolation(y, sr, target_letter):
    
    if len(target_letter) != 1:

        return {

            "accuracy": None,

            "error_type": "invalid_target_letter",

            "message": "Isolation level requires a single letter"
        }
    # -----------------------------------------------------
    # Step 1
    # speech → text
    # -----------------------------------------------------

    recognized_text = transcribe_audio(y, sr)

    if not recognized_text:

        return {
            "accuracy": 0,
            "error_type": "no_speech_detected",
            "expected_phoneme": None,
            "spoken_phoneme": None
        }

    # -----------------------------------------------------
    # Step 2
    # convert target letter → phoneme
    # -----------------------------------------------------

    target_seq = arabic_to_phoneme_sequence(target_letter)

    if not target_seq:

        return {
            "accuracy": 0,
            "error_type": "conversion_error",
            "expected_phoneme": None,
            "spoken_phoneme": None
        }

    expected_phoneme = target_seq[0]

    # -----------------------------------------------------
    # Step 3
    # convert spoken text → phonemes
    # -----------------------------------------------------

    spoken_seq = arabic_to_phoneme_sequence(recognized_text)

    if not spoken_seq:

        return {
            "accuracy": 0,
            "error_type": "phoneme_conversion_error",
            "expected_phoneme": expected_phoneme,
            "spoken_phoneme": None
        }

    # -----------------------------------------------------
    # Step 4
    # dominant phoneme detection
    # -----------------------------------------------------

    spoken_phoneme = spoken_seq[0]

    # -----------------------------------------------------
    # Step 5
    # comparison
    # -----------------------------------------------------

    if spoken_phoneme == expected_phoneme:

        return {
            "accuracy": 100,
            "error_type": None,
            "expected_phoneme": expected_phoneme,
            "spoken_phoneme": spoken_phoneme,
            "confusion_type": None
        }

    confusion = detect_confusion(expected_phoneme, spoken_phoneme)

    return {
        "accuracy": 0,
        "error_type": "substitution",
        "expected_phoneme": expected_phoneme,
        "spoken_phoneme": spoken_phoneme,
        "confusion_type": confusion
    }










# """
# Isolation Engine (Robust Version)

# Evaluates production of a single phoneme in isolation.

# Uses:
# - Allosaurus phoneme stream
# - Shared phoneme normalization
# - Phoneme confusion detection
# """

# import uuid
# import os
# import soundfile as sf

# from app.models_loader import allosaurus_model

# from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# from app.services.phoneme.phoneme_detector import normalize_stream
# from app.services.phoneme.phoneme_confusions import detect_confusion


# # ---------------------------------------------------------
# # Extract phoneme stream
# # ---------------------------------------------------------

# def infer_phoneme_stream(y, sr):

#     temp_file = f"temp_{uuid.uuid4().hex}.wav"
#     sf.write(temp_file, y, sr)

#     try:

#         result = allosaurus_model.recognize(temp_file)

#         phoneme_stream = result.strip().split()

#         return phoneme_stream

#     finally:

#         if os.path.exists(temp_file):
#             os.remove(temp_file)


# # ---------------------------------------------------------
# # Isolation detection
# # ---------------------------------------------------------

# def detect_isolation(y, sr, target_letter):

#     """
#     Detect articulation of a single phoneme.
#     """

#     # -----------------------------------------------------
#     # Convert Arabic letter → phoneme
#     # -----------------------------------------------------

#     target_seq = arabic_to_phoneme_sequence(target_letter)

#     if not target_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "conversion_error",
#             "expected_phoneme": None,
#             "spoken_phoneme": None,
#             "confusion_type": None
#         }

#     expected_phoneme = target_seq[0]

#     # -----------------------------------------------------
#     # Extract phoneme stream
#     # -----------------------------------------------------

#     phoneme_stream = infer_phoneme_stream(y, sr)

#     if not phoneme_stream:

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": expected_phoneme,
#             "spoken_phoneme": None,
#             "confusion_type": None
#         }

#     # -----------------------------------------------------
#     # Normalize phoneme stream
#     # -----------------------------------------------------

#     phoneme_stream = normalize_stream(phoneme_stream)

#     if not phoneme_stream:

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": expected_phoneme,
#             "spoken_phoneme": None,
#             "confusion_type": None
#         }

#     # -----------------------------------------------------
#     # Count occurrences
#     # -----------------------------------------------------

#     count_expected = phoneme_stream.count(expected_phoneme)
#     total = len(phoneme_stream)

#     ratio = count_expected / total

#     # -----------------------------------------------------
#     # Case 1: expected phoneme not found
#     # -----------------------------------------------------

#     if count_expected == 0:

#         spoken_phoneme = phoneme_stream[0]

#         confusion = detect_confusion(expected_phoneme, spoken_phoneme)

#         return {
#             "accuracy": 0,
#             "error_type": "substitution",
#             "expected_phoneme": expected_phoneme,
#             "spoken_phoneme": spoken_phoneme,
#             "confusion_type": confusion
#         }

#     # -----------------------------------------------------
#     # Case 2: strong correct production
#     # -----------------------------------------------------

#     if ratio >= 0.8:

#         return {
#             "accuracy": 100,
#             "error_type": None,
#             "expected_phoneme": expected_phoneme,
#             "spoken_phoneme": expected_phoneme,
#             "confusion_type": None
#         }

#     # -----------------------------------------------------
#     # Case 3: inconsistent production
#     # -----------------------------------------------------

#     if ratio >= 0.4:

#         return {
#             "accuracy": int(ratio * 100),
#             "error_type": "inconsistent_production",
#             "expected_phoneme": expected_phoneme,
#             "spoken_phoneme": expected_phoneme,
#             "confusion_type": None
#         }

#     # -----------------------------------------------------
#     # Case 4: distortion
#     # -----------------------------------------------------

#     return {
#         "accuracy": int(ratio * 100),
#         "error_type": "distortion",
#         "expected_phoneme": expected_phoneme,
#         "spoken_phoneme": expected_phoneme,
#         "confusion_type": None
#     }











# """
# Isolation Engine (Updated)

# Evaluates single phoneme production in isolation.

# Uses shared phoneme detector.
# """

# import uuid
# import os
# import soundfile as sf

# from app.models_loader import allosaurus_model

# from app.services.phoneme.phoneme_converter import arabic_to_phoneme_sequence
# from app.services.phoneme.phoneme_detector import normalize_stream
# from app.services.phoneme.phoneme_confusions import detect_confusion

# # ---------------------------------------------------------
# # Extract phoneme stream
# # ---------------------------------------------------------

# def infer_phoneme_stream(y, sr):

#     temp_file = f"temp_{uuid.uuid4().hex}.wav"
#     sf.write(temp_file, y, sr)

#     try:

#         result = allosaurus_model.recognize(temp_file)

#         phoneme_stream = result.strip().split()

#         return phoneme_stream

#     finally:

#         if os.path.exists(temp_file):
#             os.remove(temp_file)


# # ---------------------------------------------------------
# # Isolation detection
# # ---------------------------------------------------------

# def detect_isolation(y, sr, target_letter):

#     """
#     Detect articulation of a single phoneme.
#     """
#     # -----------------------------------------------------
#     # convert Arabic letter → phoneme
#     # -----------------------------------------------------

#     target_seq = arabic_to_phoneme_sequence(target_letter)

#     if not target_seq:

#         return {
#             "accuracy": 0,
#             "error_type": "conversion_error",
#             "expected_phoneme": None,
#             "spoken_phoneme": None
#         }

#     expected_phoneme = target_seq[0]

#     # -----------------------------------------------------
#     # extract phoneme stream
#     # -----------------------------------------------------

#     phoneme_stream = infer_phoneme_stream(y, sr)

#     if not phoneme_stream:

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": expected_phoneme,
#             "spoken_phoneme": None
#         }

#     # -----------------------------------------------------
#     # normalize stream
#     # -----------------------------------------------------

#     phoneme_stream = normalize_stream(phoneme_stream)

#     if not phoneme_stream:

#         return {
#             "accuracy": 0,
#             "error_type": "no_attempt",
#             "expected_phoneme": expected_phoneme,
#             "spoken_phoneme": None
#         }

#     # -----------------------------------------------------
#     # count occurrences
#     # -----------------------------------------------------

#     count_expected = phoneme_stream.count(expected_phoneme)

#     total = len(phoneme_stream)

#     ratio = count_expected / total

#     # -----------------------------------------------------
#     # classification
#     # -----------------------------------------------------

    
    
#     if count_expected == 0:

#         return {
#             "accuracy": 0,
#             "error_type": "substitution",
#             "expected_phoneme": expected_phoneme,
#             "spoken_phoneme": phoneme_stream[0]
#         }

#     if ratio >= 0.8:

#         return {
#             "accuracy": 100,
#             "error_type": None,
#             "expected_phoneme": expected_phoneme,
#             "spoken_phoneme": expected_phoneme
#         }

#     if ratio >= 0.4:

#         return {
#             "accuracy": int(ratio * 100),
#             "error_type": "inconsistent_production",
#             "expected_phoneme": expected_phoneme,
#             "spoken_phoneme": expected_phoneme
#         }

#     return {
#         "accuracy": int(ratio * 100),
#         "error_type": "distortion",
#         "expected_phoneme": expected_phoneme,
#         "spoken_phoneme": expected_phoneme
#     }






# # """
# # Isolation Engine

# # Evaluates articulation of a single phoneme in isolation.

# # Pipeline:

# # 1) Convert target Arabic letter → phoneme
# # 2) Extract phoneme stream from audio
# # 3) Detect phoneme stability
# # 4) Compare expected vs spoken phoneme
# # 5) Classify articulation error
# # """

# # import uuid
# # import os
# # import soundfile as sf
# # import numpy as np
# # import librosa

# # from app.models_loader import allosaurus_model


# # # ---------------------------------------------------------
# # # Arabic → IPA mapping
# # # ---------------------------------------------------------

# # ARABIC_TO_IPA = {
# #     "س": "s",
# #     "ز": "z",
# #     "ش": "ʃ",
# #     "ث": "θ",
# #     "ذ": "ð",
# #     "ر": "r",
# #     "ل": "l",
# #     "ك": "k",
# #     "ق": "q",
# #     "ت": "t",
# #     "د": "d",
# #     "ب": "b",
# #     "ص": "sˤ",
# #     "ض": "dˤ",
# #     "ط": "tˤ",
# #     "ظ": "ðˤ",
# #     "ف": "f",
# #     "خ": "x",
# #     "غ": "ɣ"
# # }


# # # ---------------------------------------------------------
# # # Extract phoneme stream from audio
# # # ---------------------------------------------------------

# # def infer_phoneme_stream(y, sr):

# #     temp_file = f"temp_{uuid.uuid4().hex}.wav"
# #     sf.write(temp_file, y, sr)

# #     try:

# #         result = allosaurus_model.recognize(temp_file)

# #         phoneme_stream = result.strip().split()

# #         return phoneme_stream

# #     finally:

# #         if os.path.exists(temp_file):
# #             os.remove(temp_file)


# # # ---------------------------------------------------------
# # # Spectral validation
# # # ---------------------------------------------------------

# # def spectral_validation(y, sr, expected):

# #     centroid = np.mean(
# #         librosa.feature.spectral_centroid(y=y, sr=sr)
# #     )

# #     rms = librosa.feature.rms(y=y)[0]
# #     peak = np.max(rms)

# #     if expected in ["s","z","ʃ","θ","ð","f","x","ɣ"]:
# #         return centroid > 2800

# #     if expected in ["k","q","t","d","b"]:
# #         return peak > 0.04

# #     if expected in ["r","l"]:
# #         return centroid > 1400

# #     return True


# # # ---------------------------------------------------------
# # # Main isolation detection
# # # ---------------------------------------------------------

# # def detect_isolation(y, sr, target_letter):

# #     expected = ARABIC_TO_IPA.get(target_letter, target_letter)

# #     phoneme_stream = infer_phoneme_stream(y, sr)

# #     if not phoneme_stream:

# #         return {
# #             "accuracy": 0,
# #             "error_type": "no_attempt",
# #             "expected_phoneme": expected,
# #             "spoken_phoneme": None
# #         }

# #     # -----------------------------------------------------
# #     # Unique phonemes
# #     # -----------------------------------------------------

# #     unique = set(phoneme_stream)

# #     count_expected = phoneme_stream.count(expected)

# #     ratio = count_expected / len(phoneme_stream)

# #     # -----------------------------------------------------
# #     # Case 1: sustained phoneme
# #     # -----------------------------------------------------

# #     if len(unique) == 1:

# #         spoken = list(unique)[0]

# #         if spoken == expected:

# #             if not spectral_validation(y, sr, expected):

# #                 return {
# #                     "accuracy": 70,
# #                     "error_type": "distortion",
# #                     "expected_phoneme": expected,
# #                     "spoken_phoneme": spoken
# #                 }

# #             return {
# #                 "accuracy": 100,
# #                 "error_type": None,
# #                 "expected_phoneme": expected,
# #                 "spoken_phoneme": spoken
# #             }

# #         return {
# #             "accuracy": 0,
# #             "error_type": "substitution",
# #             "expected_phoneme": expected,
# #             "spoken_phoneme": spoken
# #         }

# #     # -----------------------------------------------------
# #     # Case 2: mixed phonemes
# #     # -----------------------------------------------------

# #     if expected in unique:

# #         if ratio > 0.6:

# #             if not spectral_validation(y, sr, expected):

# #                 return {
# #                     "accuracy": 70,
# #                     "error_type": "distortion",
# #                     "expected_phoneme": expected,
# #                     "spoken_phoneme": expected
# #                 }

# #             return {
# #                 "accuracy": int(ratio * 100),
# #                 "error_type": "inconsistent_production",
# #                 "expected_phoneme": expected,
# #                 "spoken_phoneme": expected
# #             }

# #         return {
# #             "accuracy": int(ratio * 100),
# #             "error_type": "inconsistent_production",
# #             "expected_phoneme": expected,
# #             "spoken_phoneme": expected
# #         }

# #     # -----------------------------------------------------
# #     # Case 3: target phoneme missing
# #     # -----------------------------------------------------

# #     return {
# #         "accuracy": 0,
# #         "error_type": "no_attempt",
# #         "expected_phoneme": expected,
# #         "spoken_phoneme": None
# #     }









# # # """
# # # Isolation Engine (Advanced Clinical Version)

# # # This module evaluates single phoneme production in isolation.

# # # It does NOT rely on first-phoneme matching.
# # # Instead, it analyzes the entire phoneme stream contextually.

# # # It classifies into:
# # # - success
# # # - substitution
# # # - distortion
# # # - inconsistent_production
# # # - no_attempt

# # # Returns:
# # #     accuracy
# # #     error_type
# # #     expected_phoneme
# # #     spoken_phoneme
# # # """

# # # import uuid
# # # import os
# # # import numpy as np
# # # import soundfile as sf
# # # import librosa

# # # from app.models_loader import allosaurus_model


# # # # ---------------------------------------------------------
# # # # Arabic → IPA Mapping
# # # # Converts Arabic letters to IPA phonemes compatible with Allosaurus.
# # # # ---------------------------------------------------------
# # # ARABIC_TO_IPA = {
# # #     "س": "s",
# # #     "ز": "z",
# # #     "ش": "ʃ",
# # #     "ث": "θ",
# # #     "ذ": "ð",
# # #     "ر": "r",
# # #     "ل": "l",
# # #     "ك": "k",
# # #     "ق": "q",
# # #     "ت": "t",
# # #     "د": "d",
# # #     "ب": "b",
# # #     "ص": "sˤ",
# # #     "ض": "dˤ",
# # #     "ط": "tˤ",
# # #     "ظ": "ðˤ",
# # #     "ف": "f",
# # #     "خ": "x",
# # #     "غ": "ɣ"
# # # }


# # # # ---------------------------------------------------------
# # # # Phoneme Inference
# # # # Uses Allosaurus to extract full phoneme sequence from audio.
# # # # ---------------------------------------------------------
# # # def infer_phonemes(y, sr):

# # #     # Allosaurus expects a file path, so we create a temporary WAV file
# # #     temp_file = f"temp_{uuid.uuid4().hex}.wav"
# # #     sf.write(temp_file, y, sr)

# # #     try:
# # #         result = allosaurus_model.recognize(temp_file)
# # #         phoneme_sequence = result.strip().split()
# # #         return phoneme_sequence
# # #     finally:
# # #         # Always remove temp file to prevent memory leaks
# # #         if os.path.exists(temp_file):
# # #             os.remove(temp_file)


# # # # ---------------------------------------------------------
# # # # Spectral Validation
# # # # Confirms acoustic correctness even if phoneme symbol matches.
# # # # Prevents model hallucination.
# # # # ---------------------------------------------------------
# # # def spectral_validation(y, sr, expected_phoneme):

# # #     # Spectral centroid measures brightness / high-frequency energy
# # #     centroid = np.mean(
# # #         librosa.feature.spectral_centroid(y=y, sr=sr)
# # #     )

# # #     # RMS peak energy for burst detection
# # #     rms = librosa.feature.rms(y=y)[0]
# # #     peak_energy = np.max(rms)

# # #     # Fricatives require strong high-frequency energy
# # #     if expected_phoneme in ["s","z","ʃ","θ","ð","f","x","ɣ"]:
# # #         return centroid > 2800

# # #     # Stops require burst energy
# # #     if expected_phoneme in ["k","q","t","d","b"]:
# # #         return peak_energy > 0.04

# # #     # Liquids require moderate spectral energy
# # #     if expected_phoneme in ["r","l"]:
# # #         return centroid > 1400

# # #     return True


# # # # ---------------------------------------------------------
# # # # Main Isolation Detection Logic
# # # # ---------------------------------------------------------
# # # def detect_isolation(y, sr, target_letter):
# # #     """
# # #     Evaluates isolated phoneme production.

# # #     Parameters:
# # #         y : waveform
# # #         sr : sample rate
# # #         target_letter : Arabic character (e.g., "س")

# # #     Returns:
# # #         dict containing:
# # #             accuracy
# # #             error_type
# # #             expected_phoneme
# # #             spoken_phoneme
# # #     """

# # #     # Convert Arabic letter to IPA
# # #     expected = ARABIC_TO_IPA.get(target_letter, target_letter)

# # #     # Extract phoneme sequence from audio
# # #     detected_seq = infer_phonemes(y, sr)

# # #     # If model returns empty sequence → no attempt
# # #     if not detected_seq:
# # #         return {
# # #             "accuracy": 0,
# # #             "error_type": "no_attempt",
# # #             "expected_phoneme": expected,
# # #             "spoken_phoneme": None
# # #         }

# # #     # Compute unique phonemes in the stream
# # #     unique_phonemes = set(detected_seq)

# # #     # Count how many times expected phoneme appears
# # #     count_expected = detected_seq.count(expected)

# # #     # Calculate production stability ratio
# # #     ratio = count_expected / len(detected_seq)


# # #     # -----------------------------------------------------
# # #     # Case 1: Only one phoneme detected (sustained sound)
# # #     # -----------------------------------------------------
# # #     if len(unique_phonemes) == 1:

# # #         spoken = list(unique_phonemes)[0]

# # #         # If sustained phoneme equals expected
# # #         if spoken == expected:

# # #             # Validate acoustically
# # #             if not spectral_validation(y, sr, expected):
# # #                 return {
# # #                     "accuracy": 70,
# # #                     "error_type": "distortion",
# # #                     "expected_phoneme": expected,
# # #                     "spoken_phoneme": spoken
# # #                 }

# # #             return {
# # #                 "accuracy": 100,
# # #                 "error_type": None,
# # #                 "expected_phoneme": expected,
# # #                 "spoken_phoneme": spoken
# # #             }

# # #         # Sustained but wrong phoneme
# # #         return {
# # #             "accuracy": 0,
# # #             "error_type": "substitution",
# # #             "expected_phoneme": expected,
# # #             "spoken_phoneme": spoken
# # #         }


# # #     # -----------------------------------------------------
# # #     # Case 2: Two phonemes detected
# # #     # Could be unstable attempt or mixed production
# # #     # -----------------------------------------------------
# # #     if len(unique_phonemes) == 2:

# # #         if expected in unique_phonemes:

# # #             # Mostly correct but unstable
# # #             if ratio >= 0.6:

# # #                 if not spectral_validation(y, sr, expected):
# # #                     return {
# # #                         "accuracy": 70,
# # #                         "error_type": "distortion",
# # #                         "expected_phoneme": expected,
# # #                         "spoken_phoneme": expected
# # #                     }

# # #                 return {
# # #                     "accuracy": int(ratio * 100),
# # #                     "error_type": "inconsistent_production",
# # #                     "expected_phoneme": expected,
# # #                     "spoken_phoneme": expected
# # #                 }

# # #             # Present but unstable attempt
# # #             return {
# # #                 "accuracy": int(ratio * 100),
# # #                 "error_type": "inconsistent_production",
# # #                 "expected_phoneme": expected,
# # #                 "spoken_phoneme": expected
# # #             }

# # #         # Target phoneme not present at all
# # #         return {
# # #             "accuracy": 0,
# # #             "error_type": "no_attempt",
# # #             "expected_phoneme": expected,
# # #             "spoken_phoneme": None
# # #         }


# # #     # -----------------------------------------------------
# # #     # Case 3: More than two phonemes detected
# # #     # Likely the child said a word instead of isolating
# # #     # -----------------------------------------------------
# # #     if len(unique_phonemes) > 2:

# # #         if expected not in unique_phonemes:
# # #             return {
# # #                 "accuracy": 0,
# # #                 "error_type": "no_attempt",
# # #                 "expected_phoneme": expected,
# # #                 "spoken_phoneme": None
# # #             }

# # #         return {
# # #             "accuracy": int(ratio * 100),
# # #             "error_type": "inconsistent_production",
# # #             "expected_phoneme": expected,
# # #             "spoken_phoneme": expected
# # #         }