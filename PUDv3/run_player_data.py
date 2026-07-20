import time, datetime
import asyncio
import aiohttp
import openpyxl as pxl

start = time.perf_counter()

BATCH_SIZE = 20    # how many URLs to fetch concurrently per round
RETRY_DELAY = 1    # fixed seconds to wait between retries


async def fetch_one(session: aiohttp.ClientSession, url: str):
    """Fetch a single url, retrying forever until it succeeds. Returns data only."""
    while True:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                json_data = await response.json()
                return json_data.get("data")
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"{url} failed | reason : {e} | at {time.perf_counter() - start} | retrying ...")
            await asyncio.sleep(RETRY_DELAY)


async def fetch_batch(session: aiohttp.ClientSession, urls):
    """Fetch a batch of urls concurrently."""
    tasks = [fetch_one(session, i) for i in urls]
    return await asyncio.gather(*tasks)


def is_empty(data) -> bool:
    """Empty-but-200 case"""
    if data is None:
        return True
    if isinstance(data, (list, dict, str)) and len(data) == 0:
        return True
    return False


async def collect_all_data(mode: str = "known", base_url: str | None = None, url_list: list[str] | None = None,):
    """
    Single entry point with a mode switch:
      - "known": fetch a bunch of link in big patch, must be already known to have data
      - "expanding": fetch the unknown, expanding list of ids until it hits the empty data zone
    """
    results = []

    async with aiohttp.ClientSession() as session:

        if mode == "known":
            results = await fetch_batch(session, url_list)

        if mode == "expanding":
            current_offset = 0
            stop = False
            while not stop:
                batch_urls = [base_url.format(current_offset + i * 20) for i in range(BATCH_SIZE)]
                batch_results = await fetch_batch(session, batch_urls)

                for data in batch_results:
                    if is_empty(data):
                        stop = True
                        break
                    results.append(data)

                current_offset += BATCH_SIZE * 20

    return results

#credits to Claude cus I ain't understanding how this works (beside where to fix it ofc), honestly this usage of AI isn't that bad since I'm learning something?

def main():
    BASE_URL = "https://www.speedrun.com/api/v1/runs?game=46wpg3dr&offset={}"
    all_datas = asyncio.run(collect_all_data(mode="expanding", base_url=BASE_URL))
    all_runs = []
    for i in all_datas:
        for j in i:
            all_runs.append(j)
    print("finished collecting all runs' data in", time.perf_counter() - start)
    all_reg_players_uri = {"https://www.speedrun.com/api/v1/users/8dgrz6g8"}
    for run in all_runs:
        for i in run["players"]:
            if i["rel"] != "guest":
                all_reg_players_uri.add(i["uri"])
    all_reg_players_uri = list(all_reg_players_uri)
    all_reg_players_data = asyncio.run(collect_all_data(mode="known", url_list=all_reg_players_uri))
    print("finished collecting all players' data in", time.perf_counter() - start)
    return all_runs, all_reg_players_data

#main()