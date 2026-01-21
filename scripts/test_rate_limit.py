import httpx
import asyncio

async def test_rate_limit():
    url = "http://localhost:8000/api/v1/login/access-token"
    print(f"Testing rate limit on {url}...")
    
    for i in range(1, 10):
        try:
            response = httpx.post(url, data={"username": "test", "password": "test"})
            print(f"Request {i}: Status {response.status_code}")
            if response.status_code == 429:
                print("✅ Rate limit reached as expected!")
                return
        except Exception as e:
            print(f"Error: {e}")
            break
            
    print("❌ Rate limit NOT reached.")

if __name__ == "__main__":
    asyncio.run(test_rate_limit())
