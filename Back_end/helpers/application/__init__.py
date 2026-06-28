import os
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from dotenv import load_dotenv

from helpers.cache import cache
from helpers.database import db
from helpers.error_handlers import register_error_handlers

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST', 'localhost')}"
    f":{os.getenv('DB_PORT', '5432')}"
    f"/{os.getenv('DB_NAME')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = (
    f"redis://{os.getenv('CACHE_REDIS_HOST', 'localhost')}:"
    f"{os.getenv('CACHE_REDIS_PORT', '6379')}/"
    f"{os.getenv('CACHE_REDIS_DB', '0')}"
)

app.config["CACHE_DEFAULT_TIMEOUT"] = int(
    os.getenv("CACHE_DEFAULT_TIMEOUT", "300")
)

cache.init_app(app)

db.init_app(app)

migrate = Migrate(app, db)

register_error_handlers(app)

import models

api = Api(app)