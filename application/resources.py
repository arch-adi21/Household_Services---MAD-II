from flask_restful import Resource, Api, reqparse, marshal, fields
from flask_security import auth_required, roles_required, current_user
from .models import Service,Customer,User,Professional, ServiceRequest, db
from werkzeug.security import generate_password_hash
from application.sec import datastore
from datetime import datetime
from .instances import cache

api = Api(prefix='/api')

parser1 = reqparse.RequestParser()
parser1.add_argument('name', type=str, help='Name is required and should be a string', required=True)
parser1.add_argument('price', type=int, help='Price is required and should be an integer', required=True)
parser1.add_argument('time_required', type=str, help='Time Required is required and should be a string', required=True)
parser1.add_argument('description', type=str, help='Description is required and should be a string', required=True)

service_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "price": fields.Integer,
    "time_required": fields.String,
    "description": fields.String
}

#######################################################
#### Class to get all services and add new service ####
#######################################################

class Services(Resource):
    @auth_required("token")
    @cache.cached(timeout=50)
    def get(self):
        all_services = Service.query.all()
        if "professional" not in current_user.roles:
            return marshal(all_services, service_fields)
        # else:
        #     return {"message": "This funtion us not allowed for current user"}, 404
    
    @auth_required("token")
    @roles_required("admin")
    def post(self):
        args = parser1.parse_args()
        service = Service(**args)
        db.session.add(service)
        db.session.commit()
        return {"message": "Service Created"}
    
#######################################################
####      Class to update a service details        ####
#######################################################
    
class UpdateService(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self,id):
        service = Service.query.get(id)
        return marshal(service, service_fields)
    
    def post(self,id):
        service = Service.query.get(id)
        args = parser1.parse_args()
        service.name = args.name
        service.price = args.price
        service.time_required = args.time_required
        service.description = args.description
        db.session.commit()
        return {"message": "Service Updated"}

    
parser2 = reqparse.RequestParser()
parser2.add_argument('email', type=str, help='Email is required and should be a string', required=True)
parser2.add_argument('password', type=str, help='Password is required and should be a string', required=True)
parser2.add_argument('full_name', type=str, help='Full Name is required and should be a string', required=True)
parser2.add_argument('address', type=str, help='Address is required and should be a string', required=True)
parser2.add_argument('pincode', type=int, help='Pincode is required and should be an integer', required=True)
customer_fields = {
    "id": fields.Integer,
    "full_name": fields.String,
    "address": fields.String,
    "pincode": fields.Integer,
    "user_id": fields.Integer
}

#########################################################
#### Class to get all customers and add new customer ####
#########################################################
class Customers(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self):
        customers = Customer.query.all()
        if len(customers) == 0:
            return {"message": "No User Found"}, 404
        return marshal(customers, customer_fields)
    def post(self):
        args = parser2.parse_args()
        datastore.create_user(email=args.email, password=generate_password_hash(args.password), roles=['customer'])
        customer = Customer(full_name=args.full_name, address=args.address, pincode=args.pincode, user_id = User.query.filter_by(email=args.email).all()[0].id)
        db.session.add(customer)
        db.session.commit()
        return {"message": "Customer Added"}
    
parser3 = reqparse.RequestParser()
parser3.add_argument('email', type=str, help='Email is required and should be a string', required=True)
parser3.add_argument('password', type=str, help='Password is required and should be a string', required=True)
parser3.add_argument('full_name', type=str, help='Full Name is required and should be a string', required=True)
parser3.add_argument('service', type=str, help='Service is required and should be a string', required=True)
parser3.add_argument('experience', type=str, help='Experience is required and should be a string', required=True)
parser3.add_argument('address', type=str, help='Address is required and should be a string', required=True)
parser3.add_argument('pincode', type=int, help='Pincode is required and should be an integer', required=True)

professional_fields = {
    "id": fields.Integer,
    "full_name": fields.String,
    "experience": fields.String,
    "service": fields.String,
    "active": fields.Boolean
}

#################################################################
#### Class to get all professionals and add new professional ####
#################################################################
class Professionals(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self):
        professionals = Professional.query.all()
        if len(professionals) == 0:
            return {"message": "No User Found"}, 404
        return marshal(professionals, professional_fields)
    
    def post(self):
        args = parser3.parse_args()
        datastore.create_user(email=args.email, password=generate_password_hash(args.password), roles=['professional'], active=False)
        professional = Professional(full_name=args.full_name, service=args.service, experience=args.experience, address=args.address, pincode=args.pincode, user_id = User.query.filter_by(email=args.email).all()[0].id, active=False)
        db.session.add(professional)
        db.session.commit()
        return {"message": "Professional Added"}

parser4 = reqparse.RequestParser()
parser4.add_argument('service_id', type=int, help='Service ID should be an integer')
parser4.add_argument('customer_id', type=int, help='Customer ID should be an integer')
parser4.add_argument('professional_id', type=int, help='Professional ID should be an integer')
parser4.add_argument('date_of_completion', type=str, help='Date of Completion should be a string')
parser4.add_argument('service_status', type=str, help='Service Status is should be a string')
service_request_fields = {
    "id": fields.Integer,
    "service_id": fields.Integer,
    "customer_id": fields.Integer,
    "professional_id": fields.Integer,
    "date_of_request": fields.String,
    "date_of_completion": fields.String,
    "rating": fields.Integer,
    "remarks": fields.String,
    "service_status": fields.String
}

###############################################################
#### Class to get all service requests and add new request ####
###############################################################
class ServiceRequests(Resource):
    def get(self):
        service_requests = ServiceRequest.query.all()
        if len(service_requests) == 0:
            return {"message": "No User Found"}, 404
        all_services = Service.query.all()
        return {
            'service_requests': marshal(service_requests,service_request_fields),
            'services': marshal(all_services, service_fields)
        }
    
    def post(self):
        args = parser4.parse_args()
        service_request = ServiceRequest(service_id=args.service_id, customer_id=Customer.query.filter_by(user_id=args.customer_id).all()[0].id, date_of_request=datetime.now().strftime("%d/%m/%y"), service_status='requested')
        db.session.add(service_request)
        db.session.commit()
        return {"message": "Service Request Added"}
    

##############################################################
## Class to Accept Service Requests and reject the requests ##
##############################################################    
class AcceptServiceRequest(Resource):
    def get(self,id):
        service_request = ServiceRequest.query.get(id)
        service_request.professional_id = None
        service_request.service_status = 'requested'
        db.session.commit()
        return {"message": "Service Request Rejected"}
    
    def post(self,id):
        service_request = ServiceRequest.query.get(id)
        args = parser4.parse_args()
        service_request.professional_id = args.professional_id
        service_request.service_status = 'assigned'
        db.session.commit()
        return {"message": "Service Request Accepted"}
    
parser5 = reqparse.RequestParser()
parser5.add_argument('user_id', type=int, help='User_id is required and should be an integer', required=True)

##############################################################
##      Class to get Service Requests by Customer ID        ##
##############################################################
class ServiceRequestByCustomer(Resource):
    def post(self):
        args = parser5.parse_args()
        customer = Customer.query.filter_by(user_id=args.user_id).all()[0]
        service_requests = ServiceRequest.query.filter_by(customer_id=customer.id).all()
        all_services = Service.query.all()
        return {
            'service_requests': marshal(service_requests,service_request_fields),
            'services': marshal(all_services, service_fields)
        }

parser6 = reqparse.RequestParser()
parser6.add_argument('rating', type=int, help='Rating is required and should be an integer', required=True)
parser6.add_argument('remarks', type=str, help='Remarks should be a string')

##############################################################
##              Class to close Service Requests             ##
##############################################################
class CloseServiceRequest(Resource):
    def post(self,id):
        args = parser6.parse_args()
        service_request = ServiceRequest.query.get(id)
        service_request.rating = args.rating
        service_request.remarks = args.remarks
        service_request.date_of_completion = datetime.now().strftime("%d/%m/%y")
        service_request.service_status = 'closed'
        db.session.commit()
        return {"message": "Service Request Closed"}

api.add_resource(Services, '/services')
api.add_resource(Customers, '/customers')
api.add_resource(Professionals, '/professionals')
api.add_resource(UpdateService, '/update/service/<int:id>')
api.add_resource(ServiceRequests, '/request/service')
api.add_resource(AcceptServiceRequest, '/accept/service-request/<int:id>')
api.add_resource(ServiceRequestByCustomer, '/service-request/customer')
api.add_resource(CloseServiceRequest, '/close/service-request/<int:id>')