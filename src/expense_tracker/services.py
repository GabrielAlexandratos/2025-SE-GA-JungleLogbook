from models import User

class UserService:
    def get_user(self, session, user_id):
        return session.query(User).get(user_id)