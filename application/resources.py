from flask_restful import Resource, Api, reqparse 
from flask import jsonify , request , make_response
from application.model import db, Services, User, Role
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash , check_password_hash
from flask_jwt_extended import get_jwt_identity,jwt_required , create_access_token
from application.logger.logger import logger
from functools import wraps
from application.rbac import role_required
import uuid
from datetime import datetime , timedelta

api = Api(prefix='/api')


####################################################################
#### Method for JWT management for RBAC authentication #####
####################################################################

class RBACTester(Resource):
    @role_required('Customer')
    def get(self):
        return {'message': 'Access granted! This is a protected endpoint for customers only.'}, 200
    
    @role_required('Service Provider')
    def post(self):
        return {'message': 'Access granted! This is a protected endpoint for service providers only.'}, 200
    
api.add_resource(RBACTester, '/rbac-tester')





####################################################################
####            Resource class to register the user            #####
####################################################################

class RegisterController(Resource):
    def post(self):
        try :
            # Define required arguments
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, required=True, help="Username cannot be blank!")
            parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
            parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")
            parser.add_argument('role_id', type=int, required=True, help="Role ID cannot be blank!")
            args = parser.parse_args()

            # Validate input data
            if not args['username'] or not args['email'] or not args['password'] or not args['role_id']:
                return make_response(jsonify({'message': 'All fields are required'}), 400)

            # Check if the role exists in the database
            role = Role.query.filter_by(id=args['role_id']).first()
            if not role:
                return make_response(jsonify({'message': 'Invalid role'}), 400)

            # Check if the email already exists
            if User.query.filter_by(email=args['email']).first():
                return make_response(jsonify({'message': 'Email is already in use'}), 400)

            # Generate fs_uniquefier using UUID
            fs_uniquefier = str(uuid.uuid4())

            # Hash the password before storing it
            hashed_password = generate_password_hash(args['password'])

            # Create the new user instance
            new_user = User(
                username=args['username'],
                email=args['email'],
                password=hashed_password,
                role_id=args['role_id'],
                fs_uniquefier=fs_uniquefier,
                registration_date=datetime.today() # Set the registration date to the current time
            )

            # Add user to the database
            db.session.add(new_user)
            db.session.commit()

            # Return the created user as a response (Serialized into dictionary)
            user_data = {
                    'id': new_user.id,
                    'username': new_user.username,
                    'role': new_user.role.name,
                    'registration_date': new_user.registration_date.isoformat()  # Format the date properly
                }
            
            logger.debug(f'User created: {user_data}')  # Log the serializable dict instead of the model instance

            return make_response(jsonify({'message': 'User created successfully', 'user': user_data}), 201)

        except Exception as e:
            logger.error(f'Error creating user: {str(e)}')
            db.session.rollback()
            return make_response(jsonify({'message': 'An error occurred while creating the user'}), 500)
    
api.add_resource(RegisterController, '/register')





####################################################################
####     Resource class to login with JWT token management     #####
####################################################################

class LoginController(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, required=False, help="Provide email or username")
            parser.add_argument('username', type=str, required=False, help="Provide username or email")
            parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")
            args = parser.parse_args()

            # Ensure either email or username is provided
            if not args['email'] and not args['username']:
                return make_response(jsonify({'message': 'Either email or username must be provided'}), 400)

            # Validate the input
            if not args['password']:
                return make_response(jsonify({'message': 'Password is required'}), 400)

            # Look up the user by email or username
            user = None
            if args['email']:
                user = User.query.filter_by(email=args['email']).first()
            elif args['username']:
                user = User.query.filter_by(username=args['username']).first()

            if not user or not check_password_hash(user.password, args['password']):
                return make_response(jsonify({'message': 'Invalid email or password'}), 401)

            # Create access token with user role
            if user.role != 'admin' :
                access_token = create_access_token(identity=user.id,expires_delta=timedelta(hours=1) ,additional_claims={'username':user.username ,'role': user.role.name})
            elif user.role == 'admin':
                access_token = create_access_token(identity=user.id,expires_delta=timedelta(minutes=30) ,additional_claims={'username':user.username ,'role': user.role.name})
            else :
                return make_response(jsonify({'message': 'Invalid role to create a JWT token'}), 400)

            # Update last login date
            user.last_login = datetime.now()
            db.session.commit()

            return make_response(jsonify({'message': 'Login successful', 'token': access_token}), 200)
        
        except Exception as e:
            logger.error(f'Error logging in: {str(e)}')
            return make_response(jsonify({'message': 'An error occurred while logging in'}), 500)

api.add_resource(LoginController, '/login')





####################################################################
#### Resource class to create , show , delete and edit Services ####
####################################################################

class ServicesController(Resource):
    def get(self):
        # Fetch all services from the database
        services = Services.query.all()
        # Serialize the data
        services_data = [
            {
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': service.price,
                'premium_only': service.premium_only,
                'flagged': service.flagged,
                'serviced_by_id': service.serviced_by_id
            }
            for service in services
        ]
        return jsonify(services_data)

    def post(self):
        # Define required arguments for POST request
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
        parser.add_argument('description', type=str)
        parser.add_argument('price', type=float, required=True, help="Price cannot be blank!")
        parser.add_argument('premium_only', type=bool, default=False)
        parser.add_argument('flagged', type=bool, default=False)
        parser.add_argument('serviced_by_id', type=int, required=True, help="Serviced_by_id cannot be blank!")
        args = parser.parse_args()

        # Create new service record
        new_service = Services(
            name=args['name'],
            description=args.get('description'),
            price=args['price'],
            premium_only=args['premium_only'],
            flagged=args['flagged'],
            serviced_by_id=args['serviced_by_id']
        )

        # Add and commit to the database
        db.session.add(new_service)
        db.session.commit()

        return {'message': 'Service added successfully', 'service_id': new_service.id}, 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="ID of the service to delete cannot be blank!")
        args = parser.parse_args()

        # Query the service by ID
        service = Services.query.get(args['id'])
        if not service:
            return {'message': 'Data not found in db'}, 404
        
        try:
            db.session.delete(service)
            db.session.commit()
            return {'message': f'Service with id {args["id"]} deleted successfully'}, 200
        except IntegrityError:
            db.session.rollback()
            return {'message': 'An error occurred while trying to delete the service'}, 500
        
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="ID of the service to edit cannot be blank!")
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('description', type=str, required=False)
        parser.add_argument('price', type=float, required=False)
        parser.add_argument('premium_only', type=bool, required=False)
        parser.add_argument('flagged', type=bool, required=False)
        parser.add_argument('serviced_by_id', type=int, required=False)
        args = parser.parse_args()

        # Check if at least one field other than 'id' is provided for updating
        if all(value is None for key, value in args.items() if key != 'id'):
            return {'message': 'No fields provided to update'}, 400

        # Attempt to query the service by ID
        try:
            service = Services.query.get(args['id'])
            if not service:
                return {'message': 'Data not found in db'}, 404
        except ValueError:
            return {'message': 'Invalid service ID'}, 400

        # Update fields if new values are provided
        try:
            if args['name'] is not None:
                service.name = args['name']
            if args['description'] is not None:
                service.description = args['description']
            if args['price'] is not None:
                if args['price'] < 0:
                    return {'message': 'Price must be a positive number'}, 400
                service.price = args['price']
            if args['premium_only'] is not None:
                service.premium_only = args['premium_only']
            if args['flagged'] is not None:
                service.flagged = args['flagged']
            if args['serviced_by_id'] is not None:
                if args['serviced_by_id'] <= 0:
                    return {'message': 'Serviced_by_id must be a positive integer'}, 400
                service.serviced_by_id = args['serviced_by_id']

            # Commit changes to the database
            db.session.commit()
            return {'message': f'Service with id {args["id"]} updated successfully'}, 200

        except IntegrityError:
            db.session.rollback()
            return {'message': 'An error occurred while trying to update the service, possibly due to a database constraint'}, 500
        except Exception as e:
            return {'message': f'An unexpected error occurred: {str(e)}'}, 500

api.add_resource(ServicesController, '/services')


