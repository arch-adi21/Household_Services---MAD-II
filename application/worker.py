from celery import Celery, Task
from flask import current_app as app

celery = Celery("Jobs", broker='redis://localhost:6379/1', backend='redis://localhost:6379/2' , imports=["application.tasks"])
celery.conf.timezone = 'Asia/Kolkata'


class ContextTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super().__call__(self, *args, **kwargs)