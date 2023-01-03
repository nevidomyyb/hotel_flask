from datetime import timedelta

from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
from flask_restful import Resource, reqparse

from models.usuario import UserModel


def getarguments():
    argumentos = reqparse.RequestParser()
    
def is_admin(database):
    current_user = UserModel.find_by_username(get_jwt_identity(), database)
    if not current_user.is_admin:
        return False
    return True

class Usuario(Resource):
    @jwt_required()
    def get(self, database, user_id):
        
        if not is_admin(database): return {"message": "only for admins"}
        usuario = UserModel.find_user(user_id, database)
        if usuario:
            return usuario.json()
        return {"message": "user not found"}, 404
    @jwt_required()
    def delete(self, user_id, database):
        if not is_admin(database): return {"message": "only for admins"}
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
        return {"message": "user not found"}, 404
    
class UsuarioRegistro(Resource):
    
    def post(self, database):
        atributos = reqparse.RequestParser()
        atributos.add_argument("username", type=str, required=True, help="can not be empty")
        atributos.add_argument("password", type=str, required=True, help="can not be empty")
        atributos.add_argument("first_name", type=str, required=True, help="can not be empty")
        atributos.add_argument("last_name", type=str, required=True, help="can not be empty")
        atributos.add_argument("mail", type=str, required=True, help="can not be empty")
        atributos.add_argument("is_admin", type=bool)
        dados = atributos.parse_args()

        #checks if the provided username already exists in database
        if UserModel.find_by_username(dados['username'], database): return {"message": "username already in use"}, 400
        #checks if the provided mail already exists in database
        if UserModel.find_by_mail(dados['mail'], database): return {"message": "email already in use"}, 400
        #checks if the provided password is safe to save in database
        safe = UserModel.verify_safe_password(dados['password'])
        if safe != True:
            return {"message": f"can not use {safe} in password"}, 400
        #checks if the provided password is longer than 8 characters
        if not UserModel.verify_length_password(dados['password']): return {"message": "the provided password is shorter than 8 characters"}, 400
        #check if the provided email is valid
        #if not UserModel.verify_mail(dados['mail']): return {"message": "the provided email is invalid"}, 400
        
        #encrypt the password to save in database
        #dados['password'] = UserModel.encrypt_password(dados['password'])
       
        new_id = UserModel.get_new_id(database)
        user = UserModel(new_id, **dados)
        user.save_user(database)
        user = UserModel.find_user(new_id, database)
        return user.json(), 201

class UserLogin(Resource):

    @classmethod
    def post(cls, database):
        atributos = reqparse.RequestParser()
        atributos.add_argument("username", type=str, required=True, help="can not be empty")
        atributos.add_argument("password", type=str, required=True, help="can not be empty")
        dados = atributos.parse_args()

        user = UserModel.find_by_username(dados['username'], database)
        if user and user.check_password(password=dados['password']):
            token_de_acesso = create_access_token(identity=dados['username'], expires_delta=timedelta(minutes=10))
            return {"access_token": token_de_acesso}, 200
        else:
            return {"message": "Username or password is incorrect"}, 401
        

