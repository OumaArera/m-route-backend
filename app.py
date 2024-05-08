from flask import Flask, request, make_response, jsonify
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from models import db
from datetime import datetime, timezone, timedelta
from flask_cors import CORS
from dotenv import load_dotenv
import os

from models import User,  RoutePlan, Location, Outlet, Notification, ActivityLog

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")


db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

bcrypt = Bcrypt(app)

api = Api(app)
CORS(app)

@app.route('/')
def index():
    return '<h1>Merchandiser Route App</h1>'

def log_activity(action, user_id):
    try:
        new_activity = ActivityLog(
            user_id=user_id,
            action=action
        )
        db.session.add(new_activity)
        db.session.commit()

    except Exception as err:
        db.session.rollback()
        print(f"Failed to log activity. Error: {err}")


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    #Confirm if there's data
    if not data:
        return jsonify({"error":"Invalid request"}), 400

    #Extract required fields
    first_name = data.get('first_name')
    middle_name = data.get('middle_name')
    last_name = data.get('last_name')
    national_id_no = data.get('national_id_no')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check for required fields
    if not all([first_name, last_name, national_id_no, username, email, password]):
        return jsonify({'message': 'Missing required fields'}), 400

    #Check if username or email already exist
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'message': 'Username or email already exists'}), 409
    
    #Hash the password before saving it
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    #Create new user object
    new_user = User(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        national_id_no=national_id_no,
        username=username,
        email=email,
        password=hashed_password,
        role='merchandiser',  # merchandiser or manager or admin
    ) 

    try:
        db.session.add(new_user)
        db.session.commit()
        log_activity('User signed up', new_user.id)
        return jsonify({'message': 'User created successfully'}), 201
    
    except Exception as err:
        db.session.rollback()
        return({"error": f"failed to create user. Error: {err}"}), 400
    
    
@app.route('/users', methods=['GET'])
# @jwt_required()
def users():
    users = User.query.all()

    if not users:
        return jsonify({"message":"No users found"}), 404
    
    user_list = []
    for user in users:
        user_info = {
            'id': user.id,
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            'national_id_no': user.national_id_no,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'status': user.status,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Convert to string
            'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S'),  # Convert to string
            'last_password_change': user.last_password_change.strftime('%Y-%m-%d %H:%M:%S'),  # Convert to string
        }
        user_list.append(user_info)

    # user_id = get_jwt_identity()
    # log_activity('Viewed user list', user_id)

    return jsonify({'users': user_list}), 200

@app.route('/route-plans', methods=['GET', 'POST'])
@jwt_required()
def route_plan_details():
    if request.method == 'GET':
        route_plans = RoutePlan.query.all()
        if not route_plans:
            return jsonify({'message': 'No route plans found'}), 404

        route_plan_list = []
        for route_plan in route_plans:
            route_plan_info = {
                'id': route_plan.id,
                'merchandiser_id': route_plan.merchandiser_id,
                'manager_id': route_plan.manager_id,
                'date_range': route_plan.date_range,
                'instructions': route_plan.instructions,
                'status': route_plan.status
            }
            route_plan_list.append(route_plan_info)

        user_id = get_jwt_identity()
        log_activity('Viewed merchandiser routes', user_id)

        return jsonify({'route_plans': route_plan_list}), 200

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request, JSON data required"}), 400

        # Extract required fields from the JSON data
        merchandiser_id = data.get('merchandiser_id')
        manager_id = data.get('manager_id')
        date_range = data.get('date_range')
        instructions = data.get('instructions')
        status = data.get('status')

        # Check for required fields
        if not all([merchandiser_id, manager_id, date_range, status]):
            return jsonify({'message': 'Missing required fields'}), 400

        # Create a new route plan object
        new_route_plan = RoutePlan(
            merchandiser_id=merchandiser_id,
            manager_id=manager_id,
            date_range=date_range,
            instructions=instructions,
            status=status
        )

        try:
            db.session.add(new_route_plan)
            db.session.commit()

            user_id = get_jwt_identity()
            log_activity('Created merchandiser routes', user_id)
            return jsonify({'message': 'Route plan created successfully'}), 201
        except Exception as err:
            db.session.rollback()
            return jsonify({'error': f"Internal server error. Error: {err}"}), 500

@app.route('/route-plans/<int:route_plan_id>', methods=['PUT'])
@jwt_required()
def update_route_plan(route_plan_id):
    data = request.get_json()

    route_plan = db.session.get(RoutePlan, route_plan_id)
    if not route_plan:
        return jsonify({'message': 'Route plan not found'}), 404

    # Update route plan attributes
    route_plan.merchandiser_id = data.get('merchandiser_id', route_plan.merchandiser_id)
    route_plan.manager_id = data.get('manager_id', route_plan.manager_id)
    route_plan.date_range = data.get('date_range', route_plan.date_range)
    route_plan.instructions = data.get('instructions', route_plan.instructions)
    route_plan.status = data.get('status', route_plan.status)

    try:
        db.session.commit()

        user_id = get_jwt_identity()
        log_activity(f'Edited merchandiser route. Route id : {route_plan_id}', user_id)
        return jsonify({'message': 'Route plan updated successfully'}), 200

    except Exception as err:

        db.session.rollback()
        return jsonify({'error': f"Internal server error. Error: {err}"}), 500
    
@app.route('/locations', methods=['GET', 'POST'])
# @jwt_required()
def location_details():
    if request.method == 'GET':
        locations = Location.query.all()
        if not locations:
            return jsonify({'message': 'No locations found'}), 404

        location_list = []
        for location in locations:
            location_info = {
                'id': location.id,
                'merchandiser_id': location.merchandiser_id,
                'timestamp': location.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'latitude': location.latitude,
                'longitude': location.longitude
            }
            location_list.append(location_info)


        return jsonify({'locations': location_list}), 200
    elif request.method == 'POST':
        data = request.get_json()

        # Extract required fields from the JSON data
        merchandiser_id = data.get('merchandiser_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Check for required fields
        if not all([merchandiser_id, latitude, longitude]):
            return jsonify({'message': 'Missing required fields'}), 400

        # Create a new location object
        new_location = Location(
            merchandiser_id=merchandiser_id,
            timestamp=datetime.now(timezone.utc),
            latitude=latitude,
            longitude=longitude
        )

        try:
            db.session.add(new_location)
            db.session.commit()
            return jsonify({'message': 'Location created successfully'}), 201
        except Exception as err:
            db.session.rollback()
            return jsonify({'error': f"Internal server error. Error: {err}"}), 500
        

@app.route("/user/login", methods=["POST"])
def login_user():

    data = request.get_json()

    
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    email = data.get("email")
    password = data.get("password_hash")

    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    user = User.query.filter_by(email=email).first()

    
    if user:
        if user.status == "blocked":
            
            return jsonify({"message": "Access denied, please contact system administrator"}), 409
        
    
        if bcrypt.check_password_hash(user.password, password):

            if datetime.now(timezone.utc) - user.last_password_change.replace(tzinfo=timezone.utc) > timedelta(days=14):
                
                return jsonify({"message": "Your password has expired. Please change it."}), 403
            
            
            access_token = create_access_token(identity=user.id)
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()

            user_data = {
                "user_id": user.id,
                "access_token": access_token,
                "role": user.role,
                "username": user.username,
                "email": user.email,
                "last_name": user.last_name,
                "avatar": user.avatar,
                "last_login": user.last_login
                         }
            
            user_id = get_jwt_identity()
            log_activity(f'Logged in', user_id)
            return jsonify(user_data), 200
        
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route("/user/change-password", methods=["PUT"])
def change_password():
    
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    email = data.get("email")
     

    if old_password == new_password:
        return jsonify({"message": "Old password and new password cannot be the same."})

    if not old_password or not new_password:
        return jsonify({"error": "Missing required fields."}), 400

    user = User.query.filter_by(email=email).first()
    

    if user:

        user_id = user.id

        if bcrypt.check_password_hash(user.password, old_password):

            hashed_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

            user.password = hashed_new_password
            user.last_password_change = datetime.now(timezone.utc)
            db.session.commit()
            user_id = user_id
            log_activity(f'Changed password.', user_id)
            return jsonify({"message": "Password changed successfully"}), 201
        
        else:
            return jsonify({"error": "Invalid old password"}), 401
    else:
        return jsonify({"error": "User not found"}), 404



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)




