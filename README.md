# Emma – Local AI Assistant 🤖

Emma is a modular, offline-capable AI assistant built using local large language models.  
It supports persistent conversation memory, natural dialogue, and offline voice output.

This project focuses on **system design**, not model training.

---

## ✨ Features

- 🧠 Persistent conversation memory (SQLite)
- 💬 Context-aware responses
- 🔒 Offline-first (no cloud dependency)
- 🗣 Voice output using Piper TTS
- ⚙ Modular and extensible architecture
- 🚀 Lightweight and fast

---

## 🏗 Architecture

User Input → Assistant Logic → Local LLM (Ollama)
→ Response → Text + Voice Output

---

## 🛠 Technologies

- Python 3
- Ollama (Local LLM runtime)
- SQLite
- Piper TTS
- SoundDevice / SoundFile

---

## 📦 Setup

### 1. Install dependencies
```bash
pip install requirements.txt
```
### 2. Run Ollama
```bash
ollama pull phi3
ollama serve
```
### 3. Run Emma
```bash
python main.py
```

## 🎯 Project Goal

To demonstrate how a local AI assistant system can be built with memory, modularity, and offline capabilities, serving as a foundation for future automation and IoT integration.

## 🔮 Future Plans

- Command execution

- Hardware & IoT integration

- Email and task automation

- Speech input

- Cloud–local hybrid model support

## 📜 License

This project is intended for educational use.


