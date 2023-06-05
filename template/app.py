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
        print(data["alias"])
        app.modify_task(data["alias"], data["new_task"], data["old_task"])
        app.update_account(data["alias"])
        return redirect('http://127.0.0.1:5500/docs/index.html')
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

@app.route("/Delete", methods=['GET'])
def delete():
    app = logic()
    alias = request.args.get('alias')
    if alias != 'chooseaccount':
        task = request.args.get('task')
        app.remove_task(alias, task)
        app.update_account(alias)
        return redirect('http://127.0.0.1:5500/docs/index.html')
    else: 
        return "Choose an account"
    
if __name__ == '__main__':
    app.run(port=5500)