from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

# اسم الموديل اللي بيطلع الحروف زي ما اتنطقت بالظبط بدون تصحيح
model_name = "elgeish/wav2vec2-base-ar-vocab"

# المسار اللي هتحفظي فيه الموديل على جهازك
# غيري المسار ده للمكان اللي يريحك، مثلا: "D:/SpeechModels/wav2vec-ar"
save_directory = "D:/phoneme"

print("جاري تحميل الموديل... (الموديل ده حجمه خفيف وهينزل بسرعة إن شاء الله)")

# 1. تنزيل وحفظ المعالج (Processor) اللي بيتعامل مع الترددات الصوتية
processor = Wav2Vec2Processor.from_pretrained(model_name)
processor.save_pretrained(save_directory)

# 2. تنزيل وحفظ الموديل نفسه (Acoustic Model) اللي بيحول الصوت لحروف
model = Wav2Vec2ForCTC.from_pretrained(model_name)
model.save_pretrained(save_directory)

print(f"تم تحميل الموديل بنجاح وحفظه بالكامل في: {save_directory}")