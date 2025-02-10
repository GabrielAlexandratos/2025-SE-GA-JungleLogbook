from sqlalchemy import func
from expense_tracker.models import User, Expense
from sqlalchemy.orm import Session

class UserService:
    def get_user(self, session: Session, user_id):
        return session.query(User).get(user_id)
    
    def get_user_by_email(self, session: Session, email: str):
        return session.query(User).filter_by(email=email).first()
    
    def create_user(self, session: Session, email, password):
        new_user = User(email=email, password=password)
        session.add(new_user)
        session.commit()
        return new_user
    
class ExpenseService:
    def get_expenses(self, session: Session):
        return session.query(Expense).order_by('date').all()
    
    def create(self, session: Session, title, category, amount, date, description) -> Expense:
        new_expense = Expense(title=title, category=category, amount=amount, date=date, description=description)
        session.add(new_expense)
        session.commit()
        return new_expense

    def update(self, session, expense_id, title=None, category=None, amount=None, date=None, description=None) -> Expense:
        expense = session.query(Expense).get(expense_id)
        if not expense:
            raise ValueError(f"Expense {expense_id} does not exist")
        if title is not None:
            expense.title = title
        if category is not None:
            expense.category = category
        if amount is not None:
            expense.amount = amount
        if date is not None:
            expense.date = date
        if description is not None:
            expense.description = description
        session.commit()
        return expense

    def delete(self, session, expense_id) -> Expense:
        expense = session.query(Expense).get(expense_id)
        if not expense:
            raise ValueError("Expense does not exist")
        session.delete(expense)
        session.commit()
        return expense
    
    def get_by_id(self, session, expense_id) -> Expense:
        expense = session.query(Expense).get(expense_id)
        if not expense:
            raise ValueError(f"Expense {expense_id} does not exist")
        return expense

    def calculate_total(self, session) -> float:
        total_expenses = session.query(func.sum(Expense.amount)).scalar()
        return total_expenses or 0.0
