from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from expense_tracker.models import Base
from expense_tracker.services import ExpenseService

@pytest.fixture(scope='module')
def db_session():
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        yield session
        session.rollback()
        session.close()

@pytest.fixture(scope='module')
def expense_service():
    yield ExpenseService()

def test_add_remove_expense(db_session, expense_service: ExpenseService):
    expense = expense_service.create(db_session, 'test', 'category', 140.50, datetime.now(), "Groceries")
    assert len(expense_service.get_expenses(db_session)) == 1
    expense_service.delete(db_session, expense.id)
    assert len(expense_service.get_expenses(db_session)) == 0

def test_get_total_expenses(db_session, expense_service: ExpenseService):
    expense_service.create(db_session, 'test', 'category', 140.50, datetime.now(), "Groceries")
    expense_service.create(db_session, 'test', 'category', 200.50, datetime.now(), "Utilities")
    total_expenses = expense_service.calculate_total(db_session)
    assert total_expenses == 341.0
