import matchups
import players

class TeamSelector:

    def __init__(self):
        self.lineup = {}
        self.players = {}
        self.matchups = matchups.Matchups()
    
    def print_matchup(self):
        print(self.matchups.get_matchups())
    
    def print_players(self):
        if not self.matchups.find_teams():
            print("Schedule Not Updated.")
            return
            
        print("Starting Search...")
        print("_________________________\n")
        self.players = players.Players(self.matchups.get_teams())
        self.lineup = self.players.get_lineup()
        print("\nSearch Finished.")
        print("_________________________\n")
        print(self.lineup)
        



a = TeamSelector()
a.print_players()