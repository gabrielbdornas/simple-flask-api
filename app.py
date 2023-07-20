from flask import Flask
from data import students

app = Flask(__name__)

@app.route('/students', methods=['GET'])
def get():
    return students

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    return students.get(
        student_id,
        {'error': 'Student not found'}
    )
