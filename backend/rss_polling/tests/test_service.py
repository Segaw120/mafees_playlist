import asyncio
import sys
import os
import pytest
import aiohttp
from loguru import logger

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from src.config import ARTICLES_BUFFER_SIZE
from src.feed_poller import FeedPoller
from src.redis_client import RedisClient

async def test_redis_connection():
    """Test Redis connection and basic operations"""
    logger.info("Testing Redis connection...")
    redis_client = RedisClient()
    await redis_client.setup()
    
    # Test basic operations
    test_key = "test_key"
    test_value = "test_value"
    await redis_client.redis.set(test_key, test_value)
    result = await redis_client.redis.get(test_key)
    assert result == test_value
    logger.success("Redis connection test passed")
    await redis_client.close()

async def test_feed_poller_initialization():
    """Test FeedPoller initialization and setup"""
    logger.info("Testing FeedPoller initialization...")
    
    async def mock_send_to_clients(article):
        pass
    
    poller = FeedPoller(mock_send_to_clients)
    await poller.setup()
    assert poller.redis_client is not None
    assert isinstance(poller.article_buffer, list)
    logger.success("FeedPoller initialization test passed")
    await poller.redis_client.close()

async def test_feed_fetching():
    """Test feed fetching functionality"""
    logger.info("Testing feed fetching...")
    
    async def mock_send_to_clients(article):
        pass
    
    poller = FeedPoller(mock_send_to_clients)
    await poller.setup()
    
    async with aiohttp.ClientSession() as session:
        # Test with a reliable RSS feed
        test_feed = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
        result = await poller.fetch_feed(session, test_feed)
        assert result is not None
        logger.success("Feed fetching test passed")
    await poller.redis_client.close()

async def test_article_buffer():
    """Test article buffer management"""
    logger.info("Testing article buffer management...")
    
    async def mock_send_to_clients(article):
        pass
    
    poller = FeedPoller(mock_send_to_clients)
    await poller.setup()
    
    # Clear buffer
    poller.article_buffer = []
    
    # Test article processing
    async with aiohttp.ClientSession() as session:
        test_feed = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
        await poller.process_feed(session, test_feed)
    
    assert len(poller.article_buffer) <= ARTICLES_BUFFER_SIZE
    assert all(isinstance(article, dict) for article in poller.article_buffer)
    assert all('title' in article for article in poller.article_buffer)
    logger.success("Article buffer test passed")
    await poller.redis_client.close()

async def main():
    """Run all tests"""
    logger.info("Starting comprehensive service tests...")
    
    try:
        await test_redis_connection()
        await test_feed_poller_initialization()
        await test_feed_fetching()
        await test_article_buffer()
        logger.success("All tests completed successfully!")
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 