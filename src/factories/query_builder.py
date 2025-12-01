from tools._query_builder import MongoQueryBuilder
from dependency_injector.providers import Singleton
from settings.load_config import app_config


QueryBuilder = Singleton(
    MongoQueryBuilder,
    uri=app_config.mongo.uri,
    db_name=app_config.mongo.db_name,
    collection=app_config.mongo.collection
)
