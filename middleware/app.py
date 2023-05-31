from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/Modify", methods=['POST'])
def modify():
    data = request.get_json()
    if request.method == 'POST':
        
        return f'{data["new_task"], data["old_task"]}'
    else: 
        return "Only POST request"

@app.route("/Delete")
def delete():
    if request.method == 'POST':
        return "Hello, World!"
    else: 
        return "Only POST request"