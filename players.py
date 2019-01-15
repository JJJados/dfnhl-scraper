import requests
import json
import urllib.request
import re

from bs4 import BeautifulSoup

class Players:

    urls = {
        'team': 'https://statsapi.web.nhl.com/api/v1/teams/{id}',
        'roster': 'https://statsapi.web.nhl.com/api/v1/teams/{id}/roster',
        'salary': 'https://rotogrinders.com/lineups/nhl?site=fanduel'
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

        players = self.scrape_salary(player_names, player_salaries)

        return players

    def find_roster(self):
        for team in self.teams:
            id = self.teams[team]['id']
            url = self.urls['roster'].format(id=id)
            page = json.loads(requests.get(url).text)

            #players = self.find_salary()

            #for player in range(0, len(page['roster'])-1):
            #    players[page['roster'][player]['person']['fullName']] = {'id': page['roster'][player]['person']['id']}

            #self.players[self.teams[team]['name']] = players                

    def get_roster(self):
        if not self.players:
            self.find_roster()

        return self.players
