from flask import Flask
from pymongo import MongoClient



host = "mongo"  # service name as defined in the docker-compose.yml
port = 27017
username = "root"
password = "password"
database = "server_database"

app = Flask(__name__)


client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/?authSource=admin")
db = client[database]

def register_blueprints():
    from .item_routes import item_api
    from .user_routes import user_api
    app.register_blueprint(item_api)
    app.register_blueprint(user_api)

register_blueprints()

if __name__ == "__main__":
    app.run()
