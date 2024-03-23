from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize a WebDriver
driver = webdriver.Chrome()

# Navigate to the OLX website
driver.get('https://www.olx.pl/')

# Find the search bar and type "botox"
search_bar = driver.find_element(By.ID, 'headerSearch')
search_bar.send_keys('botox')

# Press Enter
search_bar.send_keys(Keys.ENTER)

# Wait for the page to load
driver.implicitly_wait(10)

# Get the HTML content of the search results page
html_text = driver.page_source

# Close the WebDriver
driver.quit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_text, 'html.parser')

# Extract offer details
offers = soup.find_all('div', class_='css-1sw7q4x')
search_results = []

for offer in offers[0:10]:  # Only scrape the first 10 offers for demonstration
    offer_name = offer.find('h3', class_='css-16v5mdi').text.strip()
    location = offer.find('span', class_='css-1e7mfvj').text.strip()

    print(f'''
    Name of the offer: {offer_name}
    Location: {location}\n
    ''')

    result = {'offer_name': offer_name, 'location': location}
    search_results.append(result)

# Convert the search results to a DataFrame and save it to a CSV file
df = pd.DataFrame(search_results)
print(df)
df.to_csv('search_results.csv', index=False)
