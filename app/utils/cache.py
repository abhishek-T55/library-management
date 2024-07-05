import logging
import redis
from app.core.config import config

logger = logging.getLogger("redis")

redis_client = redis.StrictRedis(
    host=config.redis.host,
    port=config.redis.port,
    db=config.redis.db,
    password=config.redis.password,
    decode_responses=True
)

if redis_client.ping():
    logger.info("Redis Initialized...")