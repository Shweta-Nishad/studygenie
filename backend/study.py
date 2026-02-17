from flask import Blueprint, request, jsonify, session
import os
import random

study = Blueprint("study", __name__)

@study.route("/upload_syllabus", methods=["POST"])
def upload_syllabus():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})
    file = request.files["file"]
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)
    return jsonify({"message": "File uploaded successfully"})

@study.route("/generate_plan", methods=["GET"])
def generate_plan():
    subjects = ["Math", "Physics", "ML", "Python"]
    plan = {day: random.choice(subjects) for day in range(1, 8)}
    return jsonify(plan)
