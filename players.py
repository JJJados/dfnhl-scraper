import requests
import json
import urllib.request
import re

from bs4 import BeautifulSoup

class Players:

    urls = {
        'gamelog': 'https://statsapi.web.nhl.com/api/v1/people/{id}/stats?stats=gameLog&season=20182019',
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
    
    def scrape_salary(self, player_names, player_salaries):
        names = []
        salaries = []

        for name in player_names:
            if (name.get("title") is not None):
                names.append(name.get("title"))
            else:
                names.append(name.text)
        
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
        
        return dict(zip(names, salaries))
    
    def find_salary(self):
        page = urllib.request.urlopen(self.urls['salary'])
        soup = BeautifulSoup(page, 'html.parser')

        player_names = soup.find_all('a', {'class': 'player-popup'})
        player_salaries = soup.find_all('span', {'class': 'salary'})

        temp_players = self.scrape_salary(player_names, player_salaries)

        return temp_players

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
                    if (key == 'decision'):
                        if (page['stats'][0]['splits'][i]['stat'][key] == 'W'):
                            val = self.scoring[key]
                    else:
                        val = page['stats'][0]['splits'][i]['stat'][key] * self.scoring[key]

                    fpp += val

        return round(fpp/5, 2)


    def find_roster(self):
        for team in self.teams:
            id = self.teams[team]['id']
            url = self.urls['roster'].format(id=id)
            page = json.loads(requests.get(url).text)

            temp_players = self.find_salary()

            players = {}

            # Checks current lineup and combines the id and salary under the player name
            for player in range(0, len(page['roster'])-1):
                if (page['roster'][player]['person']['fullName'] in temp_players):
                    fpp = self.projected_points(page['roster'][player]['person']['id'])
                    players[page['roster'][player]['person']['fullName']] = {
                        'id': page['roster'][player]['person']['id'],
                        'salary': temp_players[page['roster'][player]['person']['fullName']],
                        'fpp': fpp
                    }
            
            # Player lineups are put as the value for each team currently playing
            self.players[self.teams[team]['name']] = players         

    def get_roster(self):
        if not self.players:
            self.find_roster()

        return self.players