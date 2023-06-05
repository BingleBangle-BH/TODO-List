from flask import Flask, request, render_template, send_file, redirect
from flask_cors import CORS

from main import logic


app = Flask(__name__)
CORS(app)

@app.route("/Modify", methods=['POST'])
def modify():
    data = request.get_json()
    if request.method == 'POST':        
        app = logic()
        app.modify_task(data["new_task"], data["old_task"])
        return f'{data["new_task"], data["old_task"]}'
    else: 
        return "Only POST request"
    
@app.route("/Account", methods=['GET'])
def account():
    app = logic()
    alias = request.args.get('alias')
    app.update_account(alias)
    if request.method == 'GET':
        # return f"Current path: {current_path}"
        return redirect('http://127.0.0.1:5500/docs/index.html')
    else: 
        return "Only GET request"    

@app.route("/Delete", methods=['POST'])
def delete():
    if request.method == 'POST':
        return "Hello, World!"
    else: 
        return "Only POST request"
    
if __name__ == '__main__':
    app.run(port=5500)