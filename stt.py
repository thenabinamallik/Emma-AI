from faster_whisper import WhisperModel

model = WhisperModel("base", compute_type="int8")

BAD_PHRASES = {
    "thank you for watching",
    "subscribe",
    "like and subscribe",
    "see you next time",
}

def transcribe(audio):
    segments, _ = model.transcribe(audio, language="en")
    text = " ".join(seg.text for seg in segments).strip().lower()

    if len(text) < 3:
        return None

    for bad in BAD_PHRASES:
        if bad in text:
            return None

    return text
