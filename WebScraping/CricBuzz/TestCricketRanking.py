from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.cricbuzz.com/cricket-stats/icc-rankings/men/all-rounder').text
soup = BeautifulSoup(html_text, 'lxml')
players = soup.find_all('div', class_= 'cb-col cb-col-100 cb-font-14 cb-lst-itm text-center')

# print(players.text)
for player in players:
    player_name = player.find('a', class_='text-hvr-underline text-bold cb-font-16').text
    player_country = player.find('div', class_= 'cb-font-12 text-gray').text
    player_rating = player.find('div', class_= 'cb-col cb-col-17 cb-rank-tbl pull-right').text
    print(f"Player Name: {player_name}")
    print(f"Country: {player_country}")
    print(f"Player Rating: {player_rating}")