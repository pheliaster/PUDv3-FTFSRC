import map_updater
import run_player_data
import json

if __name__ == "__main__":
  #map_updater.main()

  with open('map-data.json', 'r', encoding='utf-8') as file:
    all_categories_data = json.load(file)
  
  all_data = run_player_data.main()
  all_runs_data = all_data[0]
  all_players_data = all_data[1]
  print(len(all_runs_data)," - ",len(all_players_data))



    