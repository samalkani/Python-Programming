from datetime import datetime, timedelta
from scrap import scrap_linkedin
from flask import Flask, request, render_template, Blueprint, current_app
from flaskapp.__init__ import scheduler
blueprint1 = Blueprint('main', __name__)

date_to_run = datetime.utcnow() + timedelta(minutes=61)

@blueprint1.route('/home', methods=['GET','POST'])
@blueprint1.route('/' , methods=['GET','POST'])
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






@blueprint1.route('/login')
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


@blueprint1.route('/results', methods=['GET','POST'])
def results():
    ######
    if request.method == 'POST':
        position = request.form['position']
        localisation = request.form['localisation']
        #scrap_linkedin(position, localisation)
        #return 'before adding job'
        with current_app.app_context():
             scheduler.add_job(func=scrap_linkedin, trigger="date", run_date=date_to_run, args=[position, localisation])
        return 'after adding job'
        #scheduler.print_jobs()

        #return ' <p> working: {}</p>'.format(position)
    else:
        return redirect('/login')
