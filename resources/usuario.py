from flask_restful import Resource, reqparse

from models.usuario import UserModel


def getarguments():
    argumentos = reqparse.RequestParser()
    

class Usuario(Resource):
    def get(self, database, user_id):
        usuario = UserModel.find_user(user_id, database)
        if (usuario):
            return usuario.json()
        return {"message": "user not found"}, 404
    
    def delete(self, user_id, database):
        usuario = UserModel.find_user(user_id, database)
        if usuario:
            try:
                usuario.delete_user(database)
            except:
                return {
                    "message": f"An internal error ocurred while trying to delete \
                        {usuario.nome} from database"
                }, 500
            return {"message": "user deleted"}, 410
        return {"message": "user not found"}