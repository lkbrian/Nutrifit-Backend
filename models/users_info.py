from sqlalchemy_serializer import SerializerMixin
from config import db


class UserInfo(db.Model,SerializerMixin):
  __tablename__='TBL_USER_INFO'
  serialize_only=('info_id','user_id','user_goal','height','weight','gender','dietary_preferences','meals_per_day','deit_description','activity_levels')

  info_id=db.Column(db.Integer,primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("TBL_APP_USERS.user_id"), nullable=True)
  goal=db.Column(db.String,nullable=True)
  dob=db.Column(db.String,nullable=True)
  height=db.Column(db.String,nullable=True)
  weight=db.Column(db.String,nullable=True)
  gender=db.Column(db.String,nullable=True)
  dietary_preferences=db.Column(db.String,nullable=True)
  meals_per_day=db.Column(db.String,nullable=True)
  diet_description=db.Column(db.String,nullable=True)
  activity_levels=db.Column(db.String,nullable=True)
  nutrion_knowledge=db.Column(db.String,nullable=True)
  guidance_needed=db.Column(db.String,nullable=True)

  user = db.relationship("User", back_populates="user_info")
