from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

MODEL_PATH = "app/models/jonatasgrosman_arabic"
# MODEL_PATH = "app/models/elgeish_arabic"
print("Loading Arabic ASR model...")

arabic_asr_processor = Wav2Vec2Processor.from_pretrained(MODEL_PATH)
arabic_asr_model = Wav2Vec2ForCTC.from_pretrained(MODEL_PATH)

print("ASR model loaded ✔")




# import os
# import soundfile as sf

# from faster_whisper import WhisperModel


# # =========================================================
# # BASE PATH
# # =========================================================

# BASE_PATH = os.path.abspath("app/models")


# # =========================================================
# # WHISPER MODEL
# # =========================================================

# WHISPER_MODEL_PATH = os.path.join(
#     BASE_PATH,
#     "whisper_fast"
# )

# print("Loading Whisper model...")

# whisper_model = WhisperModel(
#     WHISPER_MODEL_PATH,
#     device="cpu",
#     compute_type="int8"
# )

# print("Whisper loaded ✔")


# # =========================================================
# # Fake Wav2Vec Processor
# # =========================================================

# class FakeProcessor:

#     def __call__(self, speech, sampling_rate=16000, return_tensors="pt"):

#         return {
#             "speech": speech,
#             "sr": sampling_rate
#         }

#     def batch_decode(self, predicted_ids):

#         return predicted_ids


# # =========================================================
# # Fake Wav2Vec Model
# # =========================================================

# class FakeModel:

#     def __call__(self, **inputs):

#         speech = inputs["speech"]
#         sr = inputs["sr"]

#         temp_file = "temp_asr.wav"
#         sf.write(temp_file, speech, sr)

#         segments, _ = whisper_model.transcribe(
#             temp_file,
#             language="ar"
#         )

#         text = " ".join([seg.text for seg in segments])

#         os.remove(temp_file)

#         class Output:
#             logits = [text]

#         return Output()


# =========================================================
# EXPORT SAME VARIABLES AS WAV2VEC
# =========================================================

# arabic_asr_processor = FakeProcessor()
# arabic_asr_model = FakeModel()



# import os
# from faster_whisper import WhisperModel
# from allosaurus.app import read_recognizer
# from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC


# # =========================================================
# # BASE MODELS PATH
# # =========================================================

# BASE_PATH = os.path.abspath("app/models")


# # =========================================================
# # WHISPER
# # =========================================================

# WHISPER_PATH = os.path.join(
#     BASE_PATH,
#     "whisper-small-ar"
# )

# print("Loading Whisper model...")

# whisper_model = WhisperModel(
#     WHISPER_PATH,
#     device="cpu",
#     compute_type="int8"
# )

# print("Whisper loaded ✔")


# # =========================================================
# # ALLOSAURUS
# # =========================================================

# print("Loading Allosaurus phoneme model...")

# allosaurus_model = read_recognizer()

# print("Allosaurus loaded ✔")


# # =========================================================
# # ARABIC ASR MODEL
# # =========================================================

# ARABIC_ASR_PATH = os.path.join(
#     BASE_PATH,
#     "jonatasgrosman_arabic"
# )

# print("Loading Arabic wav2vec2 model...")

# arabic_asr_processor = Wav2Vec2Processor.from_pretrained(
#     ARABIC_ASR_PATH
# )

# arabic_asr_model = Wav2Vec2ForCTC.from_pretrained(
#     ARABIC_ASR_PATH
# )

# print("Arabic ASR loaded ✔")




# import os

# from faster_whisper import WhisperModel
# from allosaurus.app import read_recognizer

# from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC


# # =========================================================
# # BASE PATH
# # =========================================================

# BASE_PATH = os.path.abspath("app/models")


# # =========================================================
# # WHISPER MODEL
# # =========================================================

# WHISPER_MODEL_PATH = os.path.join(
#     BASE_PATH,
#     "whisper",
#     "whisper-medium-ct2"
# )

# print("Loading Whisper model...")

# whisper_model = WhisperModel(
#     WHISPER_MODEL_PATH,
#     device="cpu",
#     compute_type="int8"
# )

# print("Whisper loaded ✔")


# # =========================================================
# # ALLOSAURUS PHONEME MODEL
# # =========================================================

# print("Loading phoneme model (Allosaurus)...")

# allosaurus_model = read_recognizer()

# print("Phoneme model loaded ✔")


# # =========================================================
# # ARABIC ASR MODEL (NEW)
# # =========================================================

# ARABIC_ASR_PATH = os.path.join(
#     BASE_PATH,
#     "wav2vec2-arabic"
# )

# print("Loading Arabic ASR model...")

# arabic_asr_processor = Wav2Vec2Processor.from_pretrained(
#     ARABIC_ASR_PATH
# )

# arabic_asr_model = Wav2Vec2ForCTC.from_pretrained(
#     ARABIC_ASR_PATH
# )

# print("Arabic ASR loaded ✔")










# # from faster_whisper import WhisperModel
# # from allosaurus.app import read_recognizer
# # import os


# # # ------------------------------------
# # # Paths
# # # ------------------------------------

# # WHISPER_PATH = os.path.abspath(
# #     "app/services/models/whisper"
# # )

# # # ------------------------------------
# # # Whisper model
# # # ------------------------------------

# # print("Loading faster-whisper model...")

# # whisper_model = WhisperModel(
# #     "medium",
# #     device="cpu",
# #     compute_type="int8"
# # )

# # print("Whisper loaded ✔")


# # # ------------------------------------
# # # Allosaurus phoneme model
# # # ------------------------------------

# # print("Loading phoneme model...")

# # allosaurus_model = read_recognizer()

# # print("Phoneme model loaded ✔")









# # # import os
# # # import torch
# # # from transformers import (
# # #     AutoProcessor,
# # #     AutoModelForSpeechSeq2Seq,
# # #     Wav2Vec2Processor,
# # #     Wav2Vec2ForCTC
# # # )

# # # # =========================================================
# # # # Paths (ALL MODELS INSIDE services/models)
# # # # =========================================================

# # # BASE_PATH = os.path.abspath("app/services/models")

# # # WHISPER_PATH = os.path.join(BASE_PATH, "whisper-small-ar")
# # # PHONEME_PATH = os.path.join(BASE_PATH, "wav2vec2-phoneme")


# # # # =========================================================
# # # # Device Configuration (CPU Safe)
# # # # =========================================================

# # # DEVICE = "cpu"
# # # DTYPE = torch.float32


# # # # =========================================================
# # # # Whisper (Arabic ASR - for validation layer only)
# # # # =========================================================

# # # print("Loading Whisper-small-ar model...")

# # # whisper_processor = AutoProcessor.from_pretrained(WHISPER_PATH)
# # # whisper_model = AutoModelForSpeechSeq2Seq.from_pretrained(
# # #     WHISPER_PATH,
# # #     torch_dtype=DTYPE
# # # ).to(DEVICE)

# # # whisper_model.eval()

# # # print("Whisper loaded ✅")


# # # # =========================================================
# # # # Wav2Vec2 Phoneme Model (for articulation detection)
# # # # =========================================================

# # # print("Loading wav2vec2 phoneme model...")

# # # phoneme_processor = Wav2Vec2Processor.from_pretrained(PHONEME_PATH)
# # # phoneme_model = Wav2Vec2ForCTC.from_pretrained(PHONEME_PATH).to(DEVICE)

# # # phoneme_model.eval()

# # # print("Phoneme model loaded ✅")









# # # # from faster_whisper import WhisperModel
# # # # from allosaurus.app import read_recognizer
# # # # import os

# # # # WHISPER_MODEL_PATH = os.path.abspath(
# # # #     "app/models/whisper/whisper-medium-ct2"
# # # # )

# # # # # CPU-safe configuration
# # # # whisper_model = WhisperModel(
# # # #     WHISPER_MODEL_PATH,
# # # #     device="cpu",
# # # #     compute_type="int8"   # 🔥 IMPORTANT CHANGE
# # # # )

# # # # allosaurus_model = read_recognizer()




# # # # from faster_whisper import WhisperModel
# # # # from allosaurus.app import read_recognizer
# # # # import os

# # # # # -------------------------------------------------
# # # # # Local Whisper CT2 model path
# # # # # -------------------------------------------------
# # # # WHISPER_MODEL_PATH = os.path.abspath(
# # # #     "app/models/whisper/whisper-medium-ct2"
# # # # )

# # # # # IMPORTANT:
# # # # # use local path directly (not "medium")
# # # # whisper_model = WhisperModel(
# # # #     WHISPER_MODEL_PATH,
# # # #     device="cpu",
# # # #     compute_type="float16"
# # # # )

# # # # # -------------------------------------------------
# # # # # Allosaurus model
# # # # # -------------------------------------------------
# # # # allosaurus_model = read_recognizer()








# # # # # """
# # # # # Centralized model loader for SADA AI Engine
# # # # # Loads Faster-Whisper (CTranslate2) and Allosaurus once.
# # # # # """

# # # # # import os
# # # # # from faster_whisper import WhisperModel
# # # # # from allosaurus.app import read_recognizer

# # # # # BASE_DIR = os.path.dirname(os.path.dirname("app/models"))

# # # # # # --------------------------------------------------
# # # # # # Whisper CTranslate2 Model Path
# # # # # # --------------------------------------------------
# # # # # WHISPER_PATH = os.path.join(
# # # # #     BASE_DIR,
# # # # #     "models",
# # # # #     "whisper",
# # # # #     "whisper-medium-ct2"
# # # # # )

# # # # # # Load Whisper
# # # # # whisper_model = WhisperModel(
# # # # #     WHISPER_PATH,
# # # # #     device="cpu",          # change to "cuda" if GPU available
# # # # #     compute_type="float16"
# # # # # )

# # # # # # --------------------------------------------------
# # # # # # Load Allosaurus once
# # # # # # --------------------------------------------------
# # # # # allosaurus_model = read_recognizer()