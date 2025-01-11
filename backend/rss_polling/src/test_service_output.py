import aiohttp
import asyncio
import json
from datetime import datetime

async def test_service():
    print("\n🔍 Testing RSS Polling Service Output")
    
    async with aiohttp.ClientSession() as session:
        # Test initial articles endpoint
        try:
            print("\n📡 Testing /articles endpoint...")
            async with session.get('http://localhost:8000/articles') as response:
                data = await response.json()
                print(f"Status Code: {response.status}")
                
                if 'articles' in data:
                    print(f"\nFound {len(data['articles'])} articles")
                    
                    # Print details of first article
                    if data['articles']:
                        article = data['articles'][0]
                        print("\n📰 Sample Article Format:")
                        print(json.dumps(article, indent=2))
                        
                        # Specifically check date format
                        if 'timestamp' in article:
                            print("\n⏰ Timestamp Analysis:")
                            timestamp = article['timestamp']
                            print(f"Raw timestamp: {timestamp}")
                            try:
                                # Try parsing the timestamp
                                parsed_date = datetime.fromisoformat(timestamp)
                                print(f"Parsed date: {parsed_date}")
                                print(f"Timezone info: {parsed_date.tzinfo}")
                            except ValueError as e:
                                print(f"❌ Error parsing timestamp: {e}")
                        
                        # Check categories format
                        if 'categories' in article:
                            print("\n🏷️ Categories Analysis:")
                            print(json.dumps(article['categories'], indent=2))
                else:
                    print("❌ No articles found in response")
                    print("Response data:", json.dumps(data, indent=2))
        
        except aiohttp.ClientError as e:
            print(f"❌ Error connecting to service: {e}")
        
        # Test SSE stream
        try:
            print("\n📡 Testing /stream endpoint (waiting for updates)...")
            async with session.get('http://localhost:8000/stream') as response:
                # Wait for one SSE message
                async for line in response.content:
                    if line.startswith(b'data: '):
                        data = json.loads(line[6:].decode())  # Skip "data: " prefix
                        print("\n📨 Received SSE Update:")
                        print(json.dumps(data, indent=2))
                        break  # Exit after first message
        
        except aiohttp.ClientError as e:
            print(f"❌ Error connecting to SSE stream: {e}")

if __name__ == "__main__":
    asyncio.run(test_service()) 