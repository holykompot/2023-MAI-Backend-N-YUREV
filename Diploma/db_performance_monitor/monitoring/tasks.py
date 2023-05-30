from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .collect_metrics import collect_all_database_metrics

@shared_task
def collect_metrics_task():
    collect_all_database_metrics()