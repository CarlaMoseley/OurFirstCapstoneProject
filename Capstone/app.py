import pandas as pd
from flask import Flask, jsonify, render_template, redirect, url_for, request, session, flash
from src.connect import get_snowflake_connection
from datetime import timedelta
# from connect import get_snowflake_connection


app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = 'ShusshItsaSecret'
app.permanent_session_lifetime = timedelta(seconds=10)

def check_credentials(username, password):
    connection = get_snowflake_connection()

    try:
        cursor = connection.cursor()

        query = f"SELECT COUNT(*) FROM LANDLORD WHERE USERNAME = '{username}' AND PASSWORD = '{password}';"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result
    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        cursor.close()
        connection.close()


def insert_data_to_snowflake(data):
    try:
        print(data)
        connection = get_snowflake_connection()
        cursor = connection.cursor()

        # Your insert query here
        query = "INSERT INTO LANDLORD (FIRST_NAME, LAST_NAME, EMAIL, PHONE_NUMBER, USERNAME, PASSWORD) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, data)

        connection.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        if connection:
            connection.close()


def insert_data():
    print("wow")
    # Extract data from the request or any other source
    data_to_insert = (
        "Manan",
        "Patel",
        "manan.patel@fiserv.com",
        "9238762343",
        "Manan05",
        "Welcome123!"
    )
    insert_data_to_snowflake(data_to_insert)

    return "Data inserted successfully"


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
        session.permanent = True
        session['username'] = username
        flash('Login Successful!', 'success')
        return redirect(url_for('render_index'))
    else:
        flash('Invalid credentials. Please try again.', 'error')
        return render_template("login.html")


@app.route('/render_index')
def render_index():
    if 'username' in session:
        return render_template("index.html")
    else:
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/login')
def login():
    # Check for redirects in the login route
    return redirect(url_for('home'))


app.run(debug=True)

