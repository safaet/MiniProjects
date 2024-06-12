import csv
from bs4 import BeautifulSoup
import requests

# URL of the page to scrape
link = input("Enter Link: ")
html_text = requests.get(link).text
soup = BeautifulSoup(html_text, 'lxml')
players = soup.find_all('tr', class_='cb-srs-stats-tr')

# Prepare the CSV file
Country = input("Enter Country Name: ")
csv_file = f'Data/{Country}_cricket_most_run.csv'
csv_columns = ['Player Name', 'Matches', 'Innings', 'Runs', 'Average', 'Strike Rate', '4s', '6s']

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_columns)  # Write the header row
    
    for index, player in enumerate(players):
        if index == 0:
            continue
        
        player_data = player.find_all('td')
        
        player_name = player_data[0].text.strip()
        player_matches = player_data[1].text.strip()
        player_innings = player_data[2].text.strip()
        player_runs = player_data[3].text.strip()
        player_avg = player_data[4].text.strip()
        player_sr = player_data[5].text.strip()
        player_4s = player_data[6].text.strip()
        player_6s = player_data[7].text.strip()
        
        # Write the player data to the CSV file
        writer.writerow([player_name, player_matches, player_innings, player_runs, player_avg, player_sr, player_4s, player_6s])

print(f"Data has been written to {csv_file}")
