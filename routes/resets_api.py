# import email
import os
# import secrets
from datetime import datetime, timedelta, timezone
from sqlite3 import IntegrityError
from venv import logger

from config import db, mail
from dotenv import load_dotenv
from flask import jsonify, make_response, request
from flask_mail import Message
from flask_restful import Resource
from werkzeug.security import generate_password_hash
import random
from models import Tokens,User

load_dotenv()
def get_unique_reset_token(self):
        """Generates a unique 5-digit reset token."""
        while True:
            reset_token = str(random.randint(10000, 99999))
            token_exists = Tokens.query.filter_by(token=reset_token).first()
            if not token_exists:
                return reset_token

class Forgot_password(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        print(data)

        if not email:
            return make_response(jsonify({"error": "Email is required"}), 400)

        user = User.query.filter_by(email=email).first()
        if not user:
            return make_response(jsonify({'msg':"user doesn't exist"}),404)
       
        reset_token = self.get_unique_reset_token()
        print(reset_token)
        # Create a Tokens entry with a 1-hour expiry
        reset_token_entry = Tokens(
            token=reset_token,request_type='Forgot Password', expires_at=datetime.utcnow() + timedelta(hours=1)
        )

        reset_token_entry.user_id = user.user_id

        # Save token to the database
        db.session.add(reset_token_entry)
        db.session.commit()

        try:

            expiration_time = "1 hour"

            html_body = f"""
                    <div
                    style="width: 100%;background: #ebf2fa;padding: 20px 0 0 0;font-family: system-ui, sans-serif; text-align: center;">
                    <div
                    style="border-top: 6px solid #c5e46c; background-color: #fff; display: block; padding:  8px 20px; text-align: center;   max-width: 500px;  border-bottom-left-radius: .4rem; border-bottom-right-radius: .4rem; letter-spacing: .037rem; line-height: 26px;  margin: auto; font-size: 14px; ">
                    <div style="text-align: left; padding-top: 10px;">
                        <p style="text-align: center;">You have requested to change your email address, to confirm the change,use this code 
                        </p>
                    </div>
                        <h1>{reset_token}</h1>

                    <!-- Additional Information -->
                    <div style="text-align: center; padding-top: 2px;">
                        <p>Code  expires in <strong>{expiration_time}</strong>.</p>
                    </div>
                    </div>
                    <p style="padding: 20px 0 5px 0; text-align: center;color: rgb(150, 150, 150);font-size: 12px;">Nutrifit
                    Community
                    </p>
                    </div>"""

            # Create message
            msg = Message(
                subject="Nutrifit Otp",
                sender=os.getenv("MAIL_USERNAME"),
                recipients=[user.email],
                html=html_body,
            )

            mail.send(msg)

            return make_response(
                jsonify({"msg": " verification code sent to your old email"}), 201
            )
        except Exception as e:
            logger.error(f"Error sending password reset email: {e}")
            db.session.rollback()
            return make_response(
                jsonify(
                    {
                        "error": "An error occurred while sending the email. Please try again later."
                    }
                ),
                500,
            )        
     
        # Generate reset token
        # reset_token = secrets.token_urlsafe(16)
        # reset_token_entry = Tokens(
        #     token=reset_token,
        #     expires_at=datetime.utcnow()
        #     + timedelta(hours=1),  # Token expires in 1 hour
        # )

        # # Associate reset token with the entity
        # reset_token_entry.user_id = user.user_id
      

        # db.session.add(reset_token_entry)
        # db.session.commit()
        # try:
        #     reset_link = f"http://localhost:4000/reset_password?token={reset_token}"
        #     expiration_time = "1 hour"

        #     html_body = f"""
        #     <div
        #       style="width: 100%;background: #ebf2fa;padding: 20px 0 0 0;font-family: system-ui, sans-serif; text-align: center;">
        #       <div
        #       style="border-top: 6px solid #c5e46c; background-color: #fff; display: block; padding:  8px 20px; text-align: center;   max-width: 500px;  border-bottom-left-radius: .4rem; border-bottom-right-radius: .4rem; letter-spacing: .037rem; line-height: 26px;  margin: auto; font-size: 14px; ">
        #       <div style="text-align: left; padding-top: 10px;">
        #           <p>We've received a request to reset the password for the Nutrifit account associated with {user.email}.
        #           Please note that no changes have been made to your account yet. We recommend resetting your password
        #           immediately, to ensure the security of your account.</p>
        #           <p>Click the button below to reset your password:</p>
        #       </div>
        #       <!-- Button -->
        #       <a href='{reset_link}'
        #           style='display: inline-block;width:90%; padding: 8px 20px;  color: #111; linear-gradient(135deg, rgba(197,228,108,1) 25%, rgba(79,164,58,1) 100%); text-decoration: none; border-radius: .4rem;'>
        #           Reset Password
        #       </a>
        #       <!-- Additional Information -->
        #       <div style="text-align: center; padding-top: 2px;">
        #           <p>This link will expire in <strong>{expiration_time}</strong>.</p>
        #       </div>
        #       </div>
        #       <p style="padding: 20px 0 5px 0; text-align: center;color: rgb(150, 150, 150);font-size: 12px;">Nutrifit 
        #       Community
        #       </p>
        #   </div>"""

        #     # Create message
        #     msg = Message(
        #         subject="Reset Your Password",
        #         sender=os.getenv("MAIL_USERNAME"),
        #         recipients=[user.email],
        #         html=html_body,
        #     )

        #     mail.send(msg)

        #     return make_response(
        #         jsonify({"message": "Password reset link sent to your email"}), 200
        #     )
        # except Exception as e:
        #     logger.error(f"Error sending password reset email: {e}")
        #     db.session.rollback()
        #     return make_response(
        #         jsonify(
        #             {
        #                 "error": "An error occurred while sending the email. Please try again later."
        #             }
        #         ),
        #         500,
        #     )

class Reset_password(Resource):
    def post(self):
        data = request.json
        token = data.get("token")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        # Validate inputs
        if not token:
            return make_response(jsonify({"msg": "Token is required"}), 400)
        if not new_password or not confirm_password:
            return make_response(jsonify({"msg": "Password fields are required"}), 400)
        if new_password != confirm_password:
            return make_response(jsonify({"msg": "Passwords do not match"}), 400)

        # Find the reset token entry
        reset_token_entry = Tokens.query.filter_by(token=token).first()

        if not reset_token_entry:
            return make_response(jsonify({"msg": "Invalid or expired token"}), 400)

        # Check if the token is expired
        if reset_token_entry.expires_at < datetime.utcnow():
            db.session.delete(reset_token_entry)
            db.session.commit()
            return make_response(jsonify({"msg": "Token has expired"}), 400)

        # Determine which account type to reset based on account_type
        entity = User.query.filter_by(user_id=reset_token_entry.user_id).first()

        if not entity:
            return make_response(
                jsonify({"msg": "No account associated with this token"}), 400
            )

        # Reset the password
        entity.password_hash = generate_password_hash(new_password)

        # Delete the reset token after use
        db.session.delete(reset_token_entry)
        db.session.commit()

        return make_response(
            jsonify({"msg": "Password has been reset successfully"}), 200
        )



class Change_email(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        new_email = data.get("newEmail")

        if not email:
            return make_response(jsonify({"error": "Email is required"}), 400)
        if not new_email:
          return make_response(jsonify({"error": "New email is required"}), 400)


        user = User.query.filter_by(email=email).first()
        if not user:
          return make_response(jsonify({'msg':"user doesn't exist"}),404)
        
        existing_user = User.query.filter_by(email=new_email).first()
        if existing_user:
            return make_response(
                jsonify({"msg": "This email address is already in use."}), 409
            )
        
        reset_token = self.get_unique_reset_token()

        # Create a Tokens entry with a 1-hour expiry
        reset_token_entry = Tokens(
            token=reset_token, expires_at=datetime.utcnow() + timedelta(hours=1)
        )

        reset_token_entry.user_id = user.user_id

        # Save token to the database
        db.session.add(reset_token_entry)
        db.session.commit()

        try:

            expiration_time = "1 hour"

            html_body = f"""
                    <div
                    style="width: 100%;background: #ebf2fa;padding: 20px 0 0 0;font-family: system-ui, sans-serif; text-align: center;">
                    <div
                    style="border-top: 6px solid #c5e46c; background-color: #fff; display: block; padding:  8px 20px; text-align: center;   max-width: 500px;  border-bottom-left-radius: .4rem; border-bottom-right-radius: .4rem; letter-spacing: .037rem; line-height: 26px;  margin: auto; font-size: 14px; ">
                    <div style="text-align: left; padding-top: 10px;">
                        <p style="text-align: center;">You have requested to change your email address, to confirm the change,use this code 
                        </p>
                    </div>
                        <h1>{reset_token}</h1>

                    <!-- Additional Information -->
                    <div style="text-align: center; padding-top: 2px;">
                        <p>Code  expires in <strong>{expiration_time}</strong>.</p>
                    </div>
                    </div>
                    <p style="padding: 20px 0 5px 0; text-align: center;color: rgb(150, 150, 150);font-size: 12px;">Nutrifit
                    Community
                    </p>
                    </div>"""

            # Create message
            msg = Message(
                subject="Nutrifit Otp",
                sender=os.getenv("MAIL_USERNAME"),
                recipients=[user.email],
                html=html_body,
            )

            mail.send(msg)

            return make_response(
                jsonify({"msg": " verification code sent to your old email"}), 201
            )
        except Exception as e:
            logger.error(f"Error sending password reset email: {e}")
            db.session.rollback()
            return make_response(
                jsonify(
                    {
                        "error": "An error occurred while sending the email. Please try again later."
                    }
                ),
                500,
            )        
       

class Verify_token(Resource):
  def post(self):
        
        email = request.headers.get('email')
        token = request.headers.get('token')
        if not token:
            return make_response(jsonify({"msg": "Token is required"}), 400)

        reset_token_entry = Tokens.query.filter_by(token=token).first()

        if not reset_token_entry:
            return make_response(jsonify({"msg": "Invalid token"}), 400)

        # Check if the token is expired
        if reset_token_entry.expires_at < datetime.now(timezone.utc):
            db.session.delete(reset_token_entry)
            db.session.commit()
            return make_response(jsonify({"msg": "Token has expired"}), 400)
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return make_response(
                jsonify({"msg": "This email address is already in use."}), 409
            )
        try:
                expiration_time = "1 hour"
                reset_link = f"http://localhost:4000/change_email?token={token}&email={email}"

                html_body = f"""
                        <div
                        style="width: 100%;background: #ebf2fa;padding: 20px 0 0 0;font-family: system-ui, sans-serif; text-align: center;">
                        <div
                        style="border-top: 6px solid #c5e46c; background-color: #fff; display: block; padding:  8px 20px; text-align: center;   max-width: 500px;  border-bottom-left-radius: .4rem; border-bottom-right-radius: .4rem; letter-spacing: .037rem; line-height: 26px;  margin: auto; font-size: 14px; ">
                        
                        <div style="text-align: left; padding-top: 10px;">
                            <p style="text-align: center;">To verify and update the  your email address to {email}
                            click the button below <br/> note that this will be the new channel of communication and future logins
                            </p>
                        </div>
                        <a href='{reset_link}'
                          tyle='display: inline-block;width:90%; padding: 8px 20px;  color: #111; linear-gradient(135deg, rgba(197,228,108,1) 25%, rgba(79,164,58,1) 100%); text-decoration: none; border-radius: .4rem;'>
                          Click here
                        </a>
                        <div style="text-align: center; padding-top: 2px;">
                        <p>Code  expires in <strong>{expiration_time}</strong>.</p>
                    </div>
                        </div>
                        <p style="padding: 20px 0 5px 0; text-align: center;color: rgb(150, 150, 150);font-size: 12px;">Happy Hearts
                        Community
                        </p>
                        </div>"""

                # Create message
                msg = Message(
                    subject="Email Update",
                    sender=os.getenv("MAIL_USERNAME"),
                    recipients=[email],
                    html=html_body,
                )

                mail.send(msg)
        except Exception as e:
                logger.error(f"Error sending password reset email: {e}")
                return make_response(
                    jsonify({"msg": f"{e}, Check your mail and try Again"}),
                    500,
                )
        

class Verify_email(Resource):
    def patch(self):
        
        token = request.args.get('token')
        email = request.args.get('email')
        if not token:
            return make_response(jsonify({"msg": "Token is required"}), 400)

        reset_token_entry = Tokens.query.filter_by(token=token).first()

        if not reset_token_entry:
            return make_response(jsonify({"msg": "Invalid token"}), 400)
        
        user = User.query.filter_by(user_id=reset_token_entry.user_id).first()
        if not user:
          return make_response(jsonify({'msg':"user doesn't exist"}),404)
        
        user.email=email
        db.session.delete(reset_token_entry)
        db.session.commit()
        try:

            html_body = f"""
                    <div
                    style="width: 100%;background: #ebf2fa;padding: 20px 0 0 0;font-family: system-ui, sans-serif; text-align: center;">
                    <div
                    style="border-top: 6px solid #c5e46c; background-color: #fff; display: block; padding:  8px 20px; text-align: center;   max-width: 500px;  border-bottom-left-radius: .4rem; border-bottom-right-radius: .4rem; letter-spacing: .037rem; line-height: 26px;  margin: auto; font-size: 14px; ">
                    
                    <div style="text-align: left; padding-top: 10px;">
                        <p style="text-align: center;">Email has been updated sucessfully.</p>
                    </div>

                    <!-- Additional Information -->
                    <div style="text-align: center; padding-top: 2px;">
                        <p> For assistance, reach us at
                        <a href='mailto:{os.getenv(' MAIL_USERNAME')}'
                            style='color: #c5e46c; text-decoration: underline;'>{os.getenv('MAIL_USERNAME')}</a>.
                        </p>
                    </div>
                    </div>
                    <p style="padding: 20px 0 5px 0; text-align: center;color: rgb(150, 150, 150);font-size: 12px;">Happy Hearts
                    Community
                    </p>
                    </div>"""

            # Create message
            msg = Message(
                subject="Email Update",
                sender=os.getenv("MAIL_USERNAME"),
                recipients=[email],
                html=html_body,
            )

            mail.send(msg)

            return make_response(jsonify({"msg": " Email Update sucessful"}), 200)
        except Exception as e:
            logger.error(f"Error sending password reset email: {e}")
            db.session.rollback()
            return make_response(
                jsonify({"msg": f"{e}, Check your mail and try Again"}),
                500,
            )

            return make_response(
                jsonify({"msg": "Email has been changed successfully"}), 200
            )
        except IntegrityError as e:
            db.session.rollback()
            if "UNIQUE constraint failed" in str(e.orig):
                return make_response(
                    jsonify({"msg": "This email address is already in use."}), 400
                )
            return make_response(
                jsonify({"msg": "Database integrity error occurred"}), 400
            )
        except Exception as e:
            return make_response(jsonify({"msg": str(e)}), 500)