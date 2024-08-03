import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random

# Leer preguntas desde el archivo Excel
def load_questions_from_excel(file_path):
    df = pd.read_excel(file_path)
    print("Columnas del archivo Excel:", df.columns)  # Verificar nombres de columnas
    questions = []
    for _, row in df.iterrows():
        question = {
            'question': row['Pregunta'],
            'answers': {'a': row['a'], 'b': row['b'], 'c': row['c'], 'd': row['d'], 'e': row['e']},
            'correct': row['Correcta'].strip().lower()  # Convertir a minúsculas
        }
        questions.append(question)
    return questions

# Cargar preguntas desde el archivo Excel
questions = load_questions_from_excel('questions.xlsx')

# Barajar las preguntas
random.shuffle(questions)

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.score = 0
        self.current_question = 0
        self.create_widgets()

    def create_widgets(self):
        self.question_label = tk.Label(self.root, text="", font=("Arial", 16), wraplength=400)
        self.question_label.pack(pady=20)

        self.answer_buttons = {}
        for key in ['a', 'b', 'c', 'd', 'e']:
            button = tk.Button(self.root, text="", font=("Arial", 14), command=lambda k=key: self.check_answer(k))
            button.pack(pady=5, fill="both", expand=True)
            self.answer_buttons[key] = button

        self.next_button = tk.Button(self.root, text="Siguiente", font=("Arial", 14), command=self.next_question)
        self.next_button.pack(pady=20)
        self.next_button.config(state=tk.DISABLED)

        self.display_question()

    def display_question(self):
        question = questions[self.current_question]
        self.question_label.config(text=question['question'])
        for key, button in self.answer_buttons.items():
            button.config(text=f"{key.upper()}. {question['answers'][key]}", state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)

    def check_answer(self, key):
        question = questions[self.current_question]
        if key == question['correct']:
            self.score += 1
            messagebox.showinfo("Respuesta", "¡Correcto!")
        else:
            correct_key = question['correct']
            correct_answer = question['answers'][correct_key]
            messagebox.showinfo("Respuesta", f"Incorrecto. La respuesta correcta es {correct_key.upper()}: {correct_answer}")
        for button in self.answer_buttons.values():
            button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(questions):
            self.display_question()
        else:
            messagebox.showinfo("Fin del Quiz", f"Tu puntuación es: {self.score}/{len(questions)}")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
