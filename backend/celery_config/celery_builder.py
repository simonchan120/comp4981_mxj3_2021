from typing import List
from celery import Celery
from backend import app,dataclass
from backend.data.dataclass import GlobalStatistics
import logging
from celery.utils.log import get_task_logger
from datetime import datetime
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
    sender.add_periodic_task(app.config["SAVE_COPY_USERS_EMOTION_PROFILE_PERIOD"], save_copy_users_emotion_profile.s(), name='save_copy_users_emotion_profile')

@celery_app.task
def run_calculate_global_statistics():
    users = dataclass.User.objects.all()
    
    datetimenow = datetime.utcnow()
    target_threshold = app.config["RUN_CALCULATE_GLOBAL_STATISTICS_PERIOD"] *12
    users = filter(lambda user: (datetimenow - user.latest_conversation[0].time_sent).total_seconds() <= target_threshold, users)
    new_statistic = dataclass.GlobalStatistics.calculate_global_statistics(users)
    global_stat_pobj: GlobalStatistics = dataclass.GlobalStatistics.objects.first()
    global_stat_pobj.statistics.append(new_statistic)
    global_stat_pobj.save()
    logger.info(f"Calculatd global statistics with user group size: {len(users)}")

@celery_app.task
def save_copy_users_emotion_profile():
    users: List[dataclass.User] = dataclass.User.objects.all()
    counter = 0
    for user in users:
        if not user.previous_emotion_profile_lists:
            user.add_new_emotion_profile_list()
        if user.check_if_should_be_saved():
            user.previous_emotion_profile_lists[0].profile_list.append(user.get_emotion_profile_copy())
            user.save()
            counter += 1
    logger.info(f"Copying Emotion Profile, num of saved users: {counter}, num of total users: {len(users)}")

celery_app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'tasks.run_calculate_global_statistics',
#         'schedule': app.config["RUN_CALCULATE_GLOBAL_STATISTICS_PERIOD"],
#         'args': ()
#     },
# }