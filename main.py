from mic import record_until_silence
from stt import transcribe
from chat import ask
from voice import speak
from config import WAKE_WORD

print("🎙 Emma is listening...\n")

while True:
    audio = record_until_silence()
    if audio is None:
        continue

    text = transcribe(audio)
    if not text:
        continue

    print("Heard:", text)

    # if WAKE_WORD not in text:
    #     continue

    # print("🔔 Wake word detected")

    # command = text.split(WAKE_WORD, 1)[-1].strip()
    # if not command:
    #     continue

    reply = ask(text)
    print("Emma:", reply)
    speak(reply)
