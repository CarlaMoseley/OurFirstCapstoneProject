import MySQLdb
from flask import Flask, render_template
from flask_mysqldb import MySQL

app= Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='contacts'

mySql = MySQL(app)

@app.route('/')
def hello_world():
    cur = mySql.connection.cursor()
    cur.execute("SELECT * FROM my_contacts")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template('Main.html', title='Flask example', message='Hello Carla', data=fetchdata)
if __name__=='__main__':
    app.run(host="0.0.0.0", port=80)
    