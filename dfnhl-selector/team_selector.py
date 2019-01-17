import matchups
import players

class TeamSelector:

    def __init__(self):
        self.lineup = {}
        self.players = {}
        self.teams = {}
        self.matchups = matchups.Matchups()
    
    def print_matchup(self):
        print(self.matchups.get_matchups())
    
    def print_players(self):
        if (self.matchups.find_teams() == False):
            print("Schedule Not Updated.")
            return

        print("Starting Search...")
        print("_________________________\n")
        self.teams = self.matchups.get_teams()
        self.players = players.Players(self.teams)
        self.lineup = self.players.get_lineup()
        print("\nSearch Finished.")
        print("_________________________\n")
        print(self.lineup)
        


a = TeamSelector()
a.print_players()