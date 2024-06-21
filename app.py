import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import BytesIO

def scrape_data(link):
    try:
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'lxml')
        players = soup.find_all('tr', class_='cb-srs-stats-tr')

        data = []
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

            data.append([player_name, player_matches, player_innings, player_runs, player_avg, player_sr, player_4s, player_6s])

        return data

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

# Streamlit app
st.title("Cricket Most Runs Scraper")

st.write("e.g. https://www.cricbuzz.com/cricket-team/india/2/stats")

link = st.text_input("Enter Link:")
country = st.text_input("Enter Country Name:")

if st.button("Scrape Data"):
    if link and country:
        with st.spinner("Scraping data..."):
            data = scrape_data(link)
            if data:
                df = pd.DataFrame(data, columns=['Player Name', 'Matches', 'Innings', 'Runs', 'Average', 'Strike Rate', '4s', '6s'])
                st.success("Data scraped successfully!")

                st.write("### Scraped Data")
                st.dataframe(df)

                csv = convert_df_to_csv(df)
                # excel = convert_df_to_excel(df)

                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=f'{country}_cricket_most_run.csv',
                    mime='text/csv',
                )

                # st.download_button(
                #     label="Download data as Excel",
                #     data=excel,
                #     file_name=f'{country}_cricket_most_run.xlsx',
                #     mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                # )
            else:
                st.error("Failed to scrape data. Please check the link and try again.")
    else:
        st.warning("Please enter both the link and country name.")

