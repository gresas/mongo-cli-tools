from dependency_injector.providers import Singleton
from rest_clients.redis_client import RedisClient


from settings.load_config import app_config

RedisClientSingleton = Singleton(
    RedisClient,
    config={
        "host": app_config.redis.host(),
        "port": app_config.redis.port()
    }
)
