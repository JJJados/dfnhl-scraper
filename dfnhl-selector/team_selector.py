import matchups
import players

class TeamSelector:

    def __init__(self):
        self.lineups = {}
        self.players = {}
        self.teams = {}
        self.matchups = matchups.Matchups()

    def setup(self):
        if (self.matchups.find_teams() == False):
            print("Schedule Not Updated.")
            return False

        self.teams = self.matchups.get_teams()
        self.players = players.Players(self.teams)
        self.lineups = self.players.get_lineup()
        
        return True
    
    def print_matchups(self):
        games = self.matchups.get_matchups()

        for game in games:
            print("AWAY: " + games[game]['teams']['away']['team']['name'] 
                + " vs. HOME: " + games[game]['teams']['home']['team']['name'])

    def print_lineup(self, team):
        for lineup in self.lineups:
            if (lineup == team):
                print(team + " lineup:")
                for player in self.lineups[lineup]:
                    print("\t" + player + ", " + self.lineups[lineup][player]['position'])

    def getKey(self, item):
        return item[0]

    def bargain_players(self):
        values = []

        for lineup in self.lineups:
            for player in self.lineups[lineup]:
                salary = self.lineups[lineup][player]['salary']
                fpp = self.lineups[lineup][player]['fpp']
                if (salary > 0 and salary < 6000):
                    value = salary / fpp
                    values.append([value, player, salary, fpp])

        sorted_values = sorted(values, key=self.getKey)

        print("Top 3 Bargain Players: ")
        for i in range(0, 3):
            print("\t" + str(i+1) + ". "+ sorted_values[i][1] + ", Salary: " + str(sorted_values[i][2]) 
                    + ", Projected Fantasy Point: " + str(sorted_values[i][3]))