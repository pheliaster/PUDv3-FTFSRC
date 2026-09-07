import run_player_data, deprecated_run
import json
import random
import time, datetime

def src_time_to_datetime(txt):
  """
      - FORMAT YYYY-MM-DD hh:mm:ss
      - POSIT  01234567890123456789
  """
  return datetime.datetime(int(txt[0:4]), int(txt[5:7]), int(txt[8:10]), int(txt[11:13]), int(txt[14:16]), int(txt[17:19]))

def time_to_text(time):
  return f"{check_time_in_text(time//60)}:{check_time_in_text(time - (time//60)*60)}"

def time_to_text_2(time):
  return f"{check_time_in_text(time//3600)}h{check_time_in_text(time//60 - (time//3600)*60)}m{check_time_in_text(time - ((time//3600)*3600 + (time//60 - (time//3600)*60)*60))}s"

def check_time_in_text(t):
  if t < 10 :
    return f"0{t}"
  else:
    return f"{t}"
  
ID_EXCEPTION_LIST = []
NAME_EXCEPTION_LIST = ["Jenna_0134", "SkittlesCat"]
CURRENT_DATE_POINT = datetime.datetime.today()
TIME_MARGIN = 1
REMOVE_RUNNER_WITHOUT_RUN = True

def process_runs(acd, trd, tpd, apf):

  deprecated_run.import_map()
  with open('deprecated-run.json', 'r', encoding='utf-8') as file:
    all_deprecated_runs_data = json.load(file)

  all_categories_data = acd
  total_runs_data = trd
  total_players_data = tpd
  all_platforms = apf

  placeholder_list = []
  rejected_runs_list = []

  for run in total_runs_data:
    run["status"]["is-deprecated"] = False
    run["status"]["deprecate-date"] = f"{datetime.datetime.today().astimezone(datetime.timezone.utc) + datetime.timedelta(days=TIME_MARGIN)}"
    if (run["status"]["status"] != "rejected" and run["status"]["status"] != "new" and run["id"] not in ID_EXCEPTION_LIST):
        if run["category"] == "7dg6l4gk" or run["category"] == "n2yg8772" or run["category"] == "wk65l5e2" :
            placeholder_list.append(run)
        elif run["category"] == "7kjp5pxk" or run["category"] == "q25q0782":
          run["status"]["deprecate-date"] = run["status"]["verify-date"]
          if run["id"] in all_deprecated_runs_data:
                run["status"]["deprecate-date"] = all_deprecated_runs_data[run["id"]]
          if ("wlewoo4l" in run["values"] and "38dooe0l" in run["values"]) or ("wl31kkv8" in run["values"] and "gnx003xn" in run["values"]) :
            placeholder_list.append(run)
        
    if run["status"]["status"] == "rejected":
      rejected_runs_list.append(run)

    #print(run)

  all_runs_data = placeholder_list
  #with open("test-data.json", "w") as file:
  #  json.dump(all_runs_data, file)
  #print(len(all_runs_data))

  placeholder_list = []
  single_run = {}

  for run in all_runs_data:
    verify_date = src_time_to_datetime(run["status"]["verify-date"])
    deprecate_date = src_time_to_datetime(run["status"]["deprecate-date"])
    if CURRENT_DATE_POINT < verify_date :
      continue
    if CURRENT_DATE_POINT > deprecate_date :
      run["status"]["is-deprecated"] = True
    if run["category"] == "7dg6l4gk":
      run["category_id"] = "7dg6l4gk" + run["values"]["ylqmzpmn"] + run["values"]["gnxvz4jl"]
    elif run["category"] == "n2yg8772":
      run["category_id"] = "n2yg8772" + run["values"]["9l774k9l"] + run["values"]["yn259g0n"]
    elif run["category"] == "wk65l5e2":
      run["category_id"] = run["values"]["onvymwrn"] + run["values"]["ql695jxl"] + run["values"]["ylpk42v8"]
    elif run["category"] == "7kjp5pxk":
      run["category_id"] = run["values"]["wlewoo4l"] + run["values"]["38dooe0l"]
    elif run["category"] == "q25q0782":
      run["category_id"] = run["values"]["wl31kkv8"] + run["values"]["gnx003xn"]
    
    single_run = {}
    single_run["position"] = 0
    single_run["run_id"] = run["id"]
    if run["category_id"] in all_categories_data[2]:
      single_run["category_name"] = all_categories_data[3][all_categories_data[2].index(run["category_id"])]
      single_run["category_id"] = all_categories_data[4][all_categories_data[2].index(run["category_id"])]
      if single_run["category_id"] in all_categories_data[2] :
        single_run["category_name"] = "UNKNOWN"
        single_run["category_id"] = "0x11111100000001"
    else:
      single_run["category_name"] = all_categories_data[1][all_categories_data[0].index(run["category_id"])]
      single_run["category_id"] = run["category_id"]
    single_run["category_run_count"] = 0
    single_run["category_true_run_count"] = 0
    single_run["time_in_format"] = time_to_text(run["times"]["primary_t"])
    single_run["time_in_seconds"] = run["times"]["primary_t"]
    single_run["placement"] = 0
    single_run["players"] = []
    for player in run["players"]:
      if player["rel"] == "user":
        single_run["players"].append(total_players_data[1][total_players_data[0].index(player["id"])])
      elif player["rel"] == "guest" and player["name"] in NAME_EXCEPTION_LIST:
        single_run["players"].append(player["name"])
      else :
        single_run["players"].append(player["name"] + "(guest)")
    single_run["platform"] = all_platforms[1][all_platforms[0].index(run["system"]["platform"])]
    single_run["verify_date"] = f"{src_time_to_datetime(run["status"]["verify-date"])}"
    single_run["verifier"] = total_players_data[1][total_players_data[0].index(run["status"]["examiner"])]
    single_run["is_deprecated"] = run["status"]["is-deprecated"]
    single_run["deprecate_date"] = f"{src_time_to_datetime(run["status"]["deprecate-date"])}"
    single_run["run_link"] = run["weblink"]
    placeholder_list.append(single_run)

  all_runs_data = sorted(placeholder_list, key=lambda r: r["time_in_seconds"])
  #with open("test-data.json", "w") as file:
  #  json.dump(all_runs_data, file)

  category_run_count = []
  category_true_run_count = []
  category_obsolete_list = []
  previous_time_list = []
  for n in all_categories_data[0]:
    category_true_run_count.append(0)
    category_run_count.append(0)
    category_obsolete_list.append([])
    previous_time_list.append(0)
  
  for run in all_runs_data:
    if not run["is_deprecated"] :
      category_run_count[all_categories_data[0].index(run["category_id"])] += 1
      category_true_run_count[all_categories_data[0].index(run["category_id"])] += 1
      if set(run["players"]) in category_obsolete_list[all_categories_data[0].index(run["category_id"])]:
        category_run_count[all_categories_data[0].index(run["category_id"])] -= 1
        run["placement"] = "obsolete"
      else:
        run["placement"] = category_run_count[all_categories_data[0].index(run["category_id"])]
        category_obsolete_list[all_categories_data[0].index(run["category_id"])].append(set(run["players"]))
      if run["time_in_seconds"] == previous_time_list[all_categories_data[0].index(run["category_id"])] and run["placement"] != "obsolete":
        run["placement"] -= 1
      previous_time_list[all_categories_data[0].index(run["category_id"])] = run["time_in_seconds"]
    else:
      run["placement"] = "deprecated"

  all_runs_data = sorted(all_runs_data, key=lambda r: r["verify_date"])
  count = 0
  unknown_deprecated_run_count = 0
  for run in all_runs_data:
    count += 1
    run["position"] = count
    run["verify_date"] = f"{run["verify_date"]}" + " UTC+0"
    run["deprecate_date"] = f"{run["deprecate_date"]}" + " UTC+0"
    if run["is_deprecated"] :
      if run["category_id"] == "0x11111100000001":
        run["deprecate_date"] += " (LOST)"
      elif run["verify_date"] == run["deprecate_date"]:
        run["deprecate_date"] += " (N/A)"
        run["category_run_count"] = "N/A"
        unknown_deprecated_run_count += 1
      else:
        pass
    else:
      run["category_run_count"] = category_run_count[all_categories_data[0].index(run["category_id"])]
    if run["category_id"] != "0x11111100000001":
      run["category_true_run_count"] = category_true_run_count[all_categories_data[0].index(run["category_id"])]

  placeholder_list = []
  for p in total_players_data[1]:
    single_player = {}
    single_player["player_name"] = p
    single_player["nationality"] = total_players_data[2][total_players_data[1].index(p)]
    single_player["total_run_count"] = 0
    single_player["total_run_time"] = 0
    single_player["total_run_time_in_format"] = ""
    single_player["players_runs"] = []
    single_player["players_runs_in_simple_format"] = []
    single_player["total_1st_place"] = 0
    single_player["total_2nd_place"] = 0
    single_player["total_3rd_place"] = 0
    single_player["1st_place_runs"] = []
    single_player["2nd_place_runs"] = []
    single_player["3rd_place_runs"] = []
    single_player["1st_place_runs_in_simple_format"] = []
    single_player["2nd_place_runs_in_simple_format"] = []
    single_player["3rd_place_runs_in_simple_format"] = []
    single_player["survivor_wrs"] = 0
    single_player["survivor_wrs_list"] = []
    single_player["survivor_wrs_list_in_simple_format"] = []
    single_player["beast_wrs"] = 0
    single_player["beast_wrs_list"] = []
    single_player["beast_wrs_list_in_simple_format"] = []
    single_player["fastest_survivor_run"] = {"time_in_seconds": 900}
    single_player["fastest_beast_run"] = {"time_in_seconds": 900}
    single_player["fastest_survivor_run_in_seconds"] = 0
    single_player["fastest_beast_run_in_seconds"] = 0
    single_player["fastest_survivor_run_in_simple_format"] = "N/A"
    single_player["fastest_beast_run_in_simple_format"] = "N/A"
    placeholder_list.append(single_player)

  for run in all_runs_data:
    for player in run["players"]:
      if player in total_players_data[1]:
        player_info = placeholder_list[total_players_data[1].index(player)]
        player_info["total_run_count"] += 1
        player_info["total_run_time"] += run["time_in_seconds"]
        player_info["players_runs"].append(run)
        player_info["players_runs_in_simple_format"].append(run["category_name"] + " at " + run["time_in_format"])
        player_info["total_run_time_in_format"] = time_to_text_2(player_info["total_run_time"])
        if run["placement"] == 1:
          player_info["total_1st_place"] += 1
          player_info["1st_place_runs"].append(run)
          player_info["1st_place_runs_in_simple_format"].append(run["category_name"] + " at " + run["time_in_format"])
        elif run["placement"] == 2:
          player_info["total_2nd_place"] += 1
          player_info["2nd_place_runs"].append(run)
          player_info["2nd_place_runs_in_simple_format"].append(run["category_name"] + " at " + run["time_in_format"])
        elif run["placement"] == 3:
          player_info["total_3rd_place"] += 1
          player_info["3rd_place_runs"].append(run)
          player_info["3rd_place_runs_in_simple_format"].append(run["category_name"] + " at " + run["time_in_format"])
        if "7dg6l4gk" in run["category_id"] or "qj70zmeq" in run["category_id"] :
          if run["placement"] == 1:
            player_info["survivor_wrs"] += 1
            player_info["survivor_wrs_list"].append(run)
            player_info["survivor_wrs_list_in_simple_format"].append(run["category_name"] + " at " + run["time_in_format"])
          if player_info["total_run_count"] <= 1 or run["time_in_seconds"] < player_info["fastest_survivor_run"]["time_in_seconds"]:
            player_info["fastest_survivor_run"] = run
            player_info["fastest_survivor_run_in_seconds"] = run["time_in_seconds"]
            player_info["fastest_survivor_run_in_simple_format"] = run["category_name"] + " at " + run["time_in_format"]
        else:
          if run["placement"] == 1:
            player_info["beast_wrs"] += 1
            player_info["beast_wrs_list"].append(run)
            player_info["beast_wrs_list_in_simple_format"].append(run["category_name"] + " at " + run["time_in_format"])
          if player_info["total_run_count"] <= 1 or run["time_in_seconds"] < player_info["fastest_beast_run"]["time_in_seconds"]:
            player_info["fastest_beast_run"] = run
            player_info["fastest_beast_run_in_seconds"] = run["time_in_seconds"]
            player_info["fastest_beast_run_in_simple_format"] = run["category_name"] + " at " + run["time_in_format"]
    run["players"] = ", ".join(run["players"])

  all_players_data = sorted(placeholder_list, key=lambda r: r["total_1st_place"], reverse=True)
  if REMOVE_RUNNER_WITHOUT_RUN :
    placeholder_list = []
    for player in all_players_data:
      if  player["total_run_count"] > 0 :
        placeholder_list.append(player)

    all_players_data = placeholder_list

  return all_runs_data, all_players_data, rejected_runs_list, unknown_deprecated_run_count

def main():
  start = time.perf_counter()

  with open('map-data.json', 'r', encoding='utf-8') as file:
      all_categories_data = json.load(file)
      
  total_data = run_player_data.main()
  all_data = process_runs(all_categories_data,total_data[0],total_data[1],total_data[2])

  print("finished formatting datas in", time.perf_counter() - start)

  #print(len(all_data[0])," - ",len(all_data[1]))
  #rnd = random.randint(0,len(all_data[0])-1)
  #print(all_data[0][rnd], rnd)
  #with open("test-data.json", "w") as file:
  #  json.dump(all_data[0], file)
  #with open("test-data.json", "w") as file:
  #  json.dump(all_data[1], file)
  
  print("total runs in main board* - total players in main board*")
  print(len(all_data[0]), " - ", len(all_data[1]))

#main()
