from gtts import gTTS
from pydub import AudioSegment
import os

# الكلمة اللي عاوزاها
text = "أينب"

# 1. توليد الصوت وحفظه كـ mp3 مؤقت
tts = gTTS(text=text, lang='ar')
tts.save("temp.mp3")

# 2. قراءة الـ mp3 وتحويله لـ wav
sound = AudioSegment.from_mp3("temp.mp3")
sound.export("أينب.wav", format="wav")

# 3. مسح ملف الـ mp3 المؤقت عشان النضافة 
os.remove("temp.mp3")

print("تم حفظ الصوت بنجاح بصيغة wav!")