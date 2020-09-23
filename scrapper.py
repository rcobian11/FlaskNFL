from bs4 import BeautifulSoup
import requests, argparse

#gets the team name and returns as string
def get_team(pos):
    ctr = 0
    for num, elem in enumerate(pos):
        if elem == ':':
            ctr += 1
        if ctr == 2:
            team = pos[num + 1:-1].strip('"')
            break
    return(team)

#gets the spread, strips extra chars, and returns as float
def get_points(pos):
    #ctr counts number of " 
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
        top_team = get_team(top)
        bot_team = get_team(bot)
        teams.append((top_team,bot_team))
        #print("{} vs {}".format(top_team, bot_team))
    for junk in soup.find_all('div', 'op-item-row-wrapper not-futures'): #gets the spread which is stored in junk
        points = junk.find('div', 'op-first-row').div['data-op-info']
        spreads.append(get_points(points))
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="build website for picks")
    parser.add_argument("-u","--url",help="url of spreads",type=str, required=True)
    parser.add_argument("-g","--games",help="number of games this week",type=int, required=True)
    args = parser.parse_args()
    scrapper.build_config(args.url,args.games)  
