from config import db
from datetime import datetime,timedelta,timezone

class ResetToken(db.Model):
    __tablename__='resetokens'
    token_id= db.Column(db.Integer,primary_key=True)
    token = db.Column(db.String, nullable=False, unique=True)
    expires_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc) + timedelta(hours=1))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    
    user = db.relationship("User", back_populates="reset_tokens")