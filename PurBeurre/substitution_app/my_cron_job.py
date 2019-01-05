from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'substitution_app.my_cron_job'

    def do(self):
        # do your thing here
        print('Hello you !')
        """
        f= open("guru99.txt","w+")
        for i in range(10):
            f.write("This is line %d\r\n" % (i+1))
        f.close()
        """