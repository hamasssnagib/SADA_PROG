import torch
import torchaudio
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

MODEL_PATH = "app/services/models/wav2vec2-xlsr-53-espeak-cv-ft"

print("Loading phoneme model...")

processor = Wav2Vec2Processor.from_pretrained(MODEL_PATH)
model = Wav2Vec2ForCTC.from_pretrained(MODEL_PATH)

print("Model loaded ✔")

audio_path = "ثلثلة.wav"

speech, sr = torchaudio.load(audio_path)

# تحويل stereo إلى mono
if speech.shape[0] > 1:
    speech = speech.mean(dim=0)

speech = speech.squeeze()

# إعادة ضبط العينة
if sr != 16000:
    resampler = torchaudio.transforms.Resample(sr, 16000)
    speech = resampler(speech)

inputs = processor(
    speech,
    sampling_rate=16000,
    return_tensors="pt"
)

with torch.no_grad():
    logits = model(**inputs).logits

predicted_ids = torch.argmax(logits, dim=-1)

phonemes = processor.batch_decode(predicted_ids)

print("\nDetected phonemes:")
print(phonemes[0])