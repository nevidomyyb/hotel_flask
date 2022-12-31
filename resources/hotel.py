from flask_restful import Resource, reqparse

from models.hotel import HotelModel


def get_arguments():
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    return argumentos

class Hotel(Resource):
    def get(self, database, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id, database)
        if hotel:
            return hotel.json()
        return {"message": "hotel not found"}, 404
    
    def put(self, hotel_id, database):
        dados = get_arguments().parse_args()   
        hotel = HotelModel.find_hotel(hotel_id, database)
        if hotel:
            hotel.update_hotel(**dados, database=database)
            return hotel.json(), 200
        return {"message": "hotel not found"}, 404


    def delete(self, hotel_id, database):
        hotel= HotelModel.find_hotel(hotel_id, database)
        if hotel:
            hotel.delete_hotel(database)
            return {"message": "hotel deleted"}, 410
        return {"message": "hotel not found"}, 404        

class Hoteis(Resource):
    def get(self, database):
        return [hotel.json() for hotel in HotelModel.query_all(database=database)]



    def post(self, database):
        dados = get_arguments().parse_args()
        novo_id = HotelModel.get_new_id(database=database)
        novo_hotel = HotelModel(novo_id, **dados)
        novo_hotel.save_hotel(database) 

        hotel = HotelModel.find_hotel(novo_id, database)

        return hotel.json(), 201

