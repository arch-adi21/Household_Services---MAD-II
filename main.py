from flask import Flask
from flask_security import Security
from application.models import db
from config import DevelopmentConfig
from application.resources import api
from application.sec import datastore
import flask_excel as excel
from celery.schedules import crontab
from application.tasks import daily_reminder, monthly_reminder
from application.instances import cache
from application.worker import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    excel.init_excel(app)
    app.security = Security(app, datastore)
    celery.Task = ContextTask
    cache.init_app(app)
    with app.app_context():
        import application.views
    return app

app = create_app()
celery_app = create_app()

@celery.on_after_configure.connect
def send_email_daily(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=13, minute=34),
        daily_reminder.s('Daily Reminder')
    )
@celery.on_after_configure.connect
def send_email_monthly(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=13, minute=34, day_of_month=30),
        monthly_reminder.s('Monthly Activity Report')
    )

if __name__ == '__main__':
    app.run(debug=True)