import os
from model.userModel import User
from src import db

def clear_users():
    User.query.delete()
    db.session.commit()

def create_admin_user():
    admin_user = User(
        username='admin',
        email=['ADMIN_EMAIL'],
        password=os.environ['ADMIN_PASSWORD']
    )
    db.session.add(admin_user)