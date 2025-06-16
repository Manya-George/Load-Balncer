import asyncio
import aiohttp
from collections import Counter

counter = Counter()

async def fetch(session):
	async with session.get("http://localhost:5000/home") as resp:
		json = await resp.json()
		msg = json.get("message", "")
		sid = msg.split(":")[-1].strip()
		counter[sid] += 1

async def main():
	async with aiohttp.ClientSession() as session:
		tasks = [fetch(session) for _ in range(1000)]
		await asyncio.gather(*tasks)

	for server, count in counter.items():
		print(f"{server}: {count} requests")

if __name__ == "__main__":
	asyncio.run(main())
