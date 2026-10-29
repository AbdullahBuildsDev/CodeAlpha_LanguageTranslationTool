"""
CodeAlpha - Task 1: Language Translation Tool
-------------------------------------------------
A simple desktop app (Tkinter GUI) that lets the user type text,
pick a source and target language, and translate it using the
Google Translate engine (via the free `deep-translator` library).

Features:
  - Text input box
  - Source + target language dropdowns (with "auto" detect)
  - Translate button
  - Result box
  - Copy to clipboard button
  - Speak button (text-to-speech) - optional feature

Author: Abdullah Awan  |  CodeAlpha AI Internship
"""

import threading
import tkinter as tk
from tkinter import ttk, messagebox

from deep_translator import GoogleTranslator, MyMemoryTranslator


# A short, friendly list of common languages.
# Each maps to: (Google Translate code, MyMemory regional code)
# Google is the primary engine; MyMemory is a free backup used if Google is busy.
LANGUAGES = {
    "Auto Detect": ("auto", None),
    "English": ("en", "en-GB"),
    "Urdu": ("ur", "ur-PK"),
    "Hindi": ("hi", "hi-IN"),
    "Arabic": ("ar", "ar-SA"),
    "Spanish": ("es", "es-ES"),
    "French": ("fr", "fr-FR"),
    "German": ("de", "de-DE"),
    "Chinese (Simplified)": ("zh-CN", "zh-CN"),
    "Japanese": ("ja", "ja-JP"),
    "Russian": ("ru", "ru-RU"),
    "Portuguese": ("pt", "pt-PT"),
    "Turkish": ("tr", "tr-TR"),
}


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        root.title("CodeAlpha - Language Translation Tool")
        root.geometry("640x560")
        root.configure(bg="#f2f4f8")

        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        title = tk.Label(
            self.root,
            text="🌐 Language Translation Tool",
            font=("Helvetica", 18, "bold"),
            bg="#f2f4f8",
            fg="#1a1a2e",
        )
        title.pack(pady=(16, 4))

        subtitle = tk.Label(
            self.root,
            text="CodeAlpha AI Internship - Task 1",
            font=("Helvetica", 10),
            bg="#f2f4f8",
            fg="#555",
        )
        subtitle.pack(pady=(0, 12))

        # --- Input text ---
        tk.Label(self.root, text="Enter text:", bg="#f2f4f8",
                 font=("Helvetica", 11, "bold")).pack(anchor="w", padx=20)
        self.input_text = tk.Text(self.root, height=6, font=("Helvetica", 11),
                                  wrap="word", relief="solid", bd=1)
        self.input_text.pack(fill="x", padx=20, pady=(2, 10))

        # --- Language selectors ---
        lang_frame = tk.Frame(self.root, bg="#f2f4f8")
        lang_frame.pack(fill="x", padx=20)

        tk.Label(lang_frame, text="From:", bg="#f2f4f8",
                 font=("Helvetica", 10)).grid(row=0, column=0, sticky="w")
        self.source_var = tk.StringVar(value="Auto Detect")
        ttk.Combobox(lang_frame, textvariable=self.source_var,
                     values=list(LANGUAGES.keys()), state="readonly",
                     width=22).grid(row=1, column=0, padx=(0, 10), pady=4)

        tk.Label(lang_frame, text="To:", bg="#f2f4f8",
                 font=("Helvetica", 10)).grid(row=0, column=1, sticky="w")
        self.target_var = tk.StringVar(value="English")
        ttk.Combobox(lang_frame, textvariable=self.target_var,
                     values=[k for k in LANGUAGES if k != "Auto Detect"],
                     state="readonly", width=22).grid(row=1, column=1, pady=4)

        # --- Translate button ---
        self.translate_btn = tk.Button(
            self.root, text="Translate  ➜", command=self.start_translation,
            bg="#4361ee", fg="white", font=("Helvetica", 12, "bold"),
            relief="flat", padx=20, pady=8, activebackground="#3a0ca3",
            cursor="hand2",
        )
        self.translate_btn.pack(pady=14)

        # --- Output text ---
        tk.Label(self.root, text="Translation:", bg="#f2f4f8",
                 font=("Helvetica", 11, "bold")).pack(anchor="w", padx=20)
        self.output_text = tk.Text(self.root, height=6, font=("Helvetica", 11),
                                   wrap="word", relief="solid", bd=1,
                                   bg="#ffffff", state="disabled")
        self.output_text.pack(fill="x", padx=20, pady=(2, 10))

        # --- Action buttons ---
        btn_frame = tk.Frame(self.root, bg="#f2f4f8")
        btn_frame.pack()
        tk.Button(btn_frame, text="📋 Copy", command=self.copy_result,
                  relief="flat", bg="#e0e0e0", padx=12, pady=5,
                  cursor="hand2").grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="🔊 Speak", command=self.speak_result,
                  relief="flat", bg="#e0e0e0", padx=12, pady=5,
                  cursor="hand2").grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="🧹 Clear", command=self.clear_all,
                  relief="flat", bg="#e0e0e0", padx=12, pady=5,
                  cursor="hand2").grid(row=0, column=2, padx=6)

        # --- Status bar ---
        self.status = tk.Label(self.root, text="Ready", bg="#f2f4f8",
                               fg="#777", font=("Helvetica", 9))
        self.status.pack(side="bottom", pady=6)

    # ---------- Logic ----------
    def start_translation(self):
        """Run translation in a background thread so the UI never freezes."""
        text = self.input_text.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Empty", "Please enter some text to translate.")
            return

        self.translate_btn.config(state="disabled")
        self.status.config(text="Translating...")
        threading.Thread(target=self._translate, args=(text,), daemon=True).start()

    def _translate(self, text):
        src_g, src_m = LANGUAGES[self.source_var.get()]
        tgt_g, tgt_m = LANGUAGES[self.target_var.get()]

        # Primary engine: Google Translate (supports auto-detect).
        try:
            result = GoogleTranslator(source=src_g, target=tgt_g).translate(text)
            self.root.after(0, self._show_result, result, "Done ✓ (Google)")
            return
        except Exception:
            pass  # Google busy/rate-limited -> try the backup engine below.

        # Backup engine: MyMemory (free, no API key). Needs a specific source.
        try:
            backup_src = src_m or "en-GB"   # MyMemory can't auto-detect
            result = MyMemoryTranslator(source=backup_src, target=tgt_m).translate(text)
            self.root.after(0, self._show_result, result, "Done ✓ (backup engine)")
        except Exception as e:
            self.root.after(0, self._show_result, "",
                            f"Translation failed (both engines busy): {e}")

    def _show_result(self, result, status):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.output_text.config(state="disabled")
        self.status.config(text=status)
        self.translate_btn.config(state="normal")

    def copy_result(self):
        text = self.output_text.get("1.0", "end").strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.status.config(text="Copied to clipboard ✓")

    def speak_result(self):
        """Optional text-to-speech. Tries pyttsx3, falls back to the mac `say` command."""
        text = self.output_text.get("1.0", "end").strip()
        if not text:
            return
        threading.Thread(target=self._speak, args=(text,), daemon=True).start()

    def _speak(self, text):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception:
            # Fallback for macOS (built-in "say" command)
            import subprocess
            try:
                subprocess.run(["say", text], check=False)
            except Exception:
                self.root.after(0, lambda: self.status.config(
                    text="Text-to-speech not available on this system"))

    def clear_all(self):
        self.input_text.delete("1.0", "end")
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.config(state="disabled")
        self.status.config(text="Ready")


if __name__ == "__main__":
    root = tk.Tk()
    TranslatorApp(root)
    root.mainloop()
