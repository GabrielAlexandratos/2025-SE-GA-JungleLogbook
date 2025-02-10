from extensions import db
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