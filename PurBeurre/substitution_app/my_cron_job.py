from django_cron import CronJobBase, Schedule
from .updateDB import Update_database

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 5 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'substitution_app.my_cron_job'

    def do(self):
        # do your thing here
        pass
