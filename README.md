# CodeAlpha — Language Translation Tool (Task 1)

A simple **desktop translation app** built with Python & Tkinter. Enter text,
choose a source and target language, and get an instant translation powered by
the Google Translate engine (via the free `deep-translator` library — **no API
key required**).

## ✨ Features
- Clean graphical user interface (Tkinter)
- Source + target language selection (with **Auto Detect**)
- Instant translation using Google Translate
- 🔁 **Automatic backup engine** (MyMemory) if Google is busy/rate-limited
- 📋 Copy result to clipboard
- 🔊 Text-to-speech ("Speak" button) — *optional*
- 🧹 Clear button
- Non-blocking UI (translation runs on a background thread)

## 🛠️ Tech Stack
- **Python 3**
- **Tkinter** — GUI (built into Python)
- **deep-translator** — Google Translate API wrapper

## 🚀 How to Run

```bash
# 1. (Optional) create a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

> **Note:** An internet connection is required (the translation engine is online).

## 📖 How It Works
1. User types text and selects languages.
2. On **Translate**, the input is sent to `GoogleTranslator` from `deep-translator`.
3. The translated text is returned and displayed in the result box.
4. The user can copy it or hear it read aloud.

## 📂 Project Structure
```
CodeAlpha_LanguageTranslationTool/
├── app.py            # Main application
├── requirements.txt  # Dependencies
└── README.md         # This file
```

---
**CodeAlpha AI Internship — Task 1** · Built by Abdullah Awan
