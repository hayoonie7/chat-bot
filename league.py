import requests
import keys 

api_key = keys.api_key

def get_summoner(name, tagline): 
    api_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tagline}?api_key={api_key}"


    resp = requests.get(api_url)
    #return resp.json()
    info = resp.json()
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

    print(api_url)
    #resp = requests.get(api_url)
    #info = resp.json()


    #print(info)


name = "hayoonie"
tagline = 1946
sum_info = get_summoner(name, tagline)
print(sum_info)

