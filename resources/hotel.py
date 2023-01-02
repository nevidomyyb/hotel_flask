from flask_restful import Resource, reqparse

from models.hotel import HotelModel


def get_arguments():
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="can not be empty")
    argumentos.add_argument('estrelas', type=float, required=True, help="can not be empty")
    argumentos.add_argument('diaria', type=float, required=True, help="can not be empty")
    argumentos.add_argument('cidade', type=str, required=True, help="can not be empty")
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
            try:
                hotel.update_hotel(**dados, database=database)
            except:
                return {
                    "message": f"An internal server error ocurred while trying to update {dados.nome} \
                    into database"
                }, 500
            return hotel.json(), 200
        return {"message": "hotel not found"}, 404


    def delete(self, hotel_id, database):
        hotel= HotelModel.find_hotel(hotel_id, database)
        if hotel:
            try:
                hotel.delete_hotel(database)
            except:
                return {
                    "message": f"An internal server error ocurred while trying to delete {hotel.nome} \
                        from database"
                }, 500
            return {"message": "hotel deleted"}, 410
        return {"message": "hotel not found"}, 404        

class Hoteis(Resource):
    def get(self, database):
        return [hotel.json() for hotel in HotelModel.query_all(database=database)]



    def post(self, database):
        dados = get_arguments().parse_args()
        novo_id = HotelModel.get_new_id(database=database)
        novo_hotel = HotelModel(novo_id, **dados)
        try:
            novo_hotel.save_hotel(database) 
        except:
            return {
                "message": f"An internal server error ocurred while trying save {novo_hotel.name} \
                    into database"
            }, 500
        hotel = HotelModel.find_hotel(novo_id, database)
        return hotel.json(), 201

