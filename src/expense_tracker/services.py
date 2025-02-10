from models import User
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