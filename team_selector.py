import matchups
import players

class TeamSelector:

    def __init__(self):
        self.matchups = matchups.Matchups()
    
    def print_matchup(self):
        print(self.matchups.get_matchups())
    
    def print_players(self):
        self.matchups.find_teams()
        p = players.Players(self.matchups.get_teams())
        print(p.get_roster())



a = TeamSelector()
a.print_players()