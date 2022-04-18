from celery import Celery
from backend import app,dataclass
from backend.data.dataclass import GlobalStatistics
import logging
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

celery_app = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )


# def config_celery(celery_name, celery_backend, celery_broker):
#     celery_app.conf.update(
#         main=celery_name,
#         backend=celery_backend,
#         broker = celery_broker
#     )
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(app.config["RUN_CALCULATE_GLOBAL_STATISTICS_PERIOD"], run_calculate_global_statistics.s(), name='run_calculate_global_statistics')

@celery_app.task
def run_calculate_global_statistics():
    users = dataclass.User.objects.all()
    logger.info(f"Calculating global statistics with user group size: {len(users)}")
    new_statistic = dataclass.GlobalStatistics.calculate_global_statistics(users)
    global_stat_pobj: GlobalStatistics = dataclass.GlobalStatistics.objects.first()
    global_stat_pobj.statistics.append(new_statistic)
    global_stat_pobj.save()

celery_app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'tasks.run_calculate_global_statistics',
#         'schedule': app.config["RUN_CALCULATE_GLOBAL_STATISTICS_PERIOD"],
#         'args': ()
#     },
# }