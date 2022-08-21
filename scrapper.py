from bs4 import BeautifulSoup
import helper
import requests, argparse, urllib.parse, urllib.request, json

API_KEY = open("keys.txt", 'r').readline()

def get_date():
    #gets date
    target_html = requests.get("https://www.oddsshark.com/nfl/odds")
    soup = BeautifulSoup(target_html.text, "html.parser")
    soup = soup.find(id="op-content-wrapper")
    DateSoup = soup.find_all("div", "op-separator-bar op-left no-group-name")[1]
    DateSoup = DateSoup["data-op-date"]
    date = DateSoup.split('"')
    date = date[3]
    date = date[-2:]
    return(int(date))

def build_config(url,num_games):
    teams = []
    spreads = []
    data = requests.get(f"{url}/v4/sports/americanfootball_nfl/odds/?apiKey={API_KEY}&regions=us&markets=spreads").content
    json_data = json.loads(data)
    for num,game in enumerate(json_data):
        start_time = game["commence_time"]
        odds = game["bookmakers"][0]["markets"][0]["outcomes"][0]
        spreads.append(float(odds["point"]))
        name_field = game["bookmakers"][0]["markets"][0]["outcomes"]
        teams.append((helper.nfl_abrv[name_field[0]["name"]], helper.nfl_abrv[name_field[1]["name"]]))

    config = open("config.csv", "w")
    num = 0

    #build the config file
    for team,point in zip(teams,spreads):
        num += 1
        if num > num_games:
            break
        if point < 0:
            if point.is_integer():
                point -= 0.5
            config.write("{},{},{}\n".format(team[0].upper(),str(point),team[1].upper()))
        else:
            if point.is_integer():
                point += 0.5
            config.write("{},-{},{}\n".format(team[1].upper(),str(point),team[0].upper()))
    config.close()

def get_scores() -> dict:
    scores = {}
    response = urllib.request.urlopen("http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard")
    json_text = response.read().decode(encoding = 'utf-8')
    result = json.loads(json_text)
    for game in result['events']:
        if game['status']['type']['state'] == 'pre':
            pass
        else:
            team1 = game['competitions'][0]['competitors'][0]['team']['abbreviation']
            score1 = game['competitions'][0]['competitors'][0]['score']
            team2 = game['competitions'][0]['competitors'][1]['team']['abbreviation']
            score2 = game['competitions'][0]['competitors'][1]['score']
            if team1 == 'JAX':
                team1 = 'JAC'
            if team2 == 'JAX':
                team2 = 'JAC'
            if team1 == 'WSH':
                team1 = 'WAS'
            if team2 == 'WSH':
                team2 = 'WAS'
            scores[team1] = score1
            scores[team2] = score2
    return(scores)
