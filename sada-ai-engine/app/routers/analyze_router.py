"""
analyze_router.py

Final Production Version

This router runs the AI engine and returns structured
analysis compatible with the ERD database schema.

It does NOT store data.
Backend service is responsible for saving results.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse

from app.services.global_preprocess.audio_preprocess import preprocess_audio

from app.services.psychological_safety.acoustic_features import extract_acoustic_features
from app.services.psychological_safety.emotional_decision import emotional_decision

from app.services.articulation.articulation_engine import detect_articulation
from app.services.fluency.fluency_engine import detect_fluency
# from app.services.articulation.isolation_engine import detect_isolation
# from app.services.articulation.word_engine import detect_word_level
# from app.services.articulation.sentence_engine import detect_sentence_level


router = APIRouter()


@router.post("/analyze")
async def analyze(

    # therapy info
    problem: str = Form(...),
    level: str = Form(...),

    target: str = Form(None),
    target_word: str = Form(None),
    target_sentence: str = Form(None),

    # session info
    level_id: int = Form(...),
    session_number: int = Form(...),
    attempt_number: int = Form(...),

    # emotional baseline
    session_count: int = Form(...),
    baseline_mean_f0: float = Form(None),
    baseline_std_f0: float = Form(None),

    # control
    force_continue: bool = Form(False),

    # audio
    file: UploadFile = File(...)
):

    # -------------------------------------------------
    # Validate file
    # -------------------------------------------------

    if not file or not file.content_type or not file.content_type.startswith("audio/"):

        raise HTTPException(
            status_code=400,
            detail="Invalid file type"
        )

    try:

        audio_bytes = await file.read()

        # -------------------------------------------------
        # GLOBAL PREPROCESS
        # -------------------------------------------------

        global_data = preprocess_audio(audio_bytes)

        waveform = global_data["waveform"]
        sr = global_data["sample_rate"]

        if len(waveform) < sr * 0.3:

            return JSONResponse(
                status_code=200,
                content={
                    "status": "invalid_audio",
                    "reason": "empty_or_silence"
                }
            )

        # -------------------------------------------------
        # EMOTIONAL ANALYSIS
        # -------------------------------------------------

        acoustic_features = extract_acoustic_features(
            waveform,
            sr
        )

        baseline = None

        if baseline_mean_f0 is not None and baseline_std_f0 is not None:

            baseline = {
                "mean_f0": baseline_mean_f0,
                "std_f0": baseline_std_f0
            }

        anxiety_detected = emotional_decision(
            features=acoustic_features,
            session_count=session_count,
            baseline=baseline
        )

        if anxiety_detected and not force_continue:

            return JSONResponse(
                status_code=200,
                content={
                    "status": "retry_due_to_anxiety",
                    "analysis_blocked": True,
                    "calm_mode": True,
                    "acoustic_features": acoustic_features
                }
            )

        # # -------------------------------------------------
        # # ARTICULATION PREPROCESS
        # # -------------------------------------------------

        # enhanced = articulation_preprocess(global_data)

        # y = enhanced["enhanced_waveform"]
        # sr = enhanced["sample_rate"]

        
        # -------------------------------------------------
        # ANALYSIS ROUTING
        # -------------------------------------------------

        if problem == "articulation":

            analysis_result = detect_articulation(
                level=level,
                global_data=global_data,
                target=target,
                target_word=target_word,
                target_sentence=target_sentence
            )
        elif problem == "fluency":
            # fluency uses raw/global audio (timing sensitive)  
            analysis_result = detect_fluency(
                global_data=global_data,
                target_text=target_sentence or target_word or target)

        else:

            raise HTTPException(
                status_code=400,
                detail="Unsupported problem type"
            )
        

        # -------------------------------------------------
        # ENGINE ERROR GUARD
        # -------------------------------------------------

        engine_error = analysis_result.get("error_type")

        invalid_engine_errors = {
            "invalid_target_configuration",
            "phoneme_conversion_error",
            "target_letter_error",
            "invalid_target_letter"
        }

        if engine_error in invalid_engine_errors:

            return JSONResponse(
                status_code=400,
                content={
                    "status": "invalid_exercise_configuration",
                    "error_type": engine_error,
                    "details": analysis_result
                }
            )


        # -------------------------------------------------
        # SESSION DECISION 
        # -------------------------------------------------
        def get_session_decision(accuracy: float) -> str:
            if accuracy >= 85:
                return "promote"
            elif accuracy >= 60:
                return "continue"
            return "regress"


        accuracy = analysis_result.get("accuracy") or 0
        decision = get_session_decision(accuracy)
        

        # -------------------------------------------------
        # RESPONSE STRUCTURE (ERD compatible)
        # -------------------------------------------------
        details = analysis_result.get("details") or {} # ensure details is a dict even if engine forgot to include it
        response = {
            "problem": problem,
            "level": level,
            
            
            "session": {
                "level_id": level_id,
                "session_number": session_number,
                "overall_accuracy": accuracy,
                "decision": decision
            },

            "attempt": {
                "attempt_number": attempt_number
            },

            "analysis": {

                "accuracy": accuracy,
                "error_type": analysis_result.get("error_type"),

                # "block_rate": analysis_result.get("details", {}).get("pause_count", 0),
                # "repetition_rate": analysis_result.get("details", {}).get("repetition_count", 0),
                
                "block_rate": (
                    details.get("pause_count", 0)
                    if analysis_result.get("mode") == "fluency" else 0
                ),

                "repetition_rate": (
                    details.get("repetition_count", 0)
                    if analysis_result.get("mode") == "fluency" else 0
                ),

                "mean_f0": acoustic_features.get("mean_f0"),
                "jitter": acoustic_features.get("jitter"),
                "shimmer": acoustic_features.get("shimmer"),
                "hnr": acoustic_features.get("hnr"),
                "energy_dev": acoustic_features.get("energy_dev")
            },

            "feature_vector": {

                "centroid": acoustic_features.get("centroid", 0),
                "duration": acoustic_features.get("duration", 0),
                "energy": acoustic_features.get("energy_dev"),
                "mfcc_summary": acoustic_features.get("mfcc_summary", [])
            },

            "analysis_details": analysis_result,# include full engine output for debugging and future analysis, but also extract key details to top-level for easy access
            "mode": analysis_result.get("mode")  # include mode for easier filtering and analysis later
        }
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "analysis_complete",
                "analysis_blocked": False,
                "calm_mode": False,
                "result": response
            }
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Processing error: {str(e)}"
        )