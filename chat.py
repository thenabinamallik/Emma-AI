from personas import get_persona
from memory import extract, block
import ollama

def ask(text, persona="girl"):
    extract(text)

    prompt = (
        f"{get_persona(persona)}\n\n"
        "Known facts:\n"
        f"{block()}\n\n"
        f"User: {text}\n"
        "You:"
    )

    r = ollama.generate(
        model="gemma3:1b",
        prompt=prompt,
        options={
            "temperature": 0.6,
            "num_predict": 60
        }
    )

    return r["response"].strip()
