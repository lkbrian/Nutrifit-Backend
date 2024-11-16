from flask import jsonify, make_response, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    unset_jwt_cookies,
)
from flask_restful import Resource
from models import User
class Home(Resource):
    def get(self):
        return make_response(
            jsonify({"msg": "Nutrifit Backend"}), 200
        )
class Login(Resource):
    def post(self):
        data = request.json
        if not data:
          return {"msg": "No Input was provided"}
        
        email = data["email"]
        password = data["password"]

        user = User.query.filter_by(email=email).first()
        if not user:
          return make_response(jsonify({'msg':"user doesn't exist"}),404)
        elif user and user.check_password(password):
          token = create_access_token(
            identity={
                "email": user.email,
                "id": user.user_id,
            },
            additional_claims={"role": user.role},
        )

          response = {
              "token": token,
              "id": user.user_id,
              "email": user.email,
          }
          return response
        else:
          return make_response(jsonify({'msg':"Invalid user credentials"}),401)


class Logout(Resource):
    @jwt_required()
    def delete(self):
        current_user = get_jwt_identity()
        response = make_response(
            jsonify({"msg": f"Logged out {current_user.get('email')}"}), 200
        )
        unset_jwt_cookies(response)
        return response