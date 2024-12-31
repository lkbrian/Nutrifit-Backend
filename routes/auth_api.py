from datetime import datetime,timedelta
from flask import jsonify, make_response, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    unset_jwt_cookies,
)
from flask_restful import Resource
from models import User,Staging
from config import db,mail
import uuid
import os
from flask_mail import Message
from werkzeug.security import generate_password_hash
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
        )

          response = {
              "token": token,
              "id": user.user_id,
              "email": user.email,
          }
          return response
        else:
          return make_response(jsonify({'msg':"Invalid credentials"}),401)


class Logout(Resource):
    @jwt_required()
    def delete(self):
        current_user = get_jwt_identity()
        response = make_response(
            jsonify({"msg": f"Logged out {current_user.get('email')}"}), 200
        )
        unset_jwt_cookies(response)
        return response


class CreateAccount(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email:
            return make_response(jsonify({"error": "Email is required"}), 400)
        
        expired_staging_entry = Staging.query.filter_by(email=email).first()
        if expired_staging_entry and expired_staging_entry.expires_at < datetime.utcnow():
            # Delete expired entry before proceeding with new token creation
            db.session.delete(expired_staging_entry)
            db.session.commit()

        # Check if email is already in the system
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return make_response(jsonify({"error": "Email already exists"}), 400)

        
        verification_token = uuid.uuid4()

        
        staging_entry = Staging(
            email=email,
            password_hash=generate_password_hash(password, method="pbkdf2:sha512"),
            token=str(verification_token),
            expires_at=datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
        )

        db.session.add(staging_entry)
        db.session.commit()

        # Send verification email
        verification_link = f"{os.getenv('LOCAL_DEV_VERIFICATION_LINK')}?token={verification_token}"
        expiration_time = "1 hour"
        
        html_body = f"""
          <div  style="width: 100%;background: #ebf2fa;padding: 20px 0 10px 0;font-family: system-ui, sans-serif; text-align: center; border-radius: .3rem;">
            <div style=" background-color: #fff;  max-width: 500px; margin: auto; font-size: 14px;">
              <div
                style="border-top-left-radius: .3rem;border-top-right-radius: .3rem;background: #205A13; height: 50px;color: #ebf2fa;">
                <h1 style="font-size: 38px; font-weight: bold; text-align: center;">Nutrifit</h1>
              </div>
              <div style="padding:  0px 20px;">
                <p>Welcome! Please verify your email address to complete the registration for your Nutrifit account.</p>
                <p>Click the button below to verify your email:</p>
                <a href='{verification_link}'
                  style='display: inline-block;width:90%; padding: 8px 20px; color:  #111;
                  cursor: pointer; text-decoration: none; border-radius: .4rem;background: #205A13; width: 50%;line-height: 30px;color: #fff;'>Verify
                  Email</a>
                <p>This link will expire in <strong>{expiration_time}</strong>.</p>
              </div>
              <p style=" text-align: center;color: rgb(150, 150, 150);font-size: 12px;">Nutrifit Community
              </p>
            </div>
          </div>""" 

        msg = Message(
            subject="Verify Your Account",
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[email],
            html=html_body,
        )

        try:
            mail.send(msg)
            return make_response(jsonify({"message": "Verification link sent to your email"}), 200)
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response(jsonify({"error": "An error occurred while sending the email. Please try again later."}), 500)
        

class VerifyAccount(Resource):
    def post(self):
        data = request.json
        token = data.get("token")

        if not token:
            return make_response(jsonify({"error": "Token is required"}), 400)

        # Look for the token in the staging table
        staging_entry = Staging.query.filter_by(token=token).first()

        if not staging_entry:
            return make_response(jsonify({"error": "Invalid token or token already used"}), 400)

        if staging_entry.expires_at < datetime.utcnow():
            # Token expired: delete the staging entry and inform the user
            db.session.delete(staging_entry)
            db.session.commit()  # Ensure the expired entry is removed
            return make_response(jsonify({"error": "Token expired. Please create account again."}), 400)

        # Now create the user and move them from staging to the users table
        user = User(
            email=staging_entry.email,
            password_hash=staging_entry.password_hash,
            created_at=datetime.utcnow()
        )

        db.session.add(user)
        db.session.delete(staging_entry)  # Remove the staging entry after user creation
        db.session.commit()

        return make_response(jsonify({"message": "Account successfully created and verified"}), 200)
