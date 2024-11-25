from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()



################################################################
####             Class to store User Roles                 #####
################################################################

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))




################################################################
####             Class to store User Details               #####
################################################################

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))




################################################################
####             Class to store Customer Details           #####
################################################################

class Customer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    pincode = db.Column(db.Integer())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))




################################################################
####             Class to store Professional Details       #####
################################################################

class Professional(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.String(255))
    service = db.Column(db.String(255))
    experience = db.Column(db.String(255))
    address = db.Column(db.String(255))
    pincode = db.Column(db.Integer())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    active = db.Column(db.Boolean())




################################################################
####             Class to store Role Details               #####
################################################################

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))




################################################################
####             Class to store Service Details            #####
################################################################

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    time_required = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

    # Method to convert the object to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description
        }
    


    
    
################################################################
####         Class to store Service Request Details        #####
################################################################

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'))
    date_of_request = db.Column(db.String())
    date_of_completion = db.Column(db.String())
    rating = db.Column(db.Integer())
    remarks = db.Column(db.String())
    service_status = db.Column(db.String())
