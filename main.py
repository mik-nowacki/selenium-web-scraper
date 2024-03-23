import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# TODO: Download html file of the offer
# TODO: Take a screenshot of the offer?
# TODO: Refactor results

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Select a browser of your choice
driver = webdriver.Chrome(options=chrome_options)

# Specify a website you want to scrape
driver.get("https://www.olx.pl/")

driver.implicitly_wait(100)

# Accept cookies
accept_cookies = driver.find_element(By.ID, value="onetrust-accept-btn-handler")
accept_cookies.click()

# Find the "Search" <input> by ID
search_bar = driver.find_element(By.ID, value="search")

# Send keyboard input
search_word = "okulary"
search_bar.send_keys(search_word)
search_bar.send_keys(Keys.ENTER)

# Wait for the searched phrase to load
wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-7ddzao')))

# Search for <a> elements, that contain the offer link, in the grid container
listing_grid_container = driver.find_elements(By.CSS_SELECTOR, value=".css-1sw7q4x a")

links = []

# Get "href" attribute from the <a> element
for grid_item in listing_grid_container:
    link = grid_item.get_attribute("href")
    print(link)
    links.append(link)


search_results = []

# Extract information about the offer
for link in links:
    driver.get(link)
    driver.implicitly_wait(3)
    offer_title = driver.find_element(By.CLASS_NAME, "css-1juynto").text
    offer_description = driver.find_element(By.CLASS_NAME, "css-1t507yq").text
    offer_date = driver.find_element(By.CLASS_NAME, "css-19yf5ek").text
    offer_seller = driver.find_element(By.CLASS_NAME, "css-1lcz6o7").text
    offer_seller_seniority = driver.find_element(By.CLASS_NAME, "css-16h6te1").text
    offer_localisation_city = driver.find_element(By.CLASS_NAME, "css-1cju8pu").text

    # html = driver.page_source

    # with open(f"/saved-pages/offer{page_num}.html", "w", encoding='utf-8') as f:
    #     f.write(driver.page_source)

    result = {'offer_title': offer_title,
              'offer_description': offer_description,
              'offer_date': offer_date,
              'offer_seller': offer_seller,
              'offer_seller_seniority': offer_seller_seniority,
              'offer_localisation_city': offer_localisation_city,
              'offer_time': datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

    search_results.append(result)

next_page_button = driver.find_element(By.CSS_SELECTOR, value="a[data-testid='pagination-forward']").get_attribute("href")

print(next_page_button)

driver.get(next_page_button)

# Save data to .csv file
# df = pd.DataFrame(search_results)
# df.to_csv('search_results.csv')

# Shutdown the entire browser
# driver.quit()
