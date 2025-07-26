import json
from flask import request, jsonify
from .services import (
    get_all_users_service, get_user_service, create_user_service,
    update_user_service, delete_user_service, search_users_service,
    login_user_service, user_exists_by_email
)
from .utils import is_valid_email, is_valid_password

# Adding comments for Easy COde Readability and Navigation
# Handled Exception/Error Handling using Try-Catch


# Root Route Registration
def register_routes(app):

    #Landing Page GET
    @app.route('/')
    def home():
        return jsonify({
            "message": "Hello !!! Welcome to Efficient User Management System",
            "status": "Flask Application Running"
        }), 200

    # Get All Users GET
    @app.route('/users', methods=['GET'])
    def get_all_users():
        return jsonify(get_all_users_service()), 200

    # Get User BY Id GET
    @app.route('/user/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = get_user_service(user_id)
        if user:
            return jsonify({"id": user[0], "name": user[1], "email": user[2]}), 200
        return jsonify({"error": "User not found"}), 404

    # Create A new User POST
    @app.route('/users', methods=['POST'])
    def create_user():
        try:
            data = json.loads(request.get_data())
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')

            # Validation checks
            if not (name and email and password):
                return jsonify({"error": "Missing required fields"}), 400

            if not is_valid_email(email):
                return jsonify({"error": "Invalid email format"}), 400

            if not is_valid_password(password):
                return jsonify({"error": "Password must be at least 6 characters long and include letters and numbers"}), 400

            if user_exists_by_email(email):
                return jsonify({"error": "Email already exists"}), 400

            create_user_service(name, email, password)
            return jsonify({"message": "User created successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Update User PUT 
    @app.route('/user/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        try:
            data = json.loads(request.get_data())
            name = data.get('name')
            email = data.get('email')

            if not (name and email):
                return jsonify({"error": "Missing name or email"}), 400

            if not is_valid_email(email):
                return jsonify({"error": "Invalid email format"}), 400

            rows_affected = update_user_service(user_id, name, email)
            if rows_affected == 0:
                return jsonify({"error": "User not found"}), 404

            return jsonify({"message": "User updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Remove User from db DELETE
    @app.route('/user/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        rows_affected = delete_user_service(user_id)
        if rows_affected == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": f"User {user_id} deleted successfully"}), 200

    # Search User by Name ?search in Params GET
    @app.route('/search', methods=['GET'])
    def search_users():
        name = request.args.get('name')
        if not name:
            return jsonify({"error": "Please provide a name to search"}), 400
        return jsonify(search_users_service(name)), 200

    # Login using Email and Password POST
    @app.route('/login', methods=['POST'])
    def login():
        try:
            data = json.loads(request.get_data())
            email = data.get('email')
            password = data.get('password')

            if not (email and password):
                return jsonify({"error": "Missing email or password"}), 400

            result = login_user_service(email, password)
            return jsonify(result), 200 if result["status"] == "success" else 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500
