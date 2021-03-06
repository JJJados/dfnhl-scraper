# Daily NHL Fantasy Scraper

## Purpose

This project was intended to explore the use of the NHL API, BeautifulSoup for web-scraping and apply that to Daily Fantasy Hockey, specifically FanDuel. The selection of the players are from the daily NHL lineups, and the fpp (projected fantasy points) is based off the players last 5 games in the league (or less if the player has not reached 5 games). In addition, the salary is taken from an outside source unrelated to Fanduel, however it is updated daily and proven to be accurate.

## Feature Overview

*Currently only support for players last 5 games*

* List of Daily Matchups

* List of Team's Lineups

* List of Top 5 Daily Bargain Player's (fpp/salary)

* List of Top 5 Daily Goal/Assist/Point Leading Players

## Some Notes

Future updates to this project is to provide a model for team selection. This can be done by taking advantage of the NHL API to it's fullest capabilities by using players stats from previous seasons to find trends in their play, teams performance, and weighting these stats . Due to University and other projects these changes may take more time to implement, but provided I maintain playing Daily Fantasy Hockey my interest will continue to be improving the team selection model and providing a more analytically accurate team.

Features that may be implemented:
* Daily Fantasy Team Selection 

## Credits

Helpful end-points and documentation of the NHL API by Drew Hynes:
- [NHL-API-DOC](https://gitlab.com/dword4/nhlapi)

## License

MIT License