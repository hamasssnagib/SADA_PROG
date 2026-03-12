import os
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

# ==========================
# PATH داخل المشروع
# ==========================

MODEL_DIR = "app/services/models/wav2vec2-xlsr-53-espeak-cv-ft"

os.makedirs(MODEL_DIR, exist_ok=True)

print("Downloading phoneme model...")

processor = Wav2Vec2Processor.from_pretrained(
    "facebook/wav2vec2-xlsr-53-espeak-cv-ft"
)

model = Wav2Vec2ForCTC.from_pretrained(
    "facebook/wav2vec2-xlsr-53-espeak-cv-ft"
)

# ==========================
# حفظ الموديل محليًا
# ==========================

processor.save_pretrained(MODEL_DIR)
model.save_pretrained(MODEL_DIR)

print("Model downloaded successfully ✔")
print("Saved in:", MODEL_DIR)