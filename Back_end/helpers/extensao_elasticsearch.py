from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch

db = SQLAlchemy()
es = Elasticsearch("http://localhost:9200")