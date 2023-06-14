from flask import Flask, request, render_template, send_file, redirect
from flask_cors import CORS

from main import logic
import os

app = Flask(__name__, template_folder='src')
CORS(app)

@app.route("/Modify", methods=['POST'])
def modify():
    data = request.get_json()

    if request.method == 'POST':        
        app = logic()
        print(data["alias"])
        app.modify_task(data["alias"], data["new_task"], data["old_task"])
        app.update_account(data["alias"])
        return "Okays"
    else: 
        return "Only POST request"
    
@app.route("/CreateAccount", methods=['POST'])
def createaccount():
    data = request.get_json()
    print(data["alias"])
    return "Not implemented yet"

@app.route("/Account", methods=['GET'])
def account():
    app = logic()
    alias = request.args.get('alias')
    app.update_account(alias)
    if request.method == 'GET':
        # return f"Current path: {current_path}"
        return "Okays"
    else: 
        return "Only GET request"    

@app.route("/Delete", methods=['GET'])
def delete():
    app = logic()
    alias = request.args.get('alias')
    if alias != 'chooseaccount':
        task = request.args.get('task')
        app.remove_task(alias, task)
        app.update_account(alias)
        return "Okays"
    else: 
        return "Choose a correct account!"
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)