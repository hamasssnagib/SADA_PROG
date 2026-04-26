"""Input: waveform + sample_rate
↓
preprocess
↓
segmentation
↓
repetition
↓
prolongation
↓
decision
↓
Output structured"""

"""
Fluency Engine (Final Version)

End-to-End Stuttering Detection
"""

from app.services.fluency.fluency_preprocess import fluency_preprocess
from app.services.fluency.segmentation import segmentation_pipeline
from app.services.fluency.repetition_detection import detect_repetition
from app.services.fluency.prolongation_detection import detect_prolongation
from app.services.fluency.fluency_decision import fluency_decision


# ---------------------------------------------------------
# Main Fluency Detection
# ---------------------------------------------------------

def detect_fluency(global_data):

    # ---------------------------------------------
    # STEP 1: Preprocess
    # ---------------------------------------------

    fluency_data = fluency_preprocess(global_data)

    y = fluency_data["waveform"]
    sr = fluency_data["sample_rate"]

    # ---------------------------------------------
    # STEP 2: Segmentation + pauses
    # ---------------------------------------------

    seg = segmentation_pipeline(y, sr)

    intervals = seg["intervals"]
    pause_count = seg["pause_count"]
    max_pause = seg["max_pause"]

    # ---------------------------------------------
    # STEP 3: Repetition
    # ---------------------------------------------

    rep = detect_repetition(y, sr, intervals)

    repetition_count = rep["repetition_count"]

    # ---------------------------------------------
    # STEP 4: Prolongation
    # ---------------------------------------------

    prol = detect_prolongation(y, sr, intervals)

    prolongation_count = prol["prolongation_count"]

    # ---------------------------------------------
    # STEP 5: Decision
    # ---------------------------------------------

    decision = fluency_decision(
        repetition_count=repetition_count,
        pause_count=pause_count,
        max_pause=max_pause,
        prolongation_count=prolongation_count
    )

    # ---------------------------------------------
    # FINAL OUTPUT
    # ---------------------------------------------

    return {

    "mode": "fluency",

    "accuracy": decision["fluency_score"],

    "performance": {

        "stuttering_type": decision["stuttering_type"],
        "severity": decision["severity"]
    },

    "details": {

        "repetition_count": repetition_count,
        "pause_count": pause_count,
        "max_pause": max_pause,
        "prolongation_count": prolongation_count
    },

    "error_type": None
}
    