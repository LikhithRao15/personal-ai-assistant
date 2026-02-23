from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

model = WhisperModel("small.en", compute_type="int8")


def record_audio(filename="input.wav", duration=5):
    print("Recording...")
    samplerate = 16000

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32"
    )
    sd.wait()

    audio = np.squeeze(audio)

    # Normalize safely
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val

    wav.write(filename, samplerate, audio)


def transcribe(filename="input.wav"):
    segments, _ = model.transcribe(filename)

    text = ""
    for segment in segments:
        text += segment.text

    print("You said:", text)
    return text
