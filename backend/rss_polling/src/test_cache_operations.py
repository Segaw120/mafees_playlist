import asyncio
import redis
import json
from datetime import datetime, timedelta
import uuid
from loguru import logger

class CacheOperationsTest:
    def __init__(self):
        self.redis = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
        self.test_articles = []

    def create_test_article(self, index: int) -> dict:
        """Create a test article with unique data"""
        return {
            "id": str(uuid.uuid4()),
            "title": f"Test Article {index}",
            "content": f"Content for article {index}",
            "source": "test.com",
            "timestamp": (datetime.now() + timedelta(minutes=index)).isoformat(),
            "url": f"https://test.com/article-{index}",
            "imageUrl": f"https://test.com/image-{index}.jpg",
            "categories": [{"term": "Test"}]
        }

    async def test_cache_operations(self):
        print("\n🔍 Starting Cache Operations Tests")

        try:
            # Test 1: Basic Save and Retrieve
            print("\n📊 Test 1: Basic Save and Retrieve")
            test_article = self.create_test_article(1)
            key = f"article:{test_article['url']}"

            # Save article
            print("Saving article...")
            self.redis.set(key, json.dumps(test_article), ex=86400)  # 24 hour TTL

            # Immediate retrieve
            print("Retrieving article...")
            retrieved = self.redis.get(key)
            retrieved_article = json.loads(retrieved) if retrieved else None

            if retrieved_article and retrieved_article['id'] == test_article['id']:
                print("✅ Article successfully saved and retrieved")
            else:
                print("❌ Article retrieval failed")

            # Test 2: TTL Verification
            print("\n📊 Test 2: TTL Verification")
            ttl = self.redis.ttl(key)
            print(f"TTL for test article: {ttl} seconds")
            if 86300 <= ttl <= 86400:  # Allow for slight time difference
                print("✅ TTL correctly set to ~24 hours")
            else:
                print(f"❌ Unexpected TTL value: {ttl}")

            # Test 3: Existence Checks
            print("\n📊 Test 3: Existence Checks")
            exists = self.redis.exists(key)
            print(f"Article exists check: {exists}")
            
            # Non-existent article check
            fake_key = "article:nonexistent"
            fake_exists = self.redis.exists(fake_key)
            print(f"Non-existent article check: {fake_exists}")

            if exists and not fake_exists:
                print("✅ Existence checks working correctly")
            else:
                print("❌ Existence checks not working as expected")

            # Test 4: Multiple Articles
            print("\n📊 Test 4: Multiple Articles Operation")
            # Create and save multiple articles
            for i in range(5):
                article = self.create_test_article(i)
                self.test_articles.append(article)
                key = f"article:{article['url']}"
                self.redis.set(key, json.dumps(article), ex=86400)

            # Verify all articles
            all_exist = True
            for article in self.test_articles:
                key = f"article:{article['url']}"
                if not self.redis.exists(key):
                    all_exist = False
                    print(f"❌ Article {article['url']} not found in cache")

            if all_exist:
                print("✅ All test articles successfully cached")
            else:
                print("❌ Some articles missing from cache")

            # Test 5: Cache Overwrite
            print("\n📊 Test 5: Cache Overwrite Test")
            original_article = self.test_articles[0]
            modified_article = original_article.copy()
            modified_article['title'] = "Modified Title"
            key = f"article:{original_article['url']}"

            # Save modified version
            self.redis.set(key, json.dumps(modified_article), ex=86400)
            
            # Retrieve and verify
            retrieved = json.loads(self.redis.get(key))
            if retrieved['title'] == "Modified Title":
                print("✅ Cache overwrite successful")
            else:
                print("❌ Cache overwrite failed")

        finally:
            # Cleanup
            print("\n🧹 Cleaning up test data...")
            for article in self.test_articles:
                self.redis.delete(f"article:{article['url']}")
            self.redis.delete(key)
            print("✅ Cleanup complete")

def main():
    try:
        tester = CacheOperationsTest()
        asyncio.run(tester.test_cache_operations())
    except redis.ConnectionError:
        print("❌ Could not connect to Redis. Is Redis running?")
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        logger.exception("Test failed with error:")

if __name__ == "__main__":
    main() 