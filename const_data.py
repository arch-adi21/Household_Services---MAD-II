from main import app
from sqlalchemy.exc import SQLAlchemyError
from application.model import db , Role , User
from application.logger.logger import logger
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    password_hashsed = generate_password_hash(os.getenv('ADMIN_PASSWORD'))
    # Inserting default roles
    db.session.add(Role(name='Admin', description='Admin Role'))
    db.session.add(Role(name='Customer', description='Customer Role'))
    db.session.add(Role(name='Service Provider', description='Service Provider Role'))
    db.session.add(User( username='mad2admin', password=password_hashsed, email='admin@mad2.com', fs_uniquefier='admin', registration_date=datetime.today(), role_id=1))
    try:
        db.session.commit()
        logger.info('Default Database initialized successfully')
    except SQLAlchemyError as Exception:
        exception = Exception
        db.session.rollback()
        logger.debug(f'Default Database initialization rolled back due to :- {exception}')
        pass