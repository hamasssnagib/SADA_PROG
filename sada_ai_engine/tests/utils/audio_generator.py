from gtts import gTTS
import tempfile
import os

def generate_audio(text):

    # 🧠 تحسين النص
    if not text or len(text.strip()) == 0:
        text = "كلام"

    # لو حرف واحد → كرره
    if len(text.strip()) == 1:
        text = text * 4  # س → سسسس

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    filename = tmp.name
    tmp.close()

    # 🎤 generate speech
    tts = gTTS(text=text, lang="ar")
    tts.save(filename)

    # 🛑 تأكد إن الملف اتكتب
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        raise Exception("Audio generation failed")

    return filename