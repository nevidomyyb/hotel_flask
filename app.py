from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from sqlalchemy.orm.session import close_all_sessions

from resources.hotel import Hoteis, Hotel
from resources.usuario import UserLogin, Usuario, UsuarioRegistro

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Pedro123.321@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_BINDS = {
    "alternative": "postgresql://postgres:Pedro123.321@localhost/flask1",
}
app.config['JWT_SECRET_KEY'] = 'DoNGkdjkjS1LÇAMZMSLD23KOAAS'
api = Api(app)
jwt = JWTManager(app)

api.add_resource(Hoteis, '/<string:database>/hoteis/')
api.add_resource(Hotel, '/<string:database>/hoteis/<int:hotel_id>/')
api.add_resource(Usuario, '/<string:database>/usuarios/<int:user_id>/')
api.add_resource(UsuarioRegistro, '/<string:database>/usuarios/')
api.add_resource(UserLogin, '/<string:database>/login/')

@app.before_request
def close_all_sessions_app():
    close_all_sessions()

if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug=True)