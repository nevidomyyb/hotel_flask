from flask_restful import Resource, reqparse

from models.usuario import UserModel


def getarguments():
    argumentos = reqparse.RequestParser()
    

class Usuario(Resource):
    def get(self, database, user_id):
        usuario = UserModel.find_user(user_id, database)
        if usuario:
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
        return {"message": "user not found"}, 404
    
class UsuarioRegistro(Resource):
    def post(self, database):
        atributos = reqparse.RequestParser()
        atributos.add_argument("username", type=str, required=True, help="can not be empty")
        atributos.add_argument("password", type=str, required=True, help="can not be empty")
        atributos.add_argument("first_name", type=str, required=True, help="can not be empty")
        atributos.add_argument("last_name", type=str, required=True, help="can not be empty")
        atributos.add_argument("mail", type=str, required=True, help="can not be empty")
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
        if not UserModel.verify_mail(dados['mail']): return {"message": "the provided email is invalid"}, 400
        
        #encrypt the password to save in database
        dados['password'] = UserModel.encrypt_password(dados['password'])
       
        new_id = UserModel.get_new_id(database)
        user = UserModel(new_id, **dados)
        user.save_user(database)
        user = UserModel.find_user(new_id, database)
        return user.json(), 201