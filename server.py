from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_jwt_extended import JWTManager
from app.schema import schema
from flask_mongoengine import MongoEngine
import datetime


app = Flask(__name__)
app.debug = True
app.config['MONGODB_SETTINGS'] = {
    "db": "GraphQL",
    "host": "host",
    "username": "admin",
    "password": "aCt8HMn2x86VQf9A"
}
app.config['JWT_SECRET_KEY'] = "\x80i\xbb\xaeULT|\x91\xb85gD\xe1\xb9\x91\x13\xc0\xbe\xe8TO\xed\x1e"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=6)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=1)
CORS(app)
db = MongoEngine(app)
jwt = JWTManager(app)


app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)


if __name__ == '__main__':
    app.run(debug=True)
