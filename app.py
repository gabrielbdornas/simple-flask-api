from flask import Flask
from data import students

app = Flask(__name__)

@app.route('/students', methods=['GET'])
def get():
    return students
