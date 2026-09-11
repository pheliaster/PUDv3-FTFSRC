import data_getter
import json
import time, datetime
from copy import deepcopy

NOW_DATE = datetime.datetime.today()
TIME_MARGIN_IN_HOURS = 6

def src_time_to_datetime(txt):
  """
      - FORMAT YYYY-MM-DD hh:mm:ss
      - POSIT  01234567890123456789
  """
  return datetime.datetime(int(txt[0:4]), int(txt[5:7]), int(txt[8:10]), int(txt[11:13]), int(txt[14:16]), int(txt[17:19]))

def check_time_in_text(t):
  if t < 10 :
    return f"0{t}"
  else:
    return f"{t}"

def time_to_text(time):
  return f"{check_time_in_text(time//60)}:{check_time_in_text(time - (time//60)*60)}"

def time_to_text_2(time):
  return f"{check_time_in_text(time//3600)}h{check_time_in_text(time//60 - (time//3600)*60)}m{check_time_in_text(time - ((time//3600)*3600 + (time//60 - (time//3600)*60)*60))}s"

def create_new_reworked_run_data(run):
    """
      - "status" can only be in 6 states ["pending", "verified", "rejected", "deprecated", "orphaned", "ignored"]
    """
    single_run = {}
    single_run["position"] = 0
    single_run["run_id"] = run["id"]
    single_run["category_name"] = ""
    single_run["category_id"] = ""
    single_run["time_in_format"] = time_to_text(run["times"]["primary_t"])
    single_run["time_in_seconds"] = run["times"]["primary_t"]
    single_run["placement"] = 0
    single_run["players"] = []
    single_run["players_in_format"] = ""
    single_run["platform"] = ""
    single_run["status"] = []
    single_run["verify_date"] = None
    single_run["verifier"] = None
    single_run["rejected_reason"] = None
    single_run["validated_date"] = run["date"] + "T00:00:00Z"
    single_run["deprecated_date"] = f"{NOW_DATE.astimezone(tz=datetime.timezone.utc)}"
    single_run["run_link"] = run["weblink"]
    return single_run

def create_new_reworked_player_data(player):
    single_player = {}
    single_player["player_id"] = ""
    single_player["player_name"] = player
    single_player["nationality"] = ""
    single_player["total_run_count"] = 0
    single_player["total_run_time"] = 0
    single_player["total_run_time_in_format"] = ""
    single_player["players_runs"] = []
    single_player["players_runs_in_simple_format"] = []
    single_player["highest_wr_count"] = 0
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
    return single_player


def process_runs_and_players(datas, extras):
  """
    WARNING!!! All Players Data MUST NOT be sorted in any mean in order to align with the index of the player name and id list that is taken originally
  """

  all_runs = datas[0]
  all_players_id = datas[1][0]
  all_players_name = datas[1][1]
  all_players_national = datas[1][2]
  all_platforms = datas[2]
  all_main_categories_id = extras[0]
  all_main_categories_name = extras[1]
  all_old_categories_id = extras[2]
  all_old_categories_name = extras[3]
  fixed_old_to_main_id = extras[4]
  all_deprecated_runs = extras[5]
  all_revalidated_runs = extras[6]
  exception_username = extras[7]

  all_reworked_runs = []
  all_reworked_players = []
  unknown_verified_deprecated_date_count = 0 
  index = 0

  for run in all_runs:
      index += 1
      #print(run)
      new_run = create_new_reworked_run_data(run)
      new_run["position"] = index
      new_run["platform"] = all_platforms[1][all_platforms[0].index(run["system"]["platform"])]

      if run["category"] == "7dg6l4gk":
        if "ylqmzpmn" in run["values"] and "gnxvz4jl" in run["values"]:
          new_run["category_id"] = "7dg6l4gk" + run["values"]["ylqmzpmn"] + run["values"]["gnxvz4jl"]
          new_run["category_name"] = all_main_categories_name[all_main_categories_id.index(new_run["category_id"])]
        else:
          new_run["category_id"] = "0x11111111"
          new_run["category_name"] = "UNKNOWN NAME"
          new_run["status"].append("orphaned")
      elif run["category"] == "n2yg8772":
        if "9l774k9l" in run["values"] and "yn259g0n" in run["values"]:
          new_run["category_id"] = "n2yg8772" + run["values"]["9l774k9l"] + run["values"]["yn259g0n"]
          new_run["category_name"] = all_main_categories_name[all_main_categories_id.index(new_run["category_id"])]
        else:
          new_run["category_id"] = "0x11111111"
          new_run["category_name"] = "UNKNOWN NAME"
          new_run["status"].append("orphaned")
      elif run["category"] == "wk65l5e2":
        new_run["category_id"] = run["values"]["onvymwrn"] + run["values"]["ql695jxl"] + run["values"]["ylpk42v8"]
        new_run["category_name"] = all_main_categories_name[all_main_categories_id.index(new_run["category_id"])]
      elif run["category"] == "7kjp5pxk":
        new_run["status"].append("deprecated")
        if "wlewoo4l" in run["values"] and "38dooe0l" in run["values"]:
          new_run["category_id"] = run["values"]["wlewoo4l"] + run["values"]["38dooe0l"]
          new_run["category_name"] = all_old_categories_name[all_old_categories_id.index(new_run["category_id"])]
          new_run["category_id"] = fixed_old_to_main_id[all_old_categories_id.index(new_run["category_id"])]
          if new_run["category_id"] in all_old_categories_id :
            new_run["category_name"] = "UNKNOWN NAME"
            new_run["status"].append("ignored") 
        else :
          new_run["category_id"] = "0x11111111"
          new_run["category_name"] = "UNKNOWN NAME"
          new_run["status"].append("orphaned")
      elif run["category"] == "q25q0782":
        new_run["status"].append("deprecated")
        if "wl31kkv8" in run["values"] and "gnx003xn" in run["values"]:
          new_run["category_id"] = run["values"]["wl31kkv8"] + run["values"]["gnx003xn"]
          new_run["category_name"] = all_old_categories_name[all_old_categories_id.index(new_run["category_id"])]
          new_run["category_id"] = fixed_old_to_main_id[all_old_categories_id.index(new_run["category_id"])]
          if new_run["category_id"] in all_old_categories_id :
            new_run["category_name"] = "UNKNOWN NAME"
            new_run["status"].append("ignored")
        else :
          new_run["category_id"] = "0x11111111"
          new_run["category_name"] = "UNKNOWN NAME"
          new_run["status"].append("orphaned")
      else:
        new_run["category_id"] = run["category"]
        new_run["category_name"] = "OTHERS"
        new_run["status"].append("ignored")

      if run["status"]["status"] == "new" :
        new_run["status"] = "pending"
      elif run["status"]["status"] == "rejected":
        new_run["status"].append("rejected")
        new_run["rejected_reason"] = run["status"]["reason"]
        if "deprecated" in new_run["status"]:
          new_run["deprecated_date"] = run["date"] + "T00:00:00Z"
      else:
        new_run["status"].append("verified")
        new_run["verify_date"] = run["status"]["verify-date"]
        new_run["validated_date"] = run["status"]["verify-date"]
        new_run["verifier"] = all_players_name[all_players_id.index(run["status"]["examiner"])]
        if "deprecated" in new_run["status"]:
          new_run["deprecated_date"] = run["status"]["verify-date"] + " (N/A)"
          unknown_verified_deprecated_date_count += 1

      for player in run["players"]:
        if player["rel"] == "user":
          new_run["players"].append(all_players_name[all_players_id.index(player["id"])])
        elif player["rel"] == "guest" and player["name"] in exception_username:
          new_run["players"].append(player["name"])
        else :
          new_run["players"].append(player["name"] + "(guest)")

        if new_run["run_id"] in all_deprecated_runs:
          new_run["deprecated_date"] = all_deprecated_runs[f"{new_run["run_id"]}"]
          unknown_verified_deprecated_date_count -= 1
        if new_run["run_id"] in all_revalidated_runs:
          new_run["validated_date"] = all_revalidated_runs[f"{new_run["run_id"]}"]

      if "ignored" in new_run["status"] or "deprecated" in new_run["status"]:
        new_run["placement"] = "deprecated"
      if "rejected" in new_run["status"] and "orphaned" in new_run["status"]:
        new_run["placement"] = "rejected*"
      elif "rejected" not in new_run["status"] and "orphaned" in new_run["status"]:
        new_run["placement"] = "orphaned"
      elif "rejected" in new_run["status"] and "orphaned" not in new_run["status"]:
        new_run["placement"] = "rejected"
      else:
        pass

      if "deprecated" in new_run["status"] and "orphaned" in new_run["status"] and "verified" in new_run["status"]:
        unknown_verified_deprecated_date_count -= 1

      new_run["players_in_format"] = ", ".join(new_run["players"])

      all_reworked_runs.append(new_run)

  for player in all_players_name:
      #print(player)
      new_player = create_new_reworked_player_data(player)
      new_player["player_id"] = all_players_id[all_players_name.index(player)]
      new_player["nationality"] = all_players_national[all_players_name.index(player)]
      all_reworked_players.append(new_player)

  return all_reworked_runs, all_reworked_players, unknown_verified_deprecated_date_count
  
def get_current_data(reworked: list, datas: list):

  all_runs = deepcopy(sorted(reworked[0], key=lambda t: t["time_in_seconds"]))
  all_players = reworked[1]
  all_players_name = datas[1][1]

  all_valid_runs = []
  category_checklist = []
  obsolete_player_checklist = []
  category_run_count = []
  previous_time_list = []

  for run in all_runs:
    if "ignored" in run["status"] or "orphaned" in run["status"] or "rejected" in run["status"] or "pending" in run["status"]:
      continue
    if "deprecated" in run["status"]:
      for player in run["players"]:
          if "(guest)" not in player:
            player_info = all_players[all_players_name.index(player)]
            player_info["total_run_count"] += 1
            player_info["total_run_time"] += run["time_in_seconds"]
            player_info["total_run_time_in_format"] = time_to_text_2(player_info["total_run_time"])
            player_info["players_runs"].append(run)
            player_info["players_runs_in_simple_format"].append(run["category_name"] + " at " + run["time_in_format"])
            all_players[all_players_name.index(player)] = player_info
      all_valid_runs.append(run)
      continue

    if run["category_id"] not in category_checklist:
      category_checklist.append(run["category_id"])
      category_run_count.append(1)
      obsolete_player_checklist.append([set(run["players"])])
      previous_time_list.append(run["time_in_seconds"])
      run["placement"] = 1
    else:
      c_index = category_checklist.index(run["category_id"])
      category_run_count[c_index] += 1
      if set(run["players"]) in obsolete_player_checklist[c_index]:
        category_run_count[c_index] -= 1
        run["placement"] = "obsolete"
      else:
        run["placement"] = category_run_count[c_index]
        obsolete_player_checklist[c_index].append(set(run["players"]))
      if run["time_in_seconds"] == previous_time_list[c_index] and run["placement"] != "obsolete":
        run["placement"] -= 1
      previous_time_list[c_index] = run["time_in_seconds"]

    all_valid_runs.append(run)
    for player in run["players"]:
        if "(guest)" not in player:
          player_info = all_players[all_players_name.index(player)]
          player_info["total_run_count"] += 1
          player_info["total_run_time"] += run["time_in_seconds"]
          player_info["total_run_time_in_format"] = time_to_text_2(player_info["total_run_time"])
          player_info["players_runs"].append(run)
          player_info["players_runs_in_simple_format"].append(run["category_name"] + " at " + run["time_in_format"])
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

          all_players[all_players_name.index(player)] = player_info

  all_current_runs = sorted(all_runs, key=lambda r: r["position"])
  all_current_valid_runs = sorted(all_valid_runs, key=lambda r: r["position"])
  #with open("test-data.json", "w") as file:
  #  json.dump(all_current_runs, file)

  return all_current_runs, all_current_valid_runs, all_players

def get_player_wrc_over_time(valid_runs: list, datas: list, all_players: list):

  all_runs = deepcopy(sorted(valid_runs, key=lambda t: src_time_to_datetime(t["validated_date"])))
  all_players_name = datas[1][1]

  default_player_list = []
  for player in all_players_name:
    default_player_list.append({f"{player}" : 0, f"{player}-highest": 0})
  player_stats_overtime = []

  run_index = 0
  active_player_list = deepcopy(default_player_list)
  current_datepoint = datetime.datetime(2017, 9, 14, 0, 0, 0)
  active_run_list = []
  previous_dpoint_data = {}

  while True:
    if run_index >= len(all_runs):
      break

    validated_date = src_time_to_datetime(all_runs[run_index]["validated_date"])
    print((run_index+1), "/" ,len(all_runs), " at " , current_datepoint)

    if validated_date < current_datepoint:
      active_run_list.append(all_runs[run_index])
      run_index += 1
      continue
    else:

      current_datepoint += datetime.timedelta(hours=TIME_MARGIN_IN_HOURS)
      if len(active_run_list) <= 0:
        continue

      active_run_list = sorted(active_run_list, key=lambda r: r["time_in_seconds"])
      current_dpoint_player_list = deepcopy(default_player_list)
      category_checklist = []
      obsolete_player_checklist = []
      category_run_count = []
      previous_time_list = []
      placeholder = {}

      for run in active_run_list:
        deprecated_date = src_time_to_datetime(run["deprecated_date"])
        if deprecated_date < current_datepoint:
          continue

        if run["category_id"] not in category_checklist:
          category_checklist.append(run["category_id"])
          category_run_count.append(1)
          obsolete_player_checklist.append([set(run["players"])])
          previous_time_list.append(run["time_in_seconds"])
          run["placement"] = 1
        else:
          c_index = category_checklist.index(run["category_id"])
          category_run_count[c_index] += 1
          if set(run["players"]) in obsolete_player_checklist[c_index]:
            category_run_count[c_index] -= 1
            run["placement"] = "obsolete"
          else:
            run["placement"] = category_run_count[c_index]
            obsolete_player_checklist[c_index].append(set(run["players"]))
          if run["time_in_seconds"] == previous_time_list[c_index] and run["placement"] != "obsolete":
            run["placement"] -= 1
          previous_time_list[c_index] = run["time_in_seconds"]

        if run["placement"] == 1:
          for p in run["players"]:
            if "(guest)" not in p:
              value = current_dpoint_player_list[all_players_name.index(p)][f"{p}"]
              value += 1
              if active_player_list[all_players_name.index(p)][f"{p}-highest"] < value:
                active_player_list[all_players_name.index(p)][f"{p}-highest"] = value
                all_players[all_players_name.index(p)]["highest_wr_count"] = value
              placeholder[f"{p}"] = value
              placeholder[f"{p}-highest"] = active_player_list[all_players_name.index(p)][f"{p}-highest"]
              current_dpoint_player_list[all_players_name.index(p)][f"{p}"] = value

      if placeholder != previous_dpoint_data:
        player_stats_overtime.append({"date": f"{current_datepoint}"} | placeholder)
      previous_dpoint_data = placeholder

  all_players = sorted(all_players, key=lambda p: p["highest_wr_count"], reverse=True)   

  return player_stats_overtime, all_players

def main():
  start = time.perf_counter()

  data_getter.main()

  with open("x-data.json", 'r', encoding='utf-8') as file:
      all_datas = json.load(file)
  """
    [0] -> All Runs in the API
    [1] -> All Registered (aka having an account) Players' Information
        [0] -> IDs
        [1] -> Names of the User
        [2] -> Nationality
    [2] -> All Platforms IDs and Names
        [0] -> IDs
        [1] -> Names
  """

  with open("x-extras-data.json", 'r', encoding='utf-8') as file:
      extra_datas = json.load(file)

  """
    [0] -> All the valid reworked runs (no orphaned, no VIP and no unknown map)
    [1] -> All the names in the sub-categories
    [2] -> All the IDs in the Old category (Survivor Old & Beast Old)
    [3] -> All the names in the old sub-categories, reworked to fit the main one
    [4] -> The fitting IDs for the old sub-categories
    [5] -> Deprecated Runs start date and end date (run in the Old categories, will be very important for preserving history)
    [6] -> Revalidated Runs for runs that both the date and the deprecated date is in between the date and the verified date (aka late verifying for reasons)
    [7] -> extra names
  """

  reworked_datas = process_runs_and_players(all_datas, extra_datas)
  """
    [0] -> All reworked runs
    [1] -> All the reworked players
    [2] -> Unknown Verified Deprecated Date Count #[deprecated method, do not use]
  """

  current_datas = get_current_data(reworked_datas, all_datas)
  """
    [0] -> All runs 
    [1] -> All the currently valid runs (that means it's verified and in a known category)
    [2] -> All the current players stat
  """
  player_wrc_over_time = get_player_wrc_over_time(current_datas[1], all_datas, current_datas[2])

  print("finished formatting datas ||", time.perf_counter() - start)

  #print(len(all_data[0])," - ",len(all_data[1]))
  #rnd = random.randint(0,len(all_data[0])-1)
  #print(all_data[0][rnd], rnd)
  #with open("test-data.json", "w") as file:
  #  json.dump(all_data[0], file)
  with open("test-data.json", "w") as file:
    json.dump(player_wrc_over_time[1], file)

  return all_datas, extra_datas, reworked_datas, current_datas, player_wrc_over_time

#main()
