import pvporcupine
import pyaudio
import struct

ACCESS_KEY = "PASTE_YOUR_KEY_HERE"

def detect_wake_word():
    porcupine = pvporcupine.create(
        access_key="ZNsXn359UPt36s56AwrqFTt8Iidl/pFAXpC7Z9U/Ep+MijU5cY8Oew==",
        keywords=["jarvis"]
    )

    pa = pyaudio.PyAudio()

    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Waiting for wake word...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if porcupine.process(pcm) >= 0:
                print("Wake word detected!")
                break
    finally:
        stream.close()
        pa.terminate()
        porcupine.delete()
