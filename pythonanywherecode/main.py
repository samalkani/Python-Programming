from flask import Flask, render_template, request, redirect
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from scrap import scrap_linkedin
import psycopg2
from flask_bcrypt import Bcrypt
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import pandas as pd

username = ""
password = ""

app = Flask(__name__)
app.config['SECRET_KEY'] = ''  #os.urandom(24).hex()
bcrypt = Bcrypt(app)

user_admin = "romain"
password_admin = bcrypt.generate_password_hash("password")


@app.route('/home', methods=['GET','POST'])
@app.route('/' , methods=['GET','POST'])
def home():
    if request.method == 'POST':
        user_sent = request.form['user']
        password_sent = request.form['password']

        if user_sent == user_admin and bcrypt.check_password_hash(password_admin , password_sent):
            return """

            <form action="/results" method='POST'>
              <label for="position">Position of the person:</label><br>
              <input type="text" id="position" name="position"><br>

              <label for="localisation">Localisation:</label><br>
              <input type="text" id="localisation" name="localisation"><br><br>

              <input type="submit" value="Submit">
            </form>


                """
        else:
            return redirect('/login')
    else:
        return redirect('/login')






@app.route('/login')
def login():
    return """

<form action="/" method='POST'>
  <label for="user">user:</label><br>
  <input type="text" id="user" name="user"><br>

  <label for="password">password:</label><br>
  <input type="password" id="password" name="password"><br><br>

  <input type="submit" value="Submit">
</form>


    """


@app.route('/results', methods=['GET','POST'])
def results():
    ######
    if request.method == 'POST':
        position = request.form['position']
        localisation = request.form['localisation']


        scrap_linkedin(position, localisation)



        return ' <p> working: {}</p>'.format(position)
    else:
        return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)
