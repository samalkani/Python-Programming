from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta

scheduler = BlockingScheduler(timezone="Europe/Paris")

def function_to_trigger(argument1, argument2):
    print(argument1, argument2)

runningdate = datetime.utcnow() + timedelta(minutes=61)

#scheduler.add_job(func=function_to_trigger, trigger="interval", minutes=5)
#scheduler.add_job(func=function_to_trigger, trigger="date", run_date=runningdate)
scheduler.add_job(func=function_to_trigger, trigger="cron", second="*", args=["element1", 5])

scheduler.print_jobs()
scheduler.start()


### DOCUMENTATION : https://apscheduler.readthedocs.io/en/3.x/index.html
