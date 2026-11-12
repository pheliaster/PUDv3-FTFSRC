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

def check_count(value, check):
    if check == "qj70zmeq" or check == "7kjp5pxk" or check == "814gy5j1":
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
    elif check == "q6504o3l" or check == "q25q0782" or check == "z19ymjkl":
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

def check_count_in_int(value):
    if ("1" or "One") in value:
        return 1
    elif ("2" or "Two") in value:
        return 2
    elif ("3" or "Three") in value:
        return 3
    elif ("4" or "Four") in value:
        return 4
    else:
        return -1
    
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
        return "UNKWOWN"
    
def main():
    all_variables_url = ["https://www.speedrun.com/api/v1/categories/7dg6l4gk/variables","https://www.speedrun.com/api/v1/categories/n2yg8772/variables","https://www.speedrun.com/api/v1/categories/wk65l5e2/variables", "https://www.speedrun.com/api/v1/categories/zdn4m1qk/variables", "https://www.speedrun.com/api/v1/categories/7kjp5pxk/variables", "https://www.speedrun.com/api/v1/categories/q25q0782/variables"]
    all_variables = asyncio.run(collect_all_data(urls=list(all_variables_url)))   
    all_the_ids = []
    all_original_names = []
    all_changed_names = []
    all_maps_match = []
    all_count = []
    change_to_maps = ""
    text_placeholder = ""

    var = all_variables[0]
    for k0 in var[0]["values"]["values"]:
        for k1 in var[1]["values"]["values"]:
            text_placeholder = "7dg6l4gk" + k0 + k1
            all_the_ids.append(text_placeholder)
            text_placeholder = change_to_maps = var[0]["values"]["values"][f"{k0}"]["label"] + " " + var[1]["values"]["values"][f"{k1}"]["label"]
            all_original_names.append(text_placeholder)
            all_changed_names.append(text_placeholder)
            text_placeholder = check_name(change_to_maps)
            all_maps_match.append(text_placeholder)
            all_count.append(check_count_in_int(var[1]["values"]["values"][f"{k1}"]["label"]))

    var = all_variables[1]
    for k0 in var[0]["values"]["values"]:
        for k1 in var[1]["values"]["values"]:
            text_placeholder = "n2yg8772" + k0 + k1
            all_the_ids.append(text_placeholder)
            text_placeholder = change_to_maps = var[0]["values"]["values"][f"{k0}"]["label"] + " " + var[1]["values"]["values"][f"{k1}"]["label"]
            all_original_names.append(text_placeholder)
            all_changed_names.append(text_placeholder)
            text_placeholder = check_name(change_to_maps)
            all_maps_match.append(text_placeholder)
            all_count.append(check_count_in_int(var[1]["values"]["values"][f"{k1}"]["label"]))

    var = all_variables[2]
    for k0 in var[0]["values"]["values"]:
        for k1 in var[1]["values"]["values"]:
            for k2 in var[2]["values"]["values"]:
                text_placeholder = k0 + k1 + k2
                all_the_ids.append(text_placeholder)
                text_placeholder = change_to_maps = var[0]["values"]["values"][f"{k0}"]["label"] + " " + var[1]["values"]["values"][f"{k1}"]["label"] + " " + var[2]["values"]["values"][f"{k2}"]["label"]
                all_original_names.append(text_placeholder)
                text_placeholder = "(Seasonal) " + var[1]["values"]["values"][f"{k1}"]["label"] + " " + check_count(var[2]["values"]["values"][f"{k2}"]["label"], k0)
                all_changed_names.append(text_placeholder)
                text_placeholder = check_name(change_to_maps)
                all_maps_match.append(text_placeholder)
                all_count.append(check_count_in_int(var[2]["values"]["values"][f"{k2}"]["label"]))

    var = all_variables[3]
    for k0 in var[0]["values"]["values"]:
        for k1 in var[1]["values"]["values"]:
            for k2 in var[2]["values"]["values"]:
                text_placeholder = k0 + k1 + k2
                all_the_ids.append(text_placeholder)
                text_placeholder = change_to_maps = var[0]["values"]["values"][f"{k0}"]["label"] + " " + var[1]["values"]["values"][f"{k1}"]["label"] + " " + var[2]["values"]["values"][f"{k2}"]["label"]
                all_original_names.append(text_placeholder)
                text_placeholder = "(VIP) " + var[1]["values"]["values"][f"{k1}"]["label"] + " " + check_count(var[2]["values"]["values"][f"{k2}"]["label"], k0)
                all_changed_names.append(text_placeholder)
                text_placeholder = check_name(change_to_maps)
                all_maps_match.append(text_placeholder)   
                all_count.append(check_count_in_int(var[2]["values"]["values"][f"{k2}"]["label"]))            

    var = all_variables[4]
    for k0 in var[0]["values"]["values"]:
        for k1 in var[1]["values"]["values"]:
            text_placeholder = "7kjp5pxk" + k0 + k1
            all_the_ids.append(text_placeholder)
            text_placeholder = change_to_maps = var[0]["values"]["values"][f"{k0}"]["label"] + " " + var[1]["values"]["values"][f"{k1}"]["label"]
            all_original_names.append(text_placeholder)
            text_placeholder = "(OLD) " + var[0]["values"]["values"][f"{k0}"]["label"] + " " + check_count(var[1]["values"]["values"][f"{k1}"]["label"], "7kjp5pxk")
            all_changed_names.append(text_placeholder)
            text_placeholder = check_name(change_to_maps)
            all_maps_match.append(text_placeholder)
            all_count.append(check_count_in_int(var[1]["values"]["values"][f"{k1}"]["label"]))

    var = all_variables[5]
    for k0 in var[0]["values"]["values"]:
        for k1 in var[1]["values"]["values"]:
            text_placeholder = "q25q0782" + k0 + k1
            all_the_ids.append(text_placeholder)
            text_placeholder = change_to_maps = var[0]["values"]["values"][f"{k0}"]["label"] + " " + var[1]["values"]["values"][f"{k1}"]["label"]
            all_original_names.append(text_placeholder)
            text_placeholder = "(OLD) " + var[0]["values"]["values"][f"{k0}"]["label"] + " " + check_count(var[1]["values"]["values"][f"{k1}"]["label"], "q25q0782")
            all_changed_names.append(text_placeholder)
            text_placeholder = check_name(change_to_maps)
            all_maps_match.append(text_placeholder)
            all_count.append(check_count_in_int(var[1]["values"]["values"][f"{k1}"]["label"]))

    all_the_ids.append("")
    all_original_names.append("UNKNOWN")
    all_changed_names.append("UNKNOWN")
    all_maps_match.append("UNKNOWN")
    all_count.append(-1)
    exception_names = ["Jenna_0134", "SkittlesCat", "Newbe", "CWANIACZKA", "nfinitiy","Desgxnsz"]

    with open("x-redate-requested-runs.json", 'r', encoding='utf-8') as file:
      all_redate_needed_runs = json.load(file)
    deprecated_runs = all_redate_needed_runs[0]
    revalidated_runs = all_redate_needed_runs[1]

    all_extras_data = []
    all_extras_data.append(all_the_ids)
    all_extras_data.append(all_original_names)
    all_extras_data.append(all_changed_names)
    all_extras_data.append(all_maps_match)
    all_extras_data.append(all_count)
    all_extras_data.append(deprecated_runs)
    all_extras_data.append(revalidated_runs)
    all_extras_data.append(exception_names)

    with open("x-extras-data.json", "w") as file:
        json.dump(all_extras_data, file)
    print("finished exporting extras")

#main()
#Remember to run this code once in a while every time a new map is added to the roster !