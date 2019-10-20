import dfnhl

def main():
    fantasy = dfnhl.DailyFantasy()
    fantasy.setup()

    fantasy.print_matchups()
    #print()
    #fantasy.print_lineup("Calgary Flames")
    print()
    fantasy.bargain_players()
    print()
    fantasy.get_scoring_leaders()
    fantasy.print_all_leaders()

if __name__ == "__main__":
    main()