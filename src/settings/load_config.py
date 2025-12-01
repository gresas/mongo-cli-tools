import yaml
from logging.config import dictConfig
from logging import getLogger
from os import getenv
from dependency_injector.providers import Configuration


logger = getLogger(__name__)
app_config = Configuration("app_config")


def setup_logging():
    with open("./settings/logging.yml", "r") as f:
        dictConfig(yaml.full_load(f))

    env_settings = {
        "mongo": {
            "uri": getenv("MONGO_URI"),
            "db_name": getenv("MONGO_DB"),
            "collection": getenv("MONGO_COLLECTION")
        },
        "redis": {
            "host": getenv("REDIS_HOST"),
            "port": getenv("REDIS_PORT")
        }
    }

    app_config.override(env_settings)
