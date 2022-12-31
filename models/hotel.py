from sqlalchemy import create_engine, desc
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
        Session = sessionmaker(engine)
        with Session.begin() as session:
            hotel = session.query(HotelModel).filter_by(hotel_id=hotel_id).first()
            if hotel:
                return {
                    "hotel_id": hotel.hotel_id,
                    "nome": hotel.nome,
                    "estrelas": hotel.estrelas,
                    "diaria": hotel.diaria,
                    "cidade": hotel.cidade
                }
            else:
                return None

    @classmethod
    def save_hotel(cls, hotel, database):
        engine = create_engine(router.select_database(database))
        Session = sessionmaker(engine)
        with Session.begin() as session:
            session.add(hotel)
        