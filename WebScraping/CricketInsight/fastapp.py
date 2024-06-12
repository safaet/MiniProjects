from fastapi import FastAPI, Response, Query
from fastapi.responses import StreamingResponse
from bs4 import BeautifulSoup
import requests
import csv
import io

app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the cricket stats scraper API"}

@app.get("/scrape")
async def scrape_stats(url: str = Query(..., description="URL of the cricket stats page")):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    players = soup.find_all('tr', class_='cb-srs-stats-tr')

    csv_columns = ['Player Name', 'Matches', 'Innings', 'Runs', 'Average', 'Strike Rate', '4s', '6s']
    
    output = io.StringIO()
    writer = csv.writer(output)
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
        
        writer.writerow([player_name, player_matches, player_innings, player_runs, player_avg, player_sr, player_4s, player_6s])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=cricket_stats.csv"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
