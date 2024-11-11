from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date
from datetime import date

db = SQLAlchemy()

#### Table for storing user information ####
class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True , primary_key=True)
    username = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    active = db.Column(db.Boolean, default=True)
    premium = db.Column(db.Boolean, default=False)
    registration_date = db.Column(Date, default=date.today, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    fs_uniquefier = db.Column(db.String(256), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

#### Table for storing role assigned to users ####
class Role(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)

#### Table for storing services information ####
class Services(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    price = db.Column(db.Float, nullable=False)
    premium_only = db.Column(db.Boolean, default=False)
    flagged = db.Column(db.Boolean, default=False)
    serviced_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ratings = db.relationship('Rating', backref='service', lazy=True)

#### Table for storing ratings and comments on services ####
class Rating(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    # Ensuring a user can only rate a service once
    __table_args__ = (db.UniqueConstraint('service_id', 'user_id', name='unique_service_user_rating'),)

    user = db.relationship('User', backref=db.backref('ratings', lazy=True))

    # Optional: to calculate average ratings directly if needed
    @staticmethod
    def calculate_avg_rating(service_id):
        total_rating = db.session.query(db.func.sum(Rating.rating)).filter_by(service_id=service_id).scalar()
        count = db.session.query(db.func.count(Rating.rating)).filter_by(service_id=service_id).scalar()
        return total_rating / count if count else 0