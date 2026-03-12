"""
Phoneme Detector (Robust Version)

Shared phoneme detection logic used by:
- isolation_engine
- word_engine
- sentence_engine
"""

# ---------------------------------------------------------
# Normalize phoneme stream
# ---------------------------------------------------------

def normalize_stream(stream):

    vowels = {
        "a","e","i","o","u",
        "ɒ","ə","ɪ","ʊ","ɛ","æ","ɑ"
    }

    cleaned = []

    for p in stream:

        if p in vowels:
            continue

        p = p.replace("ː","")

        cleaned.append(p)

    return cleaned


# ---------------------------------------------------------
# Error classification
# ---------------------------------------------------------

def classify_error(expected, spoken):

    if spoken is None:
        return "omission"

    if spoken == expected:
        return None

    return "substitution"


def find_target_positions(target_seq, target_phoneme):
    """
    Finds all positions of target phoneme inside word.
    Handles repeated letters.
    """

    positions = []

    for i, p in enumerate(target_seq):

        if p == target_phoneme:
            positions.append(i)

    return positions




def evaluate_with_multiple_positions(stream, target_seq, target_phoneme):

    positions = find_target_positions(target_seq, target_phoneme)

    best_result = None
    best_score = -1

    for pos in positions:

        result = evaluate_phoneme_alignment(
            stream,
            target_seq,
            pos
        )

        if result["score"] > best_score:

            best_score = result["score"]
            best_result = result

    return best_result

# ---------------------------------------------------------
# Context search with tolerance
# ---------------------------------------------------------

def detect_phoneme_with_context(stream, target_seq, target_index):

    stream = normalize_stream(stream)

    expected = target_seq[target_index]

    before = target_seq[:target_index]
    after = target_seq[target_index+1:]

    candidates = []

    stream_len = len(stream)

    # allow phoneme shift tolerance
    search_window = 2

    for i in range(stream_len):

        for shift in range(-search_window, search_window + 1):

            pos = i + shift

            if pos < 0 or pos >= stream_len:
                continue

            # ------------------------------
            # middle of word
            # ------------------------------

            if before and after:

                start = pos - len(before)

                if start >= 0:

                    if stream[start:pos] == before:

                        if stream[pos+1:pos+1+len(after)] == after:

                            candidates.append(stream[pos])

            # ------------------------------
            # start of word
            # ------------------------------

            elif not before and after:

                if stream[pos+1:pos+1+len(after)] == after:

                    candidates.append(stream[pos])

            # ------------------------------
            # end of word
            # ------------------------------

            elif before and not after:

                if stream[pos-len(before):pos] == before:

                    candidates.append(stream[pos])

    # -----------------------------------------------------
    # no candidate found
    # -----------------------------------------------------

    if not candidates:

        return None, "omission", 0

    # -----------------------------------------------------
    # choose best candidate
    # -----------------------------------------------------

    for c in candidates:

        if c == expected:
            return c, None, 1.0

    # substitution case
    return candidates[0], "substitution", 0.6


# ---------------------------------------------------------
# Main evaluation function
# ---------------------------------------------------------

def evaluate_phoneme_alignment(stream, target_seq, target_index):

    spoken, error_type, score = detect_phoneme_with_context(
        stream,
        target_seq,
        target_index
    )

    expected = target_seq[target_index]

    return {
        "status": "aligned" if spoken else "no_attempt",
        "score": score,
        "expected_phoneme": expected,
        "spoken_phoneme": spoken,
        "error_type": error_type
    }
    
    
# ---------------------------------------------------------
# MAIN PHONEME ERROR DETECTOR
# ---------------------------------------------------------

def detect_phoneme_errors(expected_seq, spoken_seq, target_phoneme):
    """
    Detect articulation errors for target phoneme inside word.

    expected_seq : phonemes of target word
    spoken_seq   : phonemes of spoken word
    target_phoneme : phoneme we evaluate
    """

    target_positions = find_target_positions(
        expected_seq,
        target_phoneme
    )

    if not target_positions:

        return {
            "target_positions": [],
            "errors": [],
            "accuracy": 0
        }

    errors = []
    correct = 0

    for pos in target_positions:

        if pos < len(spoken_seq):

            spoken = spoken_seq[pos]

        else:

            spoken = None

        expected = expected_seq[pos]

        error_type = classify_error(expected, spoken)

        if error_type is None:
            correct += 1

        errors.append({
            "position": pos,
            "expected": expected,
            "spoken": spoken,
            "error_type": error_type
        })

    accuracy = int((correct / len(target_positions)) * 100)

    return {

        "target_positions": target_positions,

        "errors": errors,

        "accuracy": accuracy
    }







# """
# Phoneme Detector

# Shared phoneme detection logic used by:
# - isolation_engine
# - word_engine
# - sentence_engine
# """

# # ---------------------------------------------------------
# # Normalize phoneme stream
# # ---------------------------------------------------------

# def normalize_stream(stream):

#     vowels = {
#         "a","e","i","o","u",
#         "ɒ","ə","ɪ","ʊ","ɛ","æ","ɑ"
#     }

#     cleaned = []

#     for p in stream:

#         if p in vowels:
#             continue

#         p = p.replace("ː","")

#         cleaned.append(p)

#     return cleaned


# # ---------------------------------------------------------
# # Error classification
# # ---------------------------------------------------------

# def classify_error(expected, spoken):

#     if spoken is None:
#         return "omission"

#     if spoken == expected:
#         return None

#     return "substitution"


# # ---------------------------------------------------------
# # Context search
# # ---------------------------------------------------------

# def detect_phoneme_with_context(stream, target_seq, target_index):

#     stream = normalize_stream(stream)

#     expected = target_seq[target_index]

#     before = target_seq[:target_index]
#     after = target_seq[target_index+1:]

#     candidates = []

#     stream_len = len(stream)

#     for i in range(stream_len):

#         # middle of word
#         if before and after:

#             start = i - len(before)

#             if start >= 0:

#                 if stream[start:i] == before:

#                     if stream[i+1:i+1+len(after)] == after:

#                         candidates.append(stream[i])

#         # start of word
#         elif not before and after:

#             if stream[i+1:i+1+len(after)] == after:

#                 candidates.append(stream[i])

#         # end of word
#         elif before and not after:

#             if stream[i-len(before):i] == before:

#                 candidates.append(stream[i])

#     if not candidates:

#         return None, "omission", 0

#     for c in candidates:

#         if c == expected:

#             return c, None, 1.0

#     return candidates[0], "substitution", 0.6


# # ---------------------------------------------------------
# # Main evaluation function
# # ---------------------------------------------------------

# def evaluate_phoneme_alignment(stream, target_seq, target_index):

#     spoken, error_type, score = detect_phoneme_with_context(
#         stream,
#         target_seq,
#         target_index
#     )

#     expected = target_seq[target_index]

#     return {
#         "status": "aligned" if spoken else "no_attempt",
#         "score": score,
#         "expected_phoneme": expected,
#         "spoken_phoneme": spoken,
#         "error_type": error_type
#     }