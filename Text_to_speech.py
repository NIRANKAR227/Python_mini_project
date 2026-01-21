from gtts import gTTS
import os
import tkinter as tk
from tkinter import filedialog, messagebox

root = tk.Tk()
root.title("Text to Speech")
root.geometry("400x300")

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# ---------- Functions ----------

def open_file():
    filename = filedialog.askopenfilename(
        title="Select a text file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if filename:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                text = f.read()
            speak(text)
        except Exception as e:
            messagebox.showerror("Error", str(e))


def speak(text):
    if not text.strip():
        messagebox.showwarning("Warning", "No text to convert!")
        return

    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save("output.mp3")
        os.startfile("output.mp3")   # Windows
    except Exception as e:
        messagebox.showerror("Error", str(e))


def text_to_speech():
    text = entry.get()
    speak(text)


# ---------- UI ----------

title = tk.Label(root, text="Text To Speech", font=("Arial", 14, "bold"))
canvas.create_window(200, 40, window=title)

entry = tk.Entry(root, width=40)
canvas.create_window(200, 120, window=entry)

btn_entry = tk.Button(root, text="Speak Typed Text",
                      command=text_to_speech)
canvas.create_window(200, 170, window=btn_entry)

btn_file = tk.Button(root, text="Speak From File",
                     command=open_file)
canvas.create_window(200, 210, window=btn_file)

root.mainloop()
