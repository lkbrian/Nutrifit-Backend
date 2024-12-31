from sqlalchemy_serializer import SerializerMixin
from config import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class Staging(db.Model,SerializerMixin):
  __tablename__='TBL_STAGING'

  serialize_only = (
        "user_id",
        "name",
        "email",
        "timestamp",
    )

  user_id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(70), nullable=False, unique=True)
  password_hash = db.Column(db.String, nullable=False)
  token = db.Column(db.String, nullable=False)
  expires_at = db.Column(db.DateTime, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
  updated_at = db.Column(db.DateTime, onupdate=datetime.now())

  # token = db.relationship("Tokens", back_populates="user")
  # messages = db.relationship("Message", back_populates="user")

  def set_password(self, password):
      self.password_hash = generate_password_hash(password)

  def check_password(self, password):
      return check_password_hash(self.password_hash, password)
  
class User(db.Model,SerializerMixin):
  __tablename__='TBL_APP_USERS'

  serialize_only = (
        "user_id",
        "name",
        "email",
        "timestamp",
    )

  user_id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(70), nullable=False, unique=True)
  password_hash = db.Column(db.String, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
  updated_at = db.Column(db.DateTime, onupdate=datetime.now())

  reset_tokens = db.relationship("Tokens", back_populates="user")
  user_info = db.relationship("UserInfo", back_populates="user")
  # messages = db.relationship("Message", back_populates="user")

  def set_password(self, password):
      self.password_hash = generate_password_hash(password)

  def check_password(self, password):
      return check_password_hash(self.password_hash, password)
  

