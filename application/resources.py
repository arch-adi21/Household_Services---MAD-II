from flask_restful import Resource, Api, reqparse 
from flask import jsonify
from application.model import db, Services, User
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity,jwt_required
from functools import wraps

api = Api(prefix='/api')


####################################################################
#### Method for JWT management for RBAC authentication #####
####################################################################

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_identity = get_jwt_identity()
        if user_identity['role'] != 'admin':
            return jsonify({"message": "Access denied: Admins only"}), 403
        return fn(*args, **kwargs)
    return wrapper


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

####################################################################
#### Resource class to update users only with admin credentials ####
####################################################################

class UsersResource(Resource):
    @admin_required
    def get(self):
        users = User.query.all()
        users_data = [{'id': user.id, 'username': user.username, 'email': user.email, 'role_id': user.role_id} for user in users]
        return users_data, 200
