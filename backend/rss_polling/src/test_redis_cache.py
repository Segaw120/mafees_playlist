import asyncio
import redis
import json
from datetime import datetime
from loguru import logger

class RedisCacheTest:
    def __init__(self):
        self.redis = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
        
    async def run_tests(self):
        print("\n🔍 Testing Redis Cache Behavior")
        
        # Test 1: Check existing articles
        print("\n📊 Test 1: Checking existing articles in cache")
        article_keys = self.redis.keys("article:*")
        print(f"Found {len(article_keys)} articles in cache")
        
        if article_keys:
            # Sample a few articles
            print("\n📑 Sampling cached articles:")
            for key in article_keys[:3]:  # Look at first 3 articles
                article_data = self.redis.get(key)
                try:
                    article = json.loads(article_data)
                    print(f"\n🔹 Article: {key}")
                    print(f"  Title: {article.get('title', 'No title')}")
                    print(f"  URL: {article.get('url', 'No URL')}")
                    print(f"  Timestamp: {article.get('timestamp', 'No timestamp')}")
                    
                    # Check TTL
                    ttl = self.redis.ttl(key)
                    print(f"  TTL: {ttl} seconds")
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON data for key: {key}")
        
        # Test 2: Check for duplicate URLs
        print("\n📊 Test 2: Checking for duplicate URLs")
        url_count = {}
        for key in article_keys:
            try:
                article_data = json.loads(self.redis.get(key))
                url = article_data.get('url')
                if url:
                    url_count[url] = url_count.get(url, 0) + 1
            except (json.JSONDecodeError, TypeError):
                continue
        
        duplicates = {url: count for url, count in url_count.items() if count > 1}
        if duplicates:
            print("❌ Found duplicate URLs:")
            for url, count in duplicates.items():
                print(f"  URL: {url}")
                print(f"  Count: {count}")
        else:
            print("✅ No duplicate URLs found")
        
        # Test 3: Test cache operations
        print("\n📊 Test 3: Testing cache operations")
        test_article = {
            "id": "test-id",
            "title": "Test Article",
            "url": "https://test.com/article",
            "timestamp": datetime.now().isoformat()
        }
        
        # Save test article
        test_key = "article:test"
        print("Saving test article...")
        self.redis.set(test_key, json.dumps(test_article), ex=86400)
        
        # Verify it exists
        exists = self.redis.exists(test_key)
        print(f"Article exists in cache: {exists}")
        
        # Check TTL
        ttl = self.redis.ttl(test_key)
        print(f"TTL for test article: {ttl} seconds")
        
        # Clean up test article
        self.redis.delete(test_key)
        print("Test article cleaned up")

def main():
    try:
        tester = RedisCacheTest()
        asyncio.run(tester.run_tests())
    except redis.ConnectionError:
        print("❌ Could not connect to Redis. Is Redis running?")
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    main() 