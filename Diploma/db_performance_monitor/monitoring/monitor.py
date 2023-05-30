import schedule
import time
from django.core.management import call_command


def job():
    call_command('collect_all_database_metrics')


schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(300)
