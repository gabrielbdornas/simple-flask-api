from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
json.provider.DefaultJSONProvider.ensure_ascii = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    room = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Student('{self.name}', '{self.email}', '{self.room}')"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route('/students', methods=['GET'])
def get():
    students = Student.query.all()
    return jsonify([student.as_dict() for student in students])


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if student:
        return student.as_dict()
    else:
        return {'error': 'Student not found'}

@app.route('/students', methods=['POST'])
def create():
    new_student = Student(
        name=request.json['name'],
        email=request.json['email'],
        room=request.json['room'],
        )
    db.session.add(new_student)
    db.session.commit()
    return new_student.as_dict()

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete(student_id):
    student = Student.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return {'data': 'Student deleted successfully.'}
    else:
        return {'error': 'Student not found.'}

@app.route('/students/<int:student_id>', methods=['PUT'])
def update(student_id):
  student = Student.query.get(student_id)
  if student:
      for attr in request.json.keys():
        setattr(student, attr, request.json[attr])
        db.session.commit()
      return {'data': 'Student updated successfully.'}
  else:
      return {'error': 'Student not found.'}
