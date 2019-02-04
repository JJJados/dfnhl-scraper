import matchups
import players

class DailyFantasy:

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

        self.goal_leaders = []
        self.assist_leaders = []
        self.point_leaders = []
        
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
                if (salary > 0 and salary < 6000 and fpp > 0):
                    value = salary / fpp
                    values.append([value, player, salary, fpp])

        sorted_values = sorted(values, key=self.getKey)

        print("Top 5 Bargain Players (last 5 games): ")
        for i in range(0, 5):
            print("\t" + str(i+1) + ". "+ sorted_values[i][1] + ", Salary: " + str(sorted_values[i][2]) 
                    + ", Projected Fantasy Point: " + str(sorted_values[i][3]))

    def get_scoring_leaders(self):
        goal_leaders = []
        assist_leaders = []
        point_leaders = []

        for lineup in self.lineups:
            for player in self.lineups[lineup]:
                goals = self.lineups[lineup][player]['goals']
                assists = self.lineups[lineup][player]['assists']
                points = self.lineups[lineup][player]['points']
                fpp = self.lineups[lineup][player]['fpp']

                goal_leaders.append([goals, player, points, fpp])
                assist_leaders.append([assists, player, points, fpp])
                point_leaders.append([points, player, goals, assists, fpp])
        
        self.goal_leaders = sorted(goal_leaders, key=self.getKey)
        self.assist_leaders = sorted(assist_leaders, key=self.getKey)
        self.point_leaders = sorted(point_leaders, key=self.getKey)

    def leading_goals(self):
        val = 1

        print("Top 5 Goal Leaders")
        for i in range(len(self.goal_leaders)-1, len(self.goal_leaders)-6, -1):
            print("\t" + str(val) + ". "+ self.goal_leaders[i][1] + ", Goals: " + str(self.goal_leaders[i][0]) 
                    + ", Total Points: " + str(self.goal_leaders[i][2])
                    + ", Projected Fantasy Point (last 5 games): " + str(self.goal_leaders[i][3]))
            val+=1

    def leading_assists(self):
        val = 1

        print("Top 5 Assist Leaders")
        for i in range(len(self.assist_leaders)-1, len(self.assist_leaders)-6, -1):
            print("\t" + str(val) + ". "+ self.assist_leaders[i][1] + ", Assists: " + str(self.assist_leaders[i][0]) 
                    + ", Total Points: " + str(self.assist_leaders[i][2])
                    + ", Projected Fantasy Point (last 5 games): " + str(self.assist_leaders[i][3]))
            val+=1
    
    def leading_scorers(self):
        val = 1

        print("Top 5 Leading Scorers")
        for i in range(len(self.point_leaders)-1, len(self.point_leaders)-6, -1):
            print("\t" + str(val) + ". "+ self.point_leaders[i][1] + ", Points: " + str(self.point_leaders[i][0]) 
                    + ", Goals: " + str(self.point_leaders[i][2]) + ", Assists: " + str(self.point_leaders[i][3])
                    + ", Projected Fantasy Point (last 5 games): " + str(self.point_leaders[i][4]))
            val+=1