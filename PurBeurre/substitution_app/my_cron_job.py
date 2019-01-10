from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'substitution_app.my_cron_job'

    def do(self):
        # do your thing here
        update = Update_database()
        response = update.request_openfoofact_API()
        nbrePage = update.pages_number_determination(response)
        test = update.request_updated_products(response, nbrePage)
