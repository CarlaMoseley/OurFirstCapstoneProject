import pandas as pd
from flask import Flask, json, jsonify, render_template, redirect, url_for, request, session, flash

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = 'ShusshItsaSecret'
@app.route('/')
def start():
    return render_template('start.html')

@app.route('/login/<button_clicked>')
def login(button_clicked):
    print(button_clicked)
    return render_template("LoginPage.html", b=button_clicked )

 
 
@app.route("/start", methods=['POST', 'GET'])
def handle_button():
    if request.method == 'POST':
        data = request.json
        button_clicked = data.get('button')
        # Add any additional logic here if needed
    return redirect(url_for('login', button_clicked=button_clicked))

@app.route('/landlord_signup')
def landlord_signup():
    return render_template('LandlordSignUp.html')
@app.route('/tenant_signup')
def tenant_signup():
    return render_template('TenantSignUp.html')
@app.route('/login_handler', methods=['POST'])
def login_handler():
    username = request.form['username']
    password = request.form['password']
    print(username)
    print(password)
    return username
 
@app.route('/tenant_handler', methods=['POST'])
def tenant_handler():
    name = request.form['name']
    phonenumber = request.form['phonenumber']
    email = request.form['email']
    id = request.form['id']
    username = request.form['username']
    if username.strip() == "":
        username = email
    password = request.form['password'] 
    if password == request.form['confirmpassword'] and password.strip() != "":
        print(f'{name} , {phonenumber}, {email}, {id}, {username}, {password}')
        return password
    else:
        flash("Passwords Don't Match", 'error')
        return redirect(url_for('login', button_clicked = 'tenant'))   

@app.route('/landlord_handler', methods=['POST'])
def landlord_handler():
    name = request.form['name']
    phonenumber = request.form['phonenumber']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    if username.strip() == "":
        username = email
    if password == request.form['confirmpassword']:
        print(f'{name} , {phonenumber}, {email}, {username}, {password}')
        return password
    else:
        flash("Passwords Don't Match", 'error')
        return redirect(url_for('login', button_clicked = 'landlord'))   
app.run(debug=True)