import requests
import json
import re

from bs4 import BeautifulSoup

class Players:

    urls = {
        'gamelog': 'https://statsapi.web.nhl.com/api/v1/people/{id}/stats?stats=gameLog&season=20182019',
        'stats': 'https://statsapi.web.nhl.com/api/v1/people/{id}/stats?stats=statsSingleSeason&season=20182019',
        'team': 'https://statsapi.web.nhl.com/api/v1/teams/{id}',
        'roster': 'https://statsapi.web.nhl.com/api/v1/teams/{id}/roster',
        'salary': 'https://rotogrinders.com/lineups/nhl?site=fanduel'
    }

    scoring = {
        'assists': 8,
        'goals': 12,
        'shots': 1.6,
        'blocked': 1.6,
        'powerPlayPoints': 0.5,
        'powerPlayGoals': 0.5,
        'shortHandedPoints': 2,
        'shortHandedGoals': 2,
        'goalsAgaisnt': -4,
        'shutouts': 8,
        'saves': 0.8,
        'decision': 12
    }

    def __init__(self, teams):
        self.teams = teams
        self.players = {}
        self.salaries = {}
    
    def find_salary(self):
        page = requests.get(self.urls['salary']).content
        soup = BeautifulSoup(page, 'html.parser')

        player_names = soup.find_all('a', {'class': 'player-popup'})
        player_salaries = soup.find_all('span', {'class': 'salary'})

        names = []
        salaries = []

        for name in player_names:
            if (name.get("title") is not None):
                names.append(name.get("title"))
            else:
                names.append(name.text)
        
        print("Finding Player Salaries...")
        for salary in player_salaries:
            if (salary.get("data-salary") is not None):
                if (salary.get("data-salary") == ""):
                    salaries.append(0)
                else:
                    # Removes white space and \n
                    sal = re.sub(r"\W", "", salary.text)
                    # Convert strings to int and correct value
                    if len(sal) == 3:
                        sal = sal[0] + sal[1] + "00"
                        salaries.append(int(sal))
                    elif len(sal) == 2:
                        sal = sal[0] + "000"
                        salaries.append(int(sal))
        print("Found Player Salaries.")

        self.salaries = dict(zip(names, salaries))
    
    def get_salary(self):
        if not self.salaries:
            self.find_salary()

        return self.salaries

    def projected_points(self, id):
        url = self.urls['gamelog'].format(id=id)
        page = json.loads(requests.get(url).text)

        fpp = 0

        stat_len = len(page['stats'][0]['splits'])

        if (len(page['stats'][0]['splits']) < 5):
            stat_len = len(page['stats'][0]['splits'])-1
        else:
            stat_len = 5

        for i in range(0, stat_len):
            for key in self.scoring:
                if (key in page['stats'][0]['splits'][i]['stat']):
                    # Win/Loss Stat is in string format, thus this check
                    if (key == 'decision'):
                        if (page['stats'][0]['splits'][i]['stat'][key] == 'W'):
                            val = self.scoring[key]
                    else:
                        val = page['stats'][0]['splits'][i]['stat'][key] * self.scoring[key]

                    fpp += val

        return round(fpp/5, 2)

    def find_lineup(self):
        print("Getting Team Lineups...")
        for team in self.teams:
            id = self.teams[team]['id']
            url = self.urls['roster'].format(id=id)
            page = json.loads(requests.get(url).text)

            temp_players = self.get_salary()

            players = {}

            # Checks current lineup and combines the id and salary under the player name
            for player in range(0, len(page['roster'])-1):
                if (page['roster'][player]['person']['fullName'] in temp_players):
                    fpp = self.projected_points(page['roster'][player]['person']['id'])

                    stat_url = self.urls['stats'].format(id=page['roster'][player]['person']['id'])
                    stat_page = json.loads(requests.get(stat_url).text)

                    #print(page['roster'][player]['person']['id'])

                    if ('goals' in stat_page['stats'][0]['splits'][0]['stat']):
                        goals = stat_page['stats'][0]['splits'][0]['stat']['goals']
                    else:
                        goals = 0

                    if ('assists' in stat_page['stats'][0]['splits'][0]['stat']):
                        assists = stat_page['stats'][0]['splits'][0]['stat']['assists']
                    else:
                        assists = 0
                    
                    #print(stat_page['stats'][0]['splits'][0]['stat']['goals'])

                    players[page['roster'][player]['person']['fullName']] = {
                        'id': page['roster'][player]['person']['id'],
                        'position': page['roster'][player]['position']['abbreviation'],
                        'salary': temp_players[page['roster'][player]['person']['fullName']],
                        'fpp': fpp,
                        'goals': goals,
                        'assists': assists,
                        'points': goals + assists
                    }
            
            # Player lineups are put as the value for each team currently playing
            self.players[self.teams[team]['name']] = players        
        print("Found Team Lineups.\n") 

    def get_lineup(self):
        if not self.players:
            self.find_lineup()

        return self.players
