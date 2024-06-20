import requests
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
api_key = os.getenv('api_key')

def get_summoner(name, tagline): 
    api_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tagline}?api_key={api_key}"


    resp = requests.get(api_url)
    #return resp.json()
    info = resp.json()
    print(info)
    return info
    #print(info)

def get_matches(puuid, startTime=None, endTime=None, queue=None, type=None, start=None, count=None):
    start_time_string = ""
    end_string = ""
    queue_string = ""
    type_string = ""
    start_string = ""
    count_string = ""
    if startTime is not None:
        start_time_string = f"startTime={startTime}" + "&"

    if endTime is not None:
        end_string = f"endTime={endTime}" + "&"
    
    if queue is not None:
        queue_string = f"queue={queue}" + "&" 
    
    if type is not None:
        type_string = f"type={type}" + "&"
    
    if start is not None:
        start_string = f"start={start}" + "&" 
    
    if count is not None:
        count_string = f"count={count}" + "&"

    api_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?{start_time_string}{end_string}{queue_string}{type_string}{start_string}{count_string}"
    api_url = api_url + 'api_key=' + api_key

    resp = requests.get(api_url)
    info = resp.json()
    print(info)
    return info

def get_match(match_id, puuid):
    api_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    resp = requests.get(api_url)
    match_stats = resp.json()
    participants = match_stats['metadata']['participants']
    player_index = participants.index(puuid)
    print(match_stats['info']['participants'][player_index]['summonerName'])
    player_index = participants.index(puuid)
    player_data = match_stats['info']['participants'][player_index]
    champ = player_data['championName']
    k = player_data['kills']
    d = player_data['deaths']
    a = player_data['assists']
    win = player_data['win']
    print("Champ:", champ, "Kills:", k, "Deaths:", d, "Assists:", a, "Win:", win)




name = "hayoonie"
tagline = 1946
sum_info = get_summoner(name, tagline)
print(sum_info)

