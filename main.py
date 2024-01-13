import requests
import json
import html
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk

class Question:
    def __init__(self, text, choices, correct_choice):
        self.text = text
        self.choices = choices
        self.correct_choice = correct_choice

    def check_answer(self, user_answer):
        return user_answer == self.correct_choice

class Quiz:
    def __init__(self):
        self.questions = []
        self.score = 0
        self.current_question = 0

    def add_question(self, question):
        self.questions.append(question)

    def start(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            return question
        else:
            return None

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        else:
            return None

def check_answer(user_answer):
    if quiz.current_question is not None:
        question = quiz.start()
        feedback_label.config(text="", foreground="black")
        if question.check_answer(user_answer):
            feedback_label.config(text="Correct!", foreground="green")
            quiz.score += 1
        else:
            feedback_label.config(text="Wrong. Correct answer: " + html.unescape(question.choices[question.correct_choice - 1]), foreground="red")
        next_q = quiz.next_question()
        if next_q:
            display_question(next_q)
        else:
            end_quiz()

def end_quiz():
    messagebox.showinfo("Quiz Completed", f"Quiz completed. Your score is {quiz.score}/{len(quiz.questions)}.")
    window.destroy()

def display_question(question):
    question_label.config(text=html.unescape(question.text))
    for i, choice in enumerate(question.choices, 1):
        radio_buttons[i - 1].config(text=html.unescape(choice), state="normal")
    submit_button.config(state="normal")

def play_quiz():
    if quiz.start():
        display_question(quiz.start())

# Function to fetch trivia questions from Open Trivia Database
def fetch_trivia_questions():
    url = 'https://opentdb.com/api.php?amount=5&type=multiple'
    response = requests.get(url)
    data = json.loads(response.text)

    for item in data['results']:
        question_text = item['question']
        choices = item['incorrect_answers']
        correct_choice = item['correct_answer']
        choices.append(correct_choice)
        choices = [html.unescape(choice) for choice in choices]
        correct_choice_index = random.randint(1, len(choices))
        question = Question(question_text, choices, correct_choice_index)
        quiz.add_question(question)

quiz = Quiz()
fetch_trivia_questions()

window = ThemedTk(theme="radiance")  # Choose a theme (e.g., "radiance")
window.title("Quiz App")

question_label = ttk.Label(window, text="", wraplength=400)
question_label.pack(pady=20)

feedback_label = ttk.Label(window, text="")
feedback_label.pack()

radio_buttons = []
for i in range(4):
    radio_style = ttk.Style()
    radio_style.configure(f"TRadiobutton{i}.TButton", font=("Arial", 12))
    radio_button = ttk.Radiobutton(window, text="", variable=i, value=i + 1, state="disabled", style=f"TRadiobutton{i}.TButton")
    radio_buttons.append(radio_button)
    radio_button.pack(pady=10)

submit_button = ttk.Button(window, text="Submit", state="disabled", command=lambda: check_answer(i + 1), style='TButton')
submit_button.pack(pady=20)

play_quiz()

window.mainloop()
