from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import pymysql
#from scheduler import scheduler
from flaskapp.config import Config


user_admin = "romain"
password_admin = ""


jobstores = {
    'default': SQLAlchemyJobStore(url="mysql+pymysql://username:password@host:port/database", tablename="apscheduler_jobs")
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




scheduler = BackgroundScheduler(timezone="Europe/Paris", jobstores=jobstores, executors=executors, job_defaults=job_defaults)
scheduler.start()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from flaskapp.bot.routes import blueprint1
    app.register_blueprint(blueprint1)
    return app
