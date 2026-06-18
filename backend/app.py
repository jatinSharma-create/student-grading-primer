from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    # TODO: replace with your implementation. This is a mock response
    try:
        students = db.get_all_students()
        return jsonify(students), 200
    except Exception:
        return jsonify({"error": "Failed to retrieve students"}), 404


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    # Getting the request body - replace with your implementation
    try:
        student_data = request.json or {}
        name = student_data.get("name")
        course = student_data.get("course")
        mark = student_data.get("mark")

        
        if not name or not course:
            return jsonify({"error": "Missing required fields: name and course"}), 404

        # Validation/Edge Case: If mark is provided, ensure it's a valid integer
        if mark is not None:
            try:
                mark = int(mark)
            except ValueError:
                return jsonify({"error": "Mark must be a valid integer"}), 404

        new_student = db.insert_student(name, course, mark)
        return jsonify(new_student), 200
    except Exception:
        return jsonify({"error": "Failed to create student"}), 404


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    try:
        student_data = request.json or {}
        name = student_data.get("name")
        course = student_data.get("course")
        mark = student_data.get("mark")

       
        if mark is not None:
            try:
                mark = int(mark)
            except ValueError:
                return jsonify({"error": "Mark must be a valid integer"}), 404

        updated_student = db.update_student(student_id, name, course, mark)
        if not updated_student:
            return jsonify({"error": f"Student with ID {student_id} not found"}), 404

        return jsonify(updated_student), 200
    except Exception:
        return jsonify({"error": "Failed to update student"}), 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    try:
        deleted = db.delete_student(student_id)
        if not deleted:
            return jsonify({"error": f"Student with ID {student_id} not found"}), 404
        return jsonify(deleted), 200
    except Exception:
        return jsonify({"error": "Failed to delete student"}), 404


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    try:
        students = db.get_all_students()
        
       
        marks = [s["mark"] for s in students if s["mark"] is not None]
        count = len(marks)

        # what if the database contains zero students or all students have a mark of null
        if count == 0:
            return jsonify({
                "count": 0,
                "average": 0,
                "min": 0,
                "max": 0
            }), 200

        total_marks = sum(marks)
        average = round(total_marks / count, 2)
        minimum = min(marks)
        maximum = max(marks)

        return jsonify({
            "count": count,
            "average": average,
            "min": minimum,
            "max": maximum
        }), 200
    except Exception:
        return jsonify({"error": "Failed to compute statistics"}), 404


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
