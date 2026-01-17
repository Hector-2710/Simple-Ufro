import asyncio
import httpx
from app.core.config import settings

# Since we are running inside docker or host, we need the URL.
# If running inside docker 'app' service, localhost:8000 is fine.
# If running from host, localhost:8000 is fine if mapped.
# Let's assume this script runs inside the container for internal access.

BASE_URL = "http://localhost:8000/api/v1"

async def verify():
    print("🔍 Starting Verification Flow...")
    
    async with httpx.AsyncClient() as client:
        # 1. Login
        print("\n🔐 1. Testing Login...")
        response = await client.post(
            f"{BASE_URL}/access-token",
            data={"username": "student@ufro.cl", "password": "password123"}
        )
        if response.status_code != 200:
            print(f"❌ Login Failed: {response.text}")
            return
        
        token_data = response.json()
        token = token_data["access_token"]
        print("✅ Login Success! Token obtained.")
        
        auth_headers = {"Authorization": f"Bearer {token}"}

        # 2. Get Grades (First Hit - DB)
        print("\n📝 2. Testing Grades (DB Hit)...")
        start = asyncio.get_event_loop().time()
        response = await client.get(f"{BASE_URL}/academic/grades", headers=auth_headers)
        end = asyncio.get_event_loop().time()
        
        if response.status_code != 200:
            print(f"❌ Get Grades Failed: {response.text}")
        else:
            data = response.json()
            print(f"✅ Grades Fetched ({len(data)} items). Time: {end - start:.4f}s")
            if data:
                print(f"   Sample: {data[0].get('subject_name', 'No Name')} - {data[0].get('value')}")
            else:
                print("   ⚠️ No grades found (Did you seed?)")

        # 3. Get Grades (Second Hit - Cache)
        print("\n🚀 3. Testing Grades Cache (Redis Hit)...")
        start = asyncio.get_event_loop().time()
        response = await client.get(f"{BASE_URL}/academic/grades", headers=auth_headers)
        end = asyncio.get_event_loop().time()
        
        if response.status_code == 200:
             print(f"✅ Grades Fetched (Cache). Time: {end - start:.4f}s")
             # Ideally time should be lower, but in a small local env it might be similar.

        # 4. Get Schedule
        print("\n📅 4. Testing Schedule...")
        response = await client.get(f"{BASE_URL}/academic/schedule", headers=auth_headers)
        if response.status_code == 200:
             data = response.json()
             print(f"✅ Schedule Fetched ({len(data)} items).")
             if data:
                 print(f"   Sample: {data[0].get('day')} - {data[0].get('subject_name')}")
        else:
             print(f"❌ Get Schedule Failed: {response.text}")

        # 5. Get Subjects
        print("\nbooks 5. Testing Student Subjects...")
        response = await client.get(f"{BASE_URL}/academic/subjects", headers=auth_headers)
        if response.status_code == 200:
             data = response.json()
             print(f"✅ Subjects Fetched ({len(data)} items).")
        else:
             print(f"❌ Get Subjects Failed: {response.text}")
             
    print("\n✨ Verification Complete!")

if __name__ == "__main__":
    asyncio.run(verify())
