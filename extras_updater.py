import asyncio
import aiohttp
import json
import time

start = time.perf_counter()

async def fetch_one(session: aiohttp.ClientSession, url: str):
    while True:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                json_data = await response.json()
                return json_data.get("data")
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"failed | reason : {e} | at {time.perf_counter() - start} | retrying ...")
            await asyncio.sleep(1)


async def fetch_batch(session: aiohttp.ClientSession, ids):
    tasks = [fetch_one(session, i) for i in ids]
    return await asyncio.gather(*tasks)

async def collect_all_data(urls: list[str] | None = None):
    async with aiohttp.ClientSession() as session:
        results = await fetch_batch(session, urls)
        return results

def seasonal_naming(value, check):
    if check == "qj70zmeq" or check == "7kjp5pxk":
        match value:
            case "1":
                return "One Player"
            case "2":
                return "Two Players"
            case "3":
                return "Three Players"
            case "4":
                return "Four Players"
            case _:
                return "Unknown"
    elif check == "q6504o3l" or check == "q25q0782":
        match value:
            case "1":
                return "One Capture"
            case "2":
                return "Two Captures"
            case "3":
                return "Three Captures"
            case "4":
                return "Four Captures"
            case _:
                return "Unknown"

def check_name(value: str):
    if "Facility_0" in value:
        return "Facility_0"
    elif "Homestead" in value:
        return "Homestead"
    elif "Airport" in value:
        return "Airport"
    elif "Abandoned Prison" in value:
        return "Abandoned Prison"
    elif "Library" in value:
        return "Library"
    elif "Abandoned Facility" in value:
        return "Abandoned Facility Optimus"
    elif "Forgotten Facility" in value:
        return "Abandoned Facility Optimus"
    elif "Nuclear Power Plant" in value:
        return "Nuclear Power Plant"
    elif "Haunted Mansion" in value:
        return "Haunted Mansion"
    elif "Backrooms" in value:
        return "Backrooms (Halloween)"
    elif "Toy Workshop" in value:
        return "Toy Workshop (Christmas)"
    elif "School" in value:
        return "School"
    elif "Sewer Treatment Plant" in value:
        return "Sewer Treatment Plant"
    elif "Laboratory Complex" in value:
        return "Laboratory Complex"
    elif "Arcade" in value:
        return "Arcade"
    elif "Arctic Station" in value:
        return "Arctic Station"
    elif "Sanctuary Zoo" in value:
        return "Sanctuary Zoo"
    elif "Spaceship" in value:
        return "Spaceship"
    elif "Ghost Town" in value:
        return "Ghost Town"
    elif "Shopping Center" in value:
        return "Shopping Center"
    else :
        return value
    
def main():
    all_variables_url = ["https://www.speedrun.com/api/v1/categories/7dg6l4gk/variables","https://www.speedrun.com/api/v1/categories/n2yg8772/variables","https://www.speedrun.com/api/v1/categories/wk65l5e2/variables", "https://www.speedrun.com/api/v1/categories/7kjp5pxk/variables", "https://www.speedrun.com/api/v1/categories/q25q0782/variables"]
    all_extras_data = asyncio.run(collect_all_data(urls=list(all_variables_url)))   
    ids = []
    names = []
    old_ids = []
    old_names = []
    old_to_new_match = []
    text_placeholder = ""

    var = all_extras_data[0]
    for k1 in var[0]["values"]["values"]:
        for k2 in var[1]["values"]["values"]:
            text_placeholder = "7dg6l4gk" + k1 + k2
            ids.append(text_placeholder)
            text_placeholder = var[0]["values"]["values"][f"{k1}"]["label"] + " " + var[1]["values"]["values"][f"{k2}"]["label"]
            names.append(text_placeholder)

    var = all_extras_data[1]
    for k1 in var[0]["values"]["values"]:
        for k2 in var[1]["values"]["values"]:
            text_placeholder = "n2yg8772" + k1 + k2
            ids.append(text_placeholder)
            text_placeholder = var[0]["values"]["values"][f"{k1}"]["label"] + " " + var[1]["values"]["values"][f"{k2}"]["label"]
            names.append(text_placeholder)

    var = all_extras_data[2]
    for k1 in var[0]["values"]["values"]:
        for k2 in var[1]["values"]["values"]:
            for k3 in var[2]["values"]["values"]:
                text_placeholder = k1 + k2 + k3
                ids.append(text_placeholder)
                text_placeholder = var[1]["values"]["values"][f"{k2}"]["label"] + " " + seasonal_naming(var[2]["values"]["values"][f"{k3}"]["label"], k1)
                names.append(text_placeholder)

    var = all_extras_data[3]
    for k1 in var[0]["values"]["values"]:
        for k2 in var[1]["values"]["values"]:
            text_placeholder = k1 + k2
            old_ids.append(text_placeholder)
            text_placeholder = check_name(var[0]["values"]["values"][f"{k1}"]["label"]) + " " + seasonal_naming(var[1]["values"]["values"][f"{k2}"]["label"], "7kjp5pxk")
            old_names.append(text_placeholder)

    var = all_extras_data[4]
    for k1 in var[0]["values"]["values"]:
        for k3 in var[2]["values"]["values"]:
            text_placeholder = k1 + k3
            old_ids.append(text_placeholder)
            text_placeholder = check_name(var[0]["values"]["values"][f"{k1}"]["label"]) + " " + seasonal_naming(var[2]["values"]["values"][f"{k3}"]["label"], "q25q0782")
            old_names.append(text_placeholder)

    for n in old_names:
        if n in names:
            old_to_new_match.append(ids[names.index(n)])
        else:
            old_to_new_match.append(old_ids[old_names.index(n)])

    exception_names = ["Jenna_0134", "SkittlesCat", "Newbe", "CWANIACZKA"]

    with open("x-redate-requested-runs.json", 'r', encoding='utf-8') as file:
      all_redate_needed_runs = json.load(file)
    deprecated_runs = all_redate_needed_runs[0]
    revalidated_runs = all_redate_needed_runs[1]

    all_extras_data = []
    all_extras_data.append(ids)
    all_extras_data.append(names)
    all_extras_data.append(old_ids)
    all_extras_data.append(old_names)
    all_extras_data.append(old_to_new_match)
    all_extras_data.append(deprecated_runs)
    all_extras_data.append(revalidated_runs)
    all_extras_data.append(exception_names)

    with open("x-extras-data.json", "w") as file:
        json.dump(all_extras_data, file)
    print("finished exporting extras")

#main()
#Remember to run this code once in a while every time a new map is added to the roster !