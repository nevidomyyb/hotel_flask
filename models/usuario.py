import base64

from sqlalchemy import create_engine, desc, select
from sqlalchemy.orm import Session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

import router
from sql_alchemy import database


class UserModel(database.Model):
    __tablename__ = 'usuarios'

    user_id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String(40))
    password = database.Column(database.String(400))
    first_name = database.Column(database.String(40))
    last_name = database.Column(database.String(40))
    mail = database.Column(database.String(100))
    is_admin = database.Column(database.Boolean, default = 0)
    
    
    def __init__(self, user_id, username, password, first_name, last_name, mail, is_admin):
        self.user_id = user_id
        self.username = username
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.mail = mail
        self.is_admin = is_admin

    def json(self):
        return {
            "user_id": self.user_id,
            "username" : self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "mail": self.mail,
            "password": self.password
            
        }
    
    @classmethod
    def get_new_id(cls, database):
        engine = create_engine(router.select_database(database))
        session = Session(engine, future=True)
        statement = select(UserModel).order_by(UserModel.user_id.desc())
        result = session.execute(statement).scalars().first()
        if result:
            return result.user_id + 1
        return 1


    @classmethod
    def find_user(cls, user_id, database):
        engine = create_engine(router.select_database(database))
        session = Session(engine, future=True)
        statement = select(UserModel).filter_by(user_id=user_id)
        result = session.execute(statement).scalars().first()
        session.close()
        return result

    @classmethod
    def find_by_username(cls, username, database):
        engine = create_engine(router.select_database(database))
        session = Session(engine, future=True)
        statement = select(UserModel).filter_by(username=username)
        result = session.execute(statement).scalars().first()
        return result
    
    @classmethod
    def find_by_mail(cls, mail, database):
        engine = create_engine(router.select_database(database))
        session = Session(engine, future=True)
        statement = select(UserModel).filter_by(mail=mail)
        result = session.execute(statement).scalars().first()
        return result

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
   
    @classmethod
    def verify_safe_password(cls, password):
        unsafe_chars = [';', '/', '\\', '>', '<', '"', "'", ',']
        for char in unsafe_chars:
            if char in password:
                return char
        return True
    @classmethod
    def verify_length_password(cls, password):
        if len(password) < 8:
            return False
        return True
    
        

    def save_user(self, database):
        engine = create_engine(router.select_database(database))
        Session = sessionmaker(engine, future=True)
        with Session.begin() as session:
            session.add(self)
            session.commit()
            session.close()

    
    def delete_user(self, database):
        engine = create_engine(router.select_database(database))
        Session = sessionmaker(engine)
        with Session.begin() as session:
            session.query(UserModel).filter_by(user_id=self.user_id).delete(synchronize_session="fetch")
            session.commit()
            session.close()

