from flask import Flask
from flask_restful import Api

from resources.hotel import Hoteis, Hotel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Pedro123.321@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_BINDS = {
    "alternative": "postgresql://postgres:Pedro123.321@localhost/flask1",
}
api = Api(app)

api.add_resource(Hoteis, '/<string:database>/hoteis/')
api.add_resource(Hotel, '/<string:database>/hoteis/<int:hotel_id>/')

if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug=True)