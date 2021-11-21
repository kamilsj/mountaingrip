from django_cron import CronJobBase, Schedule


class LearnYourself(CronJobBase):
    RUN_EVERY_MIN = 300  # 5hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MIN)
    code = 'start.LearnYourself'

    def do(self):
        pass