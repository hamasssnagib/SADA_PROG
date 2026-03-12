import os

BASE_DIR = "sada-ai-engine"

structure = {
    "app": {
        "main.py": "",
        "config": {
            "settings.py": ""
        },
        "routers": {
            "analyze_router.py": ""
        },
        "services": {
            "global": {
                "audio_preprocess.py": "",
                "anxiety_router.py": ""
            },
            "articulation": {
                "articulation_preprocess.py": "",
                "isolation_detector.py": "",
                "word_detector.py": "",
                "sentence_detector.py": "",
                "phoneme_templates.py": ""
            },
            "fluency": {
                "fluency_preprocess.py": "",
                "block_detection.py": "",
                "repetition_detection.py": "",
                "prolongation_detection.py": ""
            }
        },
        "models": {
            "whisper": {},
            "llm": {},
            "tts": {}
        },
        "utils": {
            "audio_features.py": "",
            "logger.py": ""
        }
    },
    "temp_audio": {},
    "logs": {},
    "requirements.txt": """fastapi
uvicorn
numpy
scipy
librosa
soundfile
python-dotenv
torch
openai-whisper
""",
    ".env": "AI_ENGINE_KEY=LOCAL_SECRET\n",
    "README.md": "# SADA Local AI Engine\n"
}


def create_structure(base_path, tree):
    for name, content in tree.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            os.makedirs(base_path, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    create_structure(BASE_DIR, structure)
    print("✅ SADA AI Engine structure created successfully!")