from sqlalchemy import create_engine, desc, select
from sqlalchemy.orm import Session, sessionmaker

import router
from sql_alchemy import database


class HotelModel(database.Model):
    __tablename__ = 'hoteis'
    hotel_id = database.Column(database.Integer, primary_key = True)
    nome = database.Column(database.String(80))
    estrelas = database.Column(database.Float(precision=1))
    diaria = database.Column(database.Float(precision=2))
    cidade = database.Column(database.String(40))

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade


    def json(self):
        return {
            "hotel_id" : self.hotel_id,
            "nome" : self.nome,
            "estrelas" : self.estrelas,
            "diaria" : self.diaria,
            "cidade" : self.cidade,
        }

    @classmethod
    def get_new_id(cls, database):
        #hotel = cls.query.order_by(HotelModel.hotel_id.desc()).first()
    
        engine = create_engine(router.select_database(database))
        Session = sessionmaker(engine)
        with Session.begin() as session:
            hotel = session.query(HotelModel).order_by(HotelModel.hotel_id.desc()).first()
            if hotel:
                new_id = hotel.hotel_id + 1
                return new_id 
            return 1
    
    @classmethod
    def find_hotel(cls, hotel_id, database):
        engine = create_engine(router.select_database(database))   
        session = Session(engine, future=True)
        statement = select(HotelModel).filter_by(hotel_id=hotel_id)
        result = session.execute(statement).scalars().first()
        return result

    def update_hotel(self, nome, estrelas, diaria, cidade, database):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria =  diaria
        self.cidade =  cidade
        engine = create_engine(router.select_database(database))
        Session = sessionmaker(engine)
        with Session.begin() as session:
            session.query(HotelModel).filter_by(hotel_id=self.hotel_id).update({
                "nome": nome,
                "estrelas": estrelas,
                "diaria": diaria,
                "cidade": cidade
                }, synchronize_session="fetch")
            session.commit()
            session.close()

    def save_hotel(self, database):
        engine = create_engine(router.select_database(database))
        Session = sessionmaker(engine)
        with Session.begin() as session:
            session.add(self)
            session.commit()
            session.close()

    def delete_hotel(self, database):
        engine = create_engine(router.select_database(database))
        Session = sessionmaker(engine)
        with Session.begin() as session:
            session.query(HotelModel).filter_by(hotel_id=self.hotel_id).delete(synchronize_session="fetch")
            session.commit()
            session.close()

    @classmethod
    def query_all(cls, database):
        engine = create_engine(router.select_database(database))
        session = Session(engine, future=True)
        statement = select(HotelModel)
        result = session.execute(statement).scalars().all()
        return result