from flask import Flask
from application.model import db
from config import DevelopmentConfig
from application.resources import api
from application.jwt_manager import jwt

def create_app(app_name=__name__):
    app = Flask(app_name)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    with app.app_context():
        from application import views
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)