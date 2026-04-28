# import librosa

# from app.services.articulation import articulation_preprocess

# # حطي اسم ملف الصوت هنا
# audio_path = "test_audio.wav"

# y, sr = librosa.load(audio_path, sr=None)

# global_data = {
#     "waveform": y,
#     "sample_rate": sr
# }

# result = articulation_preprocess(global_data)

# print("Sample Rate:", result["sample_rate"])
# print("Confidence:", result["confidence"])
# print("Waveform shape:", result["enhanced_waveform"].shape)




# import librosa
# import soundfile as sf

# from app.services.articulation import articulation_preprocess

# audio_path = "test_audio.wav"

# y, sr = librosa.load(audio_path, sr=None)

# global_data = {
#     "waveform": y,
#     "sample_rate": sr
# }

# result = articulation_preprocess(global_data)

# # حفظ الناتج
# sf.write(
#     "processed_audio.wav",
#     result["enhanced_waveform"],
#     result["sample_rate"]
# )

# print("✅ Processed audio saved!")




import numpy as np

from app.services.articulation.articulation_preprocess import articulation_preprocess

def test_articulation_preprocess():

    # fake audio (1 second)
    y = np.random.randn(16000)
    sr = 16000

    global_data = {
        "waveform": y,
        "sample_rate": sr
    }

    result = articulation_preprocess(global_data)

    # keys check
    assert "enhanced_waveform" in result
    assert "sample_rate" in result
    assert "confidence" in result

    # types check
    assert isinstance(result["enhanced_waveform"], np.ndarray)
    assert result["sample_rate"] == 16000

    # waveform length
    assert len(result["enhanced_waveform"]) > 0

    # normalization check
    assert np.max(np.abs(result["enhanced_waveform"])) <= 1.0

    # confidence valid
    assert result["confidence"] in ["low", "medium", "high"]

    print("✅ All tests passed!")


# تشغيل التست
test_articulation_preprocess()