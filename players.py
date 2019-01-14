import requests
import json

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

    def find_roster(self):
        for team in self.teams:
            id = self.teams[team]['id']
            url = self.urls['roster'].format(id=id)
            page = json.loads(requests.get(url).text)

            players = {}

            for player in range(0, len(page['roster'])-1):
                players[page['roster'][player]['person']['fullName']] = page['roster'][player]['person']['id']

            self.players[self.teams[team]['name']] = players                

    def get_roster(self):
        if not self.players:
            self.find_roster()

        return self.players