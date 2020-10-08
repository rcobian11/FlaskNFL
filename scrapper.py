from bs4 import BeautifulSoup
import requests, argparse

#gets the team name and returns as string
def _get_team(pos):
    ctr = 0
    for num, elem in enumerate(pos):
        if elem == ':':
            ctr += 1
        if ctr == 2:
            team = pos[num + 1:-1].strip('"')
            break
    return(team)

#gets the spread, strips extra chars, and returns as float
def _get_points(pos):
    #ctr counts number of '"' 
    ctr = 0
    for num, elem in enumerate(pos):
        if elem == '"':
            ctr += 1
        if ctr == 3:
            num2 = num+1
            while(pos[num2] != '"'):
                num2 += 1
            points = pos[num + 1: num2]
            break
    #if number is positive return float
    if points[0] == '+':
        return(float(points[1:]))
    #else convert number to negative and return as float
    else:
        return(float(points[1:]) * -1)

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
    target_html = requests.get(url)
    soup = BeautifulSoup(target_html.text, "html.parser")
    soup = soup.find(id="op-content-wrapper")

    #gets teams in the table
    for team in soup.find_all('div', "op-matchup-wrapper football"):
        top = team.find("div","op-matchup-team-wrapper").div['data-op-name'] #home team
        bot = team.find("div","op-matchup-team-wrapper").div.next_sibling['data-op-name'] #away team
        top_team = _get_team(top)
        bot_team = _get_team(bot)
        teams.append((top_team,bot_team))
        #print("{} vs {}".format(top_team, bot_team))

    #gets the spread which is stored in junk
    for junk in soup.find_all('div', 'op-item-row-wrapper not-futures'): 
        try:
            points = junk.find_all('div', 'op-first-row')[1].div['data-op-info']
            spreads.append(_get_points(points))
        except IndexError:
            points = junk.find_all('div', 'op-first-row')[2].div['data-op-info']
            spreads.append(_get_points(points))

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
