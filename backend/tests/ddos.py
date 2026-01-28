import asyncio
import aiohttp
import time

URL = "http://localhost:8000/api/products/"

cookies = {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsInJvbGUiOiJtZW1iZXIiLCJleHAiOjE3Njk0MzI4NTl9.H4SZpEirIMmuVEVjTmX8ChFAfzgh3IP3SPcZI1LvzKA"
}

headers = {
    "accept": "application/json",
    "user-agent": "Scale-Test/1.0"
}

TOTAL_REQUESTS = 100000
CONCURRENCY = 1000  # số request chạy cùng lúc (đừng set 1000 thẳng)

sem = asyncio.Semaphore(CONCURRENCY)

async def fetch(session, idx):
    async with sem:
        try:
            async with session.get(URL, headers=headers, cookies=cookies, timeout=10) as resp:
                status = resp.status
                await resp.text()
                print(f"[{idx}] status={status}")
                return status
        except Exception as e:
            print(f"[{idx}] ERROR: {e}")
            return None

async def main():
    start = time.time()

    connector = aiohttp.TCPConnector(
        limit=CONCURRENCY,
        force_close=False
    )

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [
            fetch(session, i)
            for i in range(TOTAL_REQUESTS)
        ]
        results = await asyncio.gather(*tasks)

    end = time.time()

    success = results.count(200)
    print("\n==== RESULT ====")
    print(f"Total requests : {TOTAL_REQUESTS}")
    print(f"Success (200)  : {success}")
    print(f"Time taken    : {end - start:.2f}s")
    print(f"RPS           : {TOTAL_REQUESTS / (end - start):.2f}")

if __name__ == "__main__":
    asyncio.run(main())
