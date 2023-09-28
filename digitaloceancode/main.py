from flask import Flask, render_template, request, redirect, current_app
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from scrap import scrap_linkedin
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import pymysql
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = '' #os.urandom(24).hex()

user_admin = "romain"
password_admin = ""


jobstores = {
    'default': SQLAlchemyJobStore(url="mysql+pymysql://username:password@host:port/database_name", tablename="apscheduler_jobs"),
    'postgres': 'default': SQLAlchemyJobStore(url="postgres+psycopg2://username:password@host:port/database_name", tablename="apscheduler_jobs")
}

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3,
    'misfire_grace_time':1000
}


date_to_run = datetime.utcnow() + timedelta(minutes=61)


scheduler = BackgroundScheduler(timezone="Europe/Paris", jobstores=jobstores, executors=executors, job_defaults=job_defaults)
scheduler.start()

@app.route('/home', methods=['GET','POST'])
@app.route('/' , methods=['GET','POST'])
def home():
    if request.method == 'POST':
        user_sent = request.form['user']
        password_sent = request.form['password']

        if user_sent == user_admin and password_admin == password_sent:
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
    return """

<form action="/" method='POST'>
  <label for="user">user:</label><br>
  <input type="text" id="user" name="user"><br>

  <label for="password">password:</label><br>
  <input type="password" id="password" name="password"><br><br>

  <input type="submit" value="Submit">
</form>


    """






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
        #scrap_linkedin(position, localisation)

        with current_app.app_context():
        	scheduler.add_job(func=scrap_linkedin, trigger="date", run_date=date_to_run, args=[position, localisation], id="test")


        return ' <p> working: {}</p>'.format(position)
    else:
        return redirect('/login')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
