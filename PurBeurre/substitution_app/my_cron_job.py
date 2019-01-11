from django_cron import CronJobBase, Schedule
from .updateDB import Update_database

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 5 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'substitution_app.my_cron_job'

    def do(self):
        print("Start a task")
        update = Update_database()
        print("First ok")
        response = update.request_openfoofact_API()
        print("Seconde ok")
        nbrePage = update.pages_number_determination(response)
        print("Third ok")
        update_BD = update.request_updated_products(response, nbrePage)
        print("End of task")
