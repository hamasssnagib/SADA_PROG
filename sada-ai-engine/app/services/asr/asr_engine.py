import torch
import numpy as np
import torchaudio

from app.models_loader import arabic_asr_model, arabic_asr_processor


def transcribe_audio(y, sr):

    if isinstance(y, torch.Tensor):
        y = y.numpy()

    if len(y.shape) > 1:
        y = np.mean(y, axis=1)

    if sr != 16000:

        resampler = torchaudio.transforms.Resample(sr, 16000)

        y = torch.tensor(y)

        y = resampler(y).numpy()

    inputs = arabic_asr_processor(
        y,
        sampling_rate=16000,
        return_tensors="pt"
    )

    with torch.no_grad():
        logits = arabic_asr_model(**inputs).logits

    predicted_ids = torch.argmax(logits, dim=-1)

    text = arabic_asr_processor.batch_decode(predicted_ids)[0]

    return text.strip()