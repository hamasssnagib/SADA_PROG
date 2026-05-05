"""الأولوية:
Repetition > Block > Prolongation > Normal"""

# def classify_stuttering(repetition_count, pause_count, max_pause, prolongation_count):

#     # 👑 Repetition أقوى مؤشر
#     if repetition_count >= 2:
#         return "repetition"

#     # 👑 Block = pause طويل
#     if max_pause > 0.5:
#         return "block"

#     # 👑 Prolongation
#     if prolongation_count > 0:
#         return "prolongation"

#     return "normal"



def classify_stuttering(repetition_count, pause_count, max_pause, prolongation_count):

    if repetition_count >= 1:
        return "repetition"

    if max_pause > 0.7:
        return "block"

    if prolongation_count > 0:
        return "prolongation"

    return "normal"

# def calculate_fluency_score(repetition_count, pause_count, prolongation_count):

#     score = 100

#     score -= repetition_count * 15
#     score -= pause_count * 10
#     score -= prolongation_count * 10

#     return max(0, score)


def calculate_fluency_score(repetition_count, pause_count, prolongation_count):

    score = 100

    score -= repetition_count * 20   # 👈 repetition أقوى
    score -= pause_count * 10
    score -= prolongation_count * 12

    return max(0, score)

def classify_severity(score):

    if score >= 80:
        return "mild"
    elif score >= 50:
        return "moderate"
    else:
        return "severe"
    

def fluency_decision(
    repetition_count,
    pause_count,
    max_pause,
    prolongation_count
):

    stutter_type = classify_stuttering(
        repetition_count,
        pause_count,
        max_pause,
        prolongation_count
    )

    score = calculate_fluency_score(
        repetition_count,
        pause_count,
        prolongation_count
    )

    severity = classify_severity(score)

    return {
        "stuttering_type": stutter_type,
        "fluency_score": score,
        "severity": severity
    }