import dfnhl

def main():
    fantasy = dfnhl.DailyFantasy()
    fantasy.setup()

    fantasy.print_matchups()
    fantasy.print_lineup("Edmonton Oilers")
    fantasy.bargain_players()

if __name__ == "__main__":
    main()