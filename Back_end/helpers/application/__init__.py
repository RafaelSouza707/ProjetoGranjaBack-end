import os
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from helpers.cache import cache
from dotenv import load_dotenv

from helpers.database import db
from helpers.error_handlers import register_error_handlers

load_dotenv()

app = Flask(__name__)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Cache em memória
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

cache.init_app(app)

db.init_app(app)

migrate = Migrate(app, db)

register_error_handlers(app)

import models

api = Api(app)