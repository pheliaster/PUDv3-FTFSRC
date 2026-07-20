import asyncio
import aiohttp
import json

async def fetch_one(session: aiohttp.ClientSession, url: str):
    while True:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                json_data = await response.json()
                return json_data.get("data")
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            #print(f"failed | reason : {e} | at {time.perf_counter() - start} | retrying ...")
            await asyncio.sleep(1)


async def fetch_batch(session: aiohttp.ClientSession, ids):
    tasks = [fetch_one(session, i) for i in ids]
    return await asyncio.gather(*tasks)

async def collect_all_data(urls: list[str] | None = None):
    async with aiohttp.ClientSession() as session:
        results = await fetch_batch(session, urls)
        return results

def main():
    all_variables_url = ["https://www.speedrun.com/api/v1/categories/7dg6l4gk/variables","https://www.speedrun.com/api/v1/categories/n2yg8772/variables","https://www.speedrun.com/api/v1/categories/wk65l5e2/variables"]
    all_variables_data = asyncio.run(collect_all_data(urls=list(all_variables_url)))   
    with open("map-data.json", "w") as file:
        json.dump(all_variables_data, file)
    print("finished updating all variables' data")

#Remember to run this code once in a while verytime a new map is added to the roster !