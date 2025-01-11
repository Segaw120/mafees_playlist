import asyncio
import json
from datetime import datetime, timedelta
import uuid
from typing import List, Dict
from loguru import logger

class BufferTest:
    def __init__(self):
        self.article_buffer = []
        self.buffer_size = 15

    def create_test_article(self, timestamp_offset: int = 0) -> Dict:
        """Create a test article with a specific timestamp offset (in minutes)"""
        base_time = datetime.now() + timedelta(minutes=timestamp_offset)
        return {
            "id": str(uuid.uuid4()),
            "title": f"Test Article {timestamp_offset}",
            "content": "Test content",
            "source": "test.com",
            "timestamp": base_time.isoformat(),
            "url": f"https://test.com/article-{timestamp_offset}",
            "imageUrl": "https://test.com/image.jpg",
            "categories": [{"term": "Test"}]
        }

    async def test_buffer_operations(self):
        print("\n🔍 Testing Buffer Management")

        # Test 1: Basic Buffer Operations
        print("\n📊 Test 1: Basic Buffer Operations")
        
        # Add articles with different timestamps
        for i in range(20):  # Try to add more than buffer size
            article = self.create_test_article(timestamp_offset=-i)
            self.article_buffer.append(article)
            self.article_buffer.sort(
                key=lambda x: datetime.fromisoformat(x["timestamp"]), 
                reverse=True
            )
            self.article_buffer = self.article_buffer[:self.buffer_size]
            
            print(f"Buffer size after adding article {i+1}: {len(self.article_buffer)}")

        # Verify buffer size
        print(f"\nFinal buffer size: {len(self.article_buffer)}")
        print("Latest article timestamp:", self.article_buffer[0]["timestamp"])
        print("Oldest article timestamp:", self.article_buffer[-1]["timestamp"])

        # Test 2: Check for Duplicates in Buffer
        print("\n📊 Test 2: Checking for Duplicates in Buffer")
        url_count = {}
        id_count = {}
        
        for article in self.article_buffer:
            url = article["url"]
            article_id = article["id"]
            
            url_count[url] = url_count.get(url, 0) + 1
            id_count[article_id] = id_count.get(article_id, 0) + 1

        # Report duplicates
        url_duplicates = {url: count for url, count in url_count.items() if count > 1}
        id_duplicates = {id_: count for id_, count in id_count.items() if count > 1}

        if url_duplicates:
            print("\n❌ Found duplicate URLs in buffer:")
            for url, count in url_duplicates.items():
                print(f"  URL: {url}")
                print(f"  Count: {count}")
        else:
            print("✅ No duplicate URLs in buffer")

        if id_duplicates:
            print("\n❌ Found duplicate IDs in buffer:")
            for id_, count in id_duplicates.items():
                print(f"  ID: {id_}")
                print(f"  Count: {count}")
        else:
            print("✅ No duplicate IDs in buffer")

        # Test 3: Buffer Sorting
        print("\n📊 Test 3: Testing Buffer Sorting")
        timestamps = [datetime.fromisoformat(article["timestamp"]) 
                     for article in self.article_buffer]
        
        is_sorted = all(timestamps[i] >= timestamps[i+1] 
                       for i in range(len(timestamps)-1))
        
        if is_sorted:
            print("✅ Buffer is properly sorted (newest to oldest)")
        else:
            print("❌ Buffer sorting error detected")
            print("\nTimestamp order:")
            for i, ts in enumerate(timestamps):
                print(f"{i+1}. {ts.isoformat()}")

        # Test 4: Buffer Update Simulation
        print("\n📊 Test 4: Testing Buffer Updates")
        
        # Try to add a duplicate article
        duplicate_article = self.article_buffer[0].copy()
        duplicate_article["id"] = str(uuid.uuid4())  # New ID but same URL
        
        original_size = len(self.article_buffer)
        self.article_buffer.append(duplicate_article)
        self.article_buffer.sort(
            key=lambda x: datetime.fromisoformat(x["timestamp"]), 
            reverse=True
        )
        self.article_buffer = self.article_buffer[:self.buffer_size]
        
        print(f"Buffer size after adding duplicate: {len(self.article_buffer)}")
        if len(self.article_buffer) > original_size:
            print("❌ Buffer accepted duplicate article")
        else:
            print("✅ Buffer maintained size limit")

def main():
    try:
        tester = BufferTest()
        asyncio.run(tester.test_buffer_operations())
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    main() 