import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder="templates", static_folder="static")

def check_credentials(username, password):
    with open('first-flask-app\login.txt', 'r') as file:
        for line in file:
            usernameFromFile, passwordFromFile = line.strip().split(',')
            if username == usernameFromFile and password == passwordFromFile:
                return True
    return False

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/file", methods=['GET'])
def upload():
    try:
        filePath = 'first-flask-app\\todo_tasks_data.xlsx'
        df = pd.read_excel(filePath)
        rawData = df.values.tolist()
   
        list = []
   
        for data in rawData:
            splitTask = data[0].split(", ")
   
            task_map = {
                "Task Name": splitTask[0],
                "Date Created": splitTask[1],
                "Date Completed": splitTask[2],
                "Completion Status": splitTask[3],
                "Priority": splitTask[4],
                "Time to Complete": splitTask[5]
            }
   
            list.append(task_map)
        return jsonify(list)

    except Exception as e:
        error_message = f"Error: {str(e)}"
        return render_template('index.html', error=error_message)
    
@app.route('/index', methods=['POST'])
def index():
    username = request.form['username']
    password = request.form['password']
    
    if check_credentials(username, password):
        return render_template("index.html")
    else:
        return render_template("login.html")

app.run(debug=True)