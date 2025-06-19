import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import speech_recognition as sr
import pyttsx3

pdf_text = ""

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def select_pdf():
    global pdf_text
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            pdf_text = text.lower()
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "PDF Loaded Successfully!")

def get_speech_input(prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak(prompt)
        audio = recognizer.listen(source)
        try:
            user_text = recognizer.recognize_google(audio)
            return user_text.lower()
        except:
            return ""

def ask_question():
    global question_text
    question_text = get_speech_input("Please ask your question.")
    result_text.insert(tk.END, "\nQuestion Detected: " + question_text)

def answer_question():
    global question_text
    answer_text = get_speech_input("Please give your answer.")
    result_text.insert(tk.END, "\nAnswer Detected: " + answer_text)

    # Basic match: Find related content from PDF
    if pdf_text:
        paragraphs = pdf_text.split('\n')
        best_match = ""
        max_matches = 0
        question_words = question_text.split()

        for para in paragraphs:
            matches = sum(1 for word in question_words if word in para)
            if matches > max_matches:
                max_matches = matches
                best_match = para

        if best_match:
            expected_words = set(best_match.split())
            user_words = set(answer_text.split())
            missed = expected_words - user_words

            result_text.insert(tk.END, "\nMissed Keywords: " + ', '.join(missed))
            speak("You missed these keywords: " + ', '.join(missed))
        else:
            result_text.insert(tk.END, "\nNo relevant content found in PDF.")
            speak("No relevant content found.")
    else:
        result_text.insert(tk.END, "\nPlease load a PDF first.")
        speak("Please load a PDF first.")

# GUI setup
root = tk.Tk()
root.title("Voice Revision App")

select_btn = tk.Button(root, text="Select PDF", command=select_pdf)
select_btn.pack(pady=5)

ask_btn = tk.Button(root, text="Ask Question (Voice)", command=ask_question)
ask_btn.pack(pady=5)

answer_btn = tk.Button(root, text="Answer Question (Voice)", command=answer_question)
answer_btn.pack(pady=5)

result_text = tk.Text(root, height=20, width=60)
result_text.pack(pady=10)

root.mainloop()
