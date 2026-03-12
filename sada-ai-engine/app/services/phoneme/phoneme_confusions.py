"""
Phoneme Confusion Detector

Detects common articulation substitutions
used in speech therapy analysis
"""


CONFUSION_MAP = {

    # لثغة السين
    "s": ["θ", "th"],

    # لثغة الزاي
    "z": ["ð"],

    # ر ↔ ل
    "r": ["l"],

    # ك ↔ ت
    "k": ["t"],

    # ج ↔ د
    "dʒ": ["d"],

}


def detect_confusion(expected, spoken):

    """
    Detect phoneme substitution patterns
    """

    if spoken is None:
        return None

    if expected not in CONFUSION_MAP:
        return None

    if spoken in CONFUSION_MAP[expected]:

        return f"{expected}_to_{spoken}"

    return None