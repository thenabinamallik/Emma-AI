import json, os

FILE = "memory.json"

def load():
    if not os.path.exists(FILE):
        return {"facts": []}
    return json.load(open(FILE))

def save(mem):
    json.dump(mem, open(FILE, "w"), indent=2)

memory = load()

def extract(text):
    triggers = ["i am", "i'm", "my name is", "i like", "i love"]
    if any(t in text.lower() for t in triggers):
        if text not in memory["facts"]:
            memory["facts"].append(text)
            memory["facts"] = memory["facts"][-30:]
            save(memory)

def block():
    facts = memory["facts"][-5:]
    return "\n".join(f"- {f}" for f in facts) if facts else "- none"
