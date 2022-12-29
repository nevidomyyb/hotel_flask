from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        "hotel_id": 1,
        "nome": "Alpha Hotel",
        "estrelas": 4.3,
        "diaria": 420.43,
        "cidade": "Rio de Janeiro"
    },
    {
        "hotel_id": 2,
        "nome": "Beta Hotel",
        "estrelas": 2.2,
        "diaria": 210.43,
        "cidade": "Maceio"
    },
    {
        "hotel_id": 3,
        "nome": "Bravo Hotel",
        "estrelas": 5,
        "diaria": 600.43,
        "cidade": "Cuiabá"
    }
]

def get_arguments():
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    return argumentos

def find_hotel(hotel_id):
    for hotel in hoteis:
        if hotel['hotel_id'] == hotel_id:
            return hotel
    return None


class Hotel(Resource):
    def get(self, hotel_id):
        hotel = find_hotel(hotel_id)
        if hotel:
            return hotel
        return {"message": "hotel not found"}, 404
    
    def put(self, hotel_id):

        dados = get_arguments().parse_args()
        novo_hotel = HotelModel(hotel_id, **dados)
        hotel = find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel.json())
            return hotel
        return {"message": "hotel not found"}, 404

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel["hotel_id"] != hotel_id]
        return {"message": "hotel deleted"}, 200
        

class Hoteis(Resource):
    def get(self):
        return hoteis

    def post(self):

        dados = get_arguments().parse_args()
        novo_id = len(hoteis) + 1
        novo_hotel = HotelModel(novo_id, **dados)
        hoteis.append(novo_hotel.json())
        return novo_hotel.json(), 200
