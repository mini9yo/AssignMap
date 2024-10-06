from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __table_args__ = {'extend_existing': True}
    email = db.Column(db.String(100), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def create_user(email, name, user_type, password):
    
    new_user = User(email=email, name=name, user_type=user_type)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()






