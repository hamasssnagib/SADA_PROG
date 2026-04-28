from faster_whisper import WhisperModel

model_path = "app/models/whisper_fast"
# هنستخدم الـ CPU عشان نتخطى مشكلة الـ CUDA اللي ظهرت لك
model = WhisperModel(model_path, device="cpu", compute_type="int8")

segments, info = model.transcribe(
    "iso_s.wav", 
    language="ar",
    beam_size=1, 
    # التعديلات الجوهرية هنا:
    suppress_blank=False,
    word_timestamps=True,
    # بنلغي أي محاولة لتصحيح الجملة بناءً على اللي قبلها
    condition_on_previous_text=False,
    # بنقلل الـ compression_ratio_threshold عشان لو الكلام ملخبط ميهملوش
    compression_ratio_threshold=2.4,
    # أهم سطر: بنخلي الموديل ميحاولش يتوقع النهاية
    log_prob_threshold=-1.0,
    no_speech_threshold=0.6
)

print("النتيجة الحرفية (بدون تصحيح):")
for segment in segments:
    print(segment.text)