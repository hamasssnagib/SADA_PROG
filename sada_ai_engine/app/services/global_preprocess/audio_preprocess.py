import librosa
import numpy as np
import io
import soundfile as sf
# convert to mono and resample to 16kHz 
TARGET_SR = 16000
# This module provides functions to preprocess audio data for global analysis, including loading, normalizing, trimming silence, and extracting features such as duration, RMS energy, zero-crossing rate, spectral centroid, and speech ratio.
# The preprocess_audio function takes raw audio bytes as input and returns a dictionary containing the processed waveform, sample rate, and extracted features.

def load_audio(audio_bytes):
    # Load audio from bytes, convert to mono, and resample to TARGET_SR
    y, sr = librosa.load(
        # Use soundfile to read the audio bytes and then resample with librosa
        io.BytesIO(audio_bytes),
        sr=TARGET_SR,
        mono=True
    )
    # Ensure the audio is in the range [-1, 1]
    y = librosa.util.normalize(y)
    return y, sr

# Normalize the audio to ensure consistent amplitude levels across different recordings, which can improve the accuracy of feature extraction and subsequent analysis.
def normalize_audio(y):
    # librosa.util.normalize scales the audio signal to have a maximum absolute value of 1, which helps to prevent clipping and ensures that the features extracted are not biased by varying volume levels across different audio samples.
    return librosa.util.normalize(y)


# Trim leading and trailing silence from the audio signal to focus the analysis on the actual speech content, which can improve the accuracy of feature extraction and reduce noise in the analysis.
def trim_silence(y):
    # librosa.effects.trim removes leading and trailing silence from the audio signal based on a specified decibel threshold (top_db). This helps to focus the analysis on the actual speech content, improving the accuracy of feature extraction and reducing noise in the analysis.
    yt, _ = librosa.effects.trim(y, top_db=25)
    return yt


# Extract global features from the audio signal, including duration, RMS energy, zero-crossing rate, spectral centroid, and speech ratio. These features provide insights into the overall characteristics of the audio, such as its length, energy level, frequency content, and the proportion of speech versus silence.
def extract_global_features(y, sr):
    # duration is calculated using librosa.get_duration, which computes the total length of the audio signal in seconds based on the number of samples and the sample rate. This feature provides insight into the overall length of the audio recording, which can be important for various analyses, such as determining if the recording is long enough for certain types of processing or if it meets specific duration requirements for analysis.
    duration = librosa.get_duration(y=y, sr=sr)
    #rms energy is calculated using librosa.feature.rms, which computes the root mean square (RMS) energy of the audio signal. The RMS energy provides a measure of the overall loudness or intensity of the audio, which can be useful for distinguishing between different types of sounds (e.g., speech vs. background noise) and for analyzing the dynamics of the audio signal.
    rms = np.mean(librosa.feature.rms(y=y))
    # zero-crossing rate is calculated using librosa.feature.zero_crossing_rate, which computes the rate at which the audio signal changes sign (i.e., crosses the zero amplitude line). The zero-crossing rate can provide insights into the noisiness or complexity of the audio signal, as higher rates may indicate more complex or noisy audio, while lower rates may indicate smoother or more tonal audio. 
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    # spectral centroid is calculated using librosa.feature.spectral_centroid, which computes the "center of mass" of the spectrum of the audio signal. The spectral centroid provides information about the brightness or timbre of the audio, with higher values indicating a brighter sound and lower values indicating a darker sound. This feature can be useful for distinguishing between different types of sounds and for analyzing the frequency content of the audio signal.
    spectral_centroid = np.mean(
        librosa.feature.spectral_centroid(y=y, sr=sr)
    )

    # نسبة الكلام مقابل الصمت
    # speech ratio is calculated by using librosa.effects.split to identify the intervals of the audio signal that contain speech (i.e., non-silent segments) based on a specified decibel threshold (top_db). The total number of samples in these speech intervals is then summed and divided by the total number of samples in the original audio signal to compute the speech ratio. This feature provides insight into the proportion of the audio that contains speech versus silence, which can be useful for analyzing the overall content of the audio and for distinguishing between recordings with varying levels of speech activity.
    intervals = librosa.effects.split(y, top_db=25)
    speech_samples = sum([end - start for start, end in intervals])
    speech_ratio = speech_samples / len(y)

    # The extracted features are returned as a dictionary, which can be easily accessed and used for further analysis or processing in the context of global audio analysis. This structured format allows for efficient integration with other components of the audio processing pipeline, such as machine learning models or visualization tools.
    return {
        "duration": float(duration),
        "rms_energy": float(rms),
        "zero_crossing_rate": float(zcr),
        "spectral_centroid_mean": float(spectral_centroid),
        "speech_ratio": float(speech_ratio)
    }
    
    

# The preprocess_audio function serves as the main entry point for processing raw audio data. It takes audio bytes as input, loads and preprocesses the audio signal, and extracts relevant features that can be used for global analysis. The returned dictionary contains the processed waveform, sample rate, and extracted features, which can be utilized in various applications such as speech analysis, emotion detection, or other audio-related tasks.
def preprocess_audio(audio_bytes):
    # Load the audio from bytes, convert to mono, and resample to TARGET_SR
    y, sr = load_audio(audio_bytes)
    # Normalize the audio to ensure consistent amplitude levels across different recordings, which can improve the accuracy of feature extraction and subsequent analysis.
    y = normalize_audio(y)
    # Trim leading and trailing silence from the audio signal to focus the analysis on the actual speech content, which can improve the accuracy of feature extraction and reduce noise in the analysis.
    y = trim_silence(y)
    # Extract global features from the audio signal, including duration, RMS energy, zero-crossing rate, spectral centroid, and speech ratio. These features provide insights into the overall characteristics of the audio, such as its length, energy level, frequency content, and the proportion of speech versus silence.
    features = extract_global_features(y, sr)
    # The preprocess_audio function serves as the main entry point for processing raw audio data. It takes audio bytes as input, loads and preprocesses the audio signal, and extracts relevant features that can be used for global analysis. The returned dictionary contains the processed waveform, sample rate, and extracted features, which can be utilized in various applications such as speech analysis, emotion detection, or other audio-related tasks.
    return {
        "waveform": y,
        "sample_rate": sr,
        **features
    }