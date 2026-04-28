# import torch
# import librosa
# from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
# import os

# MODEL_PATH = os.path.abspath("app/models/wav2vec2")

# print("Loading phoneme model...")
# processor = Wav2Vec2Processor.from_pretrained(MODEL_PATH)
# model = Wav2Vec2ForCTC.from_pretrained(MODEL_PATH)
# model.eval()
# print("Model loaded ✅")

# audio_path = "ثمكة.wav"
# y, sr = librosa.load(audio_path, sr=16000)

# inputs = processor(y, sampling_rate=16000, return_tensors="pt")

# with torch.no_grad():
#     logits = model(**inputs).logits

# predicted_ids = torch.argmax(logits, dim=-1)
# phoneme_seq = processor.batch_decode(predicted_ids)[0]

# print("\n===== PHONEME OUTPUT =====")
# print(phoneme_seq)

# import os
# import soundfile as sf
# from allosaurus.app import read_recognizer


# # =====================================
# # MODEL PATH
# # =====================================

# MODEL_PATH = "app/models/allosaurusmodel"


# print("Loading Allosaurus model...")

# recognizer = read_recognizer(MODEL_PATH)

# print("Model loaded ✔")


# # =====================================
# # AUDIO FILE
# # =====================================

# audio_path = "iso_s.wav"

# print("\n==============================")
# print("STEP 1: LOAD AUDIO")
# print("==============================")

# speech, sr = sf.read(audio_path)

# print("Sample rate:", sr)
# print("Audio length:", len(speech))


# # =====================================
# # PHONEME RECOGNITION
# # =====================================

# print("\n==============================")
# print("STEP 2: PHONEME RECOGNITION")
# print("==============================")

# result = recognizer.recognize(audio_path)

# print("\nRaw result:")
# print(result)


# # =====================================
# # PHONEME STREAM
# # =====================================

# phoneme_stream = result.strip().split()

# print("\n==============================")
# print("STEP 3: PHONEME STREAM")
# print("==============================")

# print(phoneme_stream)


# print("\n==============================")
# print("TOTAL PHONEMES:", len(phoneme_stream))
# print("==============================")

from allosaurus.app import read_recognizer

print("Loading Allosaurus model...")

recognizer = read_recognizer()   # بدون مسار

print("Model loaded ✔")


audio_path = "iso_s.wav"

print("\nRecognizing phonemes...")

result = recognizer.recognize(audio_path)

print("\nRaw phoneme output:")
print(result)


phoneme_stream = result.strip().split()

print("\nPhoneme stream:")
print(phoneme_stream)