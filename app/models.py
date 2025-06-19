from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='citizen')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DocumentRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    document_type = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='Received')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    purpose = db.Column(db.String(200), nullable=False)
    schedule_date = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Pending')

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String(200), nullable=False)
    transaction_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(50), default='Pending')

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default='Submitted')

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, server_default=db.func.now())

