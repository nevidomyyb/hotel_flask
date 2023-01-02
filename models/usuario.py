from sqlalchemy import create_engine, desc, select
from sqlalchemy.orm import Session, sessionmaker

import router
from sql_alchemy import database


class UserModel(database.Model):
    __tablename__ = 'usuarios'

    user_id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String(40))
    password = database.Column(database.String(40))
    first_name = database.Column(database.String(40))
    last_name = database.Column(database.String(40))
    mail = database.column(database.String(100))

    def __init__(self, username, password, first_name, last_name, mail):
        self.username = username
        self.password = password,
        self.first_name = first_name
        self.last_name = last_name
        self.mail = mail

    def json(self):
        return {
            "user_id": self.user_id,
            "username" : self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "mail": self.mail
            
        }
    
    @classmethod
    def find_user(cls, user_id, database):
        engine = create_engine(router.select_database(database))
        session = Session(engine, future=True)
        statement = select(UserModel).filter_by(user_id=user_id)
        result = session.execute(statement).scalars().first()
        return result

    def save_user(self, database):
        engine = create_engine(router.select_database(database))
        Session = sessionmaker(engine)
        with Session.begin() as session:
            session.add(self)
    
    def delete_hotel(self, database):
        engine = create_engine(router.select_database(database))
        Session = sessionmaker(engine)
        with Session.begin() as session:
            session.query(UserModel).filter_by(user_id=self.user_id).delete(synchronize_session="fetch")

