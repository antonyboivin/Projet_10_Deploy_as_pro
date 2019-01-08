from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 5 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'substitution_app.my_cron_job'
"""
    # Test code
    def do(self):
        f= open("testCron.txt","a+")
        f.write("Un truc")
        f.close()
"""