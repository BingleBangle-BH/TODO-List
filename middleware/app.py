from flask import Flask, request

app = Flask(__name__)

@app.route("/Modify")
def modify():
    if request.method == 'POST':
        return "Hello, World!"
    else: 
        return "Only POST request"

@app.route("/Delete")
def delete():
    if request.method == 'POST':
        return "Hello, World!"
    else: 
        return "Only POST request"