# # import torch
# # import torchaudio
# # import soundfile as sf
# # import numpy as np
# # from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

# # MODEL_PATH = "app/services/models/wav2vec2-xlsr-53-espeak-cv-ft"

# # print("Loading phoneme model...")

# # processor = Wav2Vec2Processor.from_pretrained(MODEL_PATH)
# # model = Wav2Vec2ForCTC.from_pretrained(MODEL_PATH)

# # print("Model loaded ✔")

# # audio_path = "أينب.wav"

# # speech, sr = sf.read(audio_path)

# # # stereo → mono
# # if len(speech.shape) > 1:
# #     speech = np.mean(speech, axis=1)

# # speech = speech.astype("float32")

# # # resample
# # if sr != 16000:
# #     resampler = torchaudio.transforms.Resample(sr, 16000)
# #     speech = torch.tensor(speech)
# #     speech = resampler(speech)
# # else:
# #     speech = torch.tensor(speech)

# # inputs = processor(
# #     speech,
# #     sampling_rate=16000,
# #     return_tensors="pt"
# # )

# # with torch.no_grad():
# #     logits = model(**inputs).logits

# # predicted_ids = torch.argmax(logits, dim=-1)

# # phonemes = processor.batch_decode(predicted_ids)

# # print("\nDetected phonemes:")
# # print(phonemes[0])





# import torch
# import torchaudio
# import soundfile as sf  # ضفنا المكتبة دي هنا
# from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

# # 1. تحديد الموديل
# MODEL_DIR = "app/models/jonatasgrosman_arabic" 

# print("Loading model...")
# processor = Wav2Vec2Processor.from_pretrained(MODEL_DIR)
# model = Wav2Vec2ForCTC.from_pretrained(MODEL_DIR)

# # 2. مسار ملف الصوت بتاعك
# audio_path = "ثلثلة3.wav" 

# # ==========================================
# # التعديل: قراءة الصوت باستخدام soundfile بدلاً من torchaudio
# # ==========================================
# # قراءة الملف
# audio_data, sample_rate = sf.read(audio_path)

# # تحويل البيانات لشكل Tensor عشان الموديل يفهمه
# waveform = torch.tensor(audio_data).float()

# # لو الصوت ستيريو (قناتين)، ندمجهم في قناة واحدة (مونو)
# if waveform.ndim > 1:
#     waveform = waveform.mean(dim=1)
    
# waveform = waveform.unsqueeze(0)

# # الموديلات دي بتطلب الصوت يكون بتردد 16000 هرتز
# if sample_rate != 16000:
#     resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
#     waveform = resampler(waveform)
# # ==========================================

# # 3. معالجة الصوت واستخراج الكلمة
# inputs = processor(waveform.squeeze(), sampling_rate=16000, return_tensors="pt", padding=True)

# with torch.no_grad():
#     logits = model(inputs.input_values).logits

# # فك شفرة النتيجة لحروف عربي
# predicted_ids = torch.argmax(logits, dim=-1)
# transcription = processor.batch_decode(predicted_ids)[0]

# print("\n=========================")
# print("الكلمة اللي الموديل سمعها هي:", transcription)
# print("=========================\n")




import torch
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

# 1. حطي مسار الفولدر اللي في الصورة هنا (تأكدي من الاسم بالظبط)
MODEL_PATH = "app/models/jonatasgrosman_arabic" 

print("Loading model from local path...")

# تحميل الـ Processor والموديل من الفولدر المحلي
processor = Wav2Vec2Processor.from_pretrained(MODEL_PATH)
model = Wav2Vec2ForCTC.from_pretrained(MODEL_PATH)

# 2. تحميل ملف الصوت (تأكدي إن الـ sr=16000)
audio_path = "ثمكة3.wav" 
speech, sr = librosa.load(audio_path, sr=16000)

# 3. تحويل الصوت لبيانات رقمية
inputs = processor(speech, sampling_rate=16000, return_tensors="pt", padding=True)

# 4. التنبؤ الخام (السر في عدم التصحيح)
with torch.no_grad():
    logits = model(inputs.input_values).logits

# اختيار أعلى حرف احتمالاً (Greedy Decoding)
# ده اللي بيمنع الموديل إنه يصلح الغلط لغوياً
predicted_ids = torch.argmax(logits, dim=-1)

# تحويل الـ IDs لنص
transcription = processor.batch_decode(predicted_ids)[0]

print("-" * 30)
print("النتيجة الخام (بدون تصحيح):")
print(transcription)
print("-" * 30)