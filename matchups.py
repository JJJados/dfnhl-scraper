import requests
import json

class Matchups:

    urls = {
        'schedule': 'https://statsapi.web.nhl.com/api/v1/schedule',
    }

    def __init__(self):
        self.url = self.urls['schedule']
        self.page = json.loads(requests.get(self.url).text)
        self.games = {}
        self.teams = {}

    def find_matchups(self):
        for game in range(0, len(self.page['dates'][0]['games'])):
            game_num = 'game_{}'.format(game)
            self.games[game_num] = self.page['dates'][0]['games'][game]

    def get_matchups(self):
        if not self.games:
            self.find_matchups()

        return self.games

    def find_teams(self):
        if not self.games:
            self.find_matchups()
        
        i = 0

        for game in self.games:
            team_num_away = 'team_{}'.format(i)
            team_num_home = 'team_{}'.format(i+1)
            self.teams[team_num_away] = {'name': self.games[game]['teams']['away']['team']['name'], 'id': self.games[game]['teams']['away']['team']['id']}
            self.teams[team_num_home] = {'name': self.games[game]['teams']['home']['team']['name'], 'id': self.games[game]['teams']['home']['team']['id']}
            i+=2

    def get_teams(self):
        if not self.teams:
            self.find_teams()

        return self.teams