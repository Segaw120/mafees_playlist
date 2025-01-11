import redis
from loguru import logger
from src.config import REDIS_HOST, REDIS_PORT, REDIS_DB
import asyncio

async def clear_redis_cache():
    """Utility function to clear Redis cache"""
    try:
        # Connect to Redis
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )
        
        # Clear all keys matching article pattern
        keys = redis_client.keys("article:*")
        if keys:
            redis_client.delete(*keys)
            logger.info(f"✅ Cleared {len(keys)} articles from Redis cache")
        else:
            logger.info("Cache already empty")
            
        redis_client.close()
        
    except redis.RedisError as e:
        logger.error(f"❌ Redis error while clearing cache: {str(e)}")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(clear_redis_cache()) 