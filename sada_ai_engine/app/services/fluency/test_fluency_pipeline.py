"""نتأكد إن:
preprocess → segmentation → repetition → prolongation → decision
شغالين مع بعض صح"""

import librosa

# ------------------------------------------
# IMPORT YOUR MODULES
# ------------------------------------------

from app.services.global_preprocess.audio_preprocess import preprocess_audio

from app.services.fluency.fluency_preprocess import fluency_preprocess
from app.services.fluency.segmentation import segmentation_pipeline
from app.services.fluency.repetition_detection import detect_repetition
from app.services.fluency.prolongation_detection import detect_prolongation
from app.services.fluency.fluency_decision import fluency_decision


# ------------------------------------------
# LOAD AUDIO
# ------------------------------------------

AUDIO_PATH = r"sada_ai_engine\أرنب3.wav"  # حطي هنا ملفك

print("\n==============================")
print("STEP 1: LOAD AUDIO")
print("==============================")

y, sr = librosa.load(AUDIO_PATH, sr=None)

global_data = {
    "waveform": y,
    "sample_rate": sr
}

print("Audio loaded ✔")


# ------------------------------------------
# STEP 2: GLOBAL PREPROCESS
# ------------------------------------------

print("\n==============================")
print("STEP 2: GLOBAL PREPROCESS")
print("==============================")

global_data = preprocess_audio(open(AUDIO_PATH, "rb").read())

print("Waveform length:", len(global_data["waveform"]))
print("Sample rate:", global_data["sample_rate"])


# ------------------------------------------
# STEP 3: FLUENCY PREPROCESS
# ------------------------------------------

print("\n==============================")
print("STEP 3: FLUENCY PREPROCESS")
print("==============================")

fluency_data = fluency_preprocess(global_data)

y = fluency_data["waveform"]
sr = fluency_data["sample_rate"]

print("Processed waveform length:", len(y))


# ------------------------------------------
# STEP 4: SEGMENTATION + PAUSES
# ------------------------------------------

print("\n==============================")
print("STEP 4: SEGMENTATION")
print("==============================")

seg_result = segmentation_pipeline(y, sr)

intervals = seg_result["intervals"]

print("Segments:", len(intervals))
print("Pause count:", seg_result["pause_count"])
print("Max pause:", seg_result["max_pause"])


# ------------------------------------------
# STEP 5: REPETITION
# ------------------------------------------

print("\n==============================")
print("STEP 5: REPETITION DETECTION")
print("==============================")

rep_result = detect_repetition(y, sr, intervals)

print("Repetition count:", rep_result["repetition_count"])
print("Similarities:", rep_result["similarities"])


# ------------------------------------------
# STEP 6: PROLONGATION
# ------------------------------------------

print("\n==============================")
print("STEP 6: PROLONGATION DETECTION")
print("==============================")

prol_result = detect_prolongation(y, sr, intervals)

print("Prolongation count:", prol_result["prolongation_count"])
print("Durations:", prol_result["durations"])


# ------------------------------------------
# STEP 7: DECISION
# ------------------------------------------

print("\n==============================")
print("STEP 7: DECISION")
print("==============================")

final_result = fluency_decision(
    repetition_count=rep_result["repetition_count"],
    pause_count=seg_result["pause_count"],
    max_pause=seg_result["max_pause"],
    prolongation_count=prol_result["prolongation_count"]
)

print("Final Result:")
print(final_result)


# ------------------------------------------
# DONE
# ------------------------------------------

print("\n==============================")
print("FLUENCY PIPELINE FINISHED ✔")
print("==============================")