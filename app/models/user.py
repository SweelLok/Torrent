from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password
        
    def get_id(self):
        return str(self.user_id)