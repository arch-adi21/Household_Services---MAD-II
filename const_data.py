from main import app
from application.model import db , Role , User
with app.app_context():
    db.create_all()
    # Inserting default roles
    db.session.add(Role(name='Admin', description='Admin Role'))
    db.session.add(Role(name='Customer', description='Customer Role'))
    db.session.add(Role(name='Service Provider', description='Service Provider Role'))
    db.session.add(User( username='admin', password='admin', email='admin@mad2.com', fs_uniquefier='admin', role_id=1))
    try:
        db.session.commit()
    except:
        db.session.rollback()
        pass