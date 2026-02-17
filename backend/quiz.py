from flask import Blueprint, jsonify
import random

quiz = Blueprint("quiz", __name__)

@quiz.route("/generate_quiz", methods=["GET"])
def generate_quiz():
    questions = [
        {"question": "What is ML?", "options": ["A", "B", "C"], "answer": "A"},
        {"question": "What is Python?", "options": ["Language", "Snake"], "answer": "Language"},
    ]
    return jsonify(random.sample(questions, 2))
