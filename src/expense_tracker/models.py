from flask_login import UserMixin
from extensions import db, bcrypt
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timezone

# Define the base class for declarative models.
class Base(DeclarativeBase):
  pass

class Expense(db.Model):
    __tablename__ = 'expense'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.Date, nullable=False, default=datetime.now(timezone.utc))
    description = db.Column(db.String(255), nullable=True)


    def __repr__(self):
        return f"Expense('{self.title}', '{self.category}', {self.amount}, {self.date})"
    

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin

    def __repr__(self):
        return f"<email {self.email}>"