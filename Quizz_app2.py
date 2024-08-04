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
        correct_keys = [key.strip().lower() for key in row['Correcta'].split(',')]
        question = {
            'question': row['Pregunta'],
            'answers': {'a': row['a'], 'b': row['b'], 'c': row['c'], 'd': row['d'], 'e': row['e']},
            'correct': correct_keys
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
        self.correct_count = 0
        self.incorrect_count = 0
        self.create_widgets()

    def create_widgets(self):
        # Etiqueta para la pregunta
        self.question_label = tk.Label(self.root, text="", font=("Arial", 16), wraplength=400)
        self.question_label.pack(pady=20)

        # Etiquetas para los contadores
        self.correct_label = tk.Label(self.root, text="Respuestas correctas: 0", font=("Arial", 14))
        self.correct_label.pack(pady=5)

        self.incorrect_label = tk.Label(self.root, text="Respuestas incorrectas: 0", font=("Arial", 14))
        self.incorrect_label.pack(pady=5)

        # Casillas de verificación para las respuestas
        self.check_vars = {}
        self.check_buttons = {}
        for key in ['a', 'b', 'c', 'd', 'e']:
            var = tk.BooleanVar()
            check_button = tk.Checkbutton(self.root, text="", font=("Arial", 14), variable=var)
            check_button.pack(pady=5, fill="both", expand=True)
            self.check_vars[key] = var
            self.check_buttons[key] = check_button

        # Botón para enviar respuesta
        self.submit_button = tk.Button(self.root, text="Enviar Respuesta", font=("Arial", 14), command=self.check_answer)
        self.submit_button.pack(pady=20)

        # Botón para la siguiente pregunta
        self.next_button = tk.Button(self.root, text="Siguiente", font=("Arial", 14), command=self.next_question)
        self.next_button.pack(pady=20)
        self.next_button.config(state=tk.DISABLED)

        # Mostrar la primera pregunta
        self.display_question()

    def display_question(self):
        question = questions[self.current_question]
        self.question_label.config(text=question['question'])
        for key, button in self.check_buttons.items():
            button.config(text=f"{key.upper()}. {question['answers'][key]}", state=tk.NORMAL)
            self.check_vars[key].set(False)  # Reset the checkbox state
        self.submit_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)

    def check_answer(self):
        question = questions[self.current_question]
        selected_keys = [key for key, var in self.check_vars.items() if var.get()]
        correct_keys = question['correct']

        print(f"Selected: {selected_keys}")
        print(f"Correct: {correct_keys}")

        # Comprobar si todas las respuestas seleccionadas están en las respuestas correctas
        if set(selected_keys) == set(correct_keys):
            self.score += 1
            self.correct_count += 1
            messagebox.showinfo("Respuesta", "¡Correcto!")
        else:
            self.incorrect_count += 1
            correct_answers = [f"{k.upper()}: {question['answers'].get(k, 'No disponible')}" for k in correct_keys]
            messagebox.showinfo("Respuesta", f"Incorrecto. Las respuestas correctas son: {', '.join(correct_answers)}")

        # Actualizar los contadores en la interfaz
        self.correct_label.config(text=f"Respuestas correctas: {self.correct_count}")
        self.incorrect_label.config(text=f"Respuestas incorrectas: {self.incorrect_count}")

        for button in self.check_buttons.values():
            button.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(questions):
            self.display_question()
        else:
            messagebox.showinfo("Fin del Quiz", f"Tu puntuación es: {self.score}/{len(questions)}\n"
                                                f"Respuestas correctas: {self.correct_count}\n"
                                                f"Respuestas incorrectas: {self.incorrect_count}")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
    