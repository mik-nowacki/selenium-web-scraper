import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# TODO: Add /?page={page_num} instead
# TODO: Download html file of the offer
# TODO: Take a screenshot of the offer?
# TODO: Refactor results

ABSOLUTE_FILE_PATH = f"E:/Strony GIF/"  # CHANGE THIS ACCORDING TO YOUR LIKING


#  Set up a driver to use Chrome browser
def setup_chrome_driver():
    # Keep Chrome browser open after program finishes
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=chrome_options)


#  Go to a website of a given address and wait 100ms for it to load
def go_to_website(driver, address):
    driver.get(address)
    driver.implicitly_wait(100)


#  Accept cookies for convenience
def accept_cookies(driver):
    # Find the accept button and click it
    accept_btn = driver.find_element(By.ID, value="onetrust-accept-btn-handler")
    accept_btn.click()


#  Search for offers connected to a given keyword
def search_for_offers(driver, search_word):
    # Find the "Search" <input> by ID
    search_bar = driver.find_element(By.ID, value="search")

    # Send keyboard input
    search_bar.send_keys(search_word)
    search_bar.send_keys(Keys.ENTER)

    # Wait for the searched phrase to load
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-7ddzao')))


#  Extract title, description, date, seller name, how long the seller is offering services and the city
def scrape_offers(driver, search_results):
    links = []

    # Search for <a> elements, that contain the offer link, in the grid container
    listing_grid_container = driver.find_elements(By.CSS_SELECTOR, value=".css-1sw7q4x a")

    # Get "href" attribute from the <a> element
    for grid_item in listing_grid_container:
        link = grid_item.get_attribute("href")
        print(link)
        links.append(link)

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

        search_time = datetime.now().strftime("%d/%m/%Y %H:%M")

        result = {'offer_title': offer_title,
                  'offer_description': offer_description,
                  'offer_date': offer_date,
                  'offer_seller': offer_seller,
                  'offer_seller_seniority': offer_seller_seniority,
                  'offer_localisation_city': offer_localisation_city,
                  'search_time': search_time}

        search_results.append(result)

        # download_html(driver, ABSOLUTE_FILE_PATH + f"scraping {search_time}/{offer_title}.html")
        # download_html(driver, ABSOLUTE_FILE_PATH + f"/{offer_title}.html")


def download_html(driver, file_path):
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(driver.page_source)


def save_to_csv(search_results):
    # Save data to .csv file
    df = pd.DataFrame(search_results)
    df.to_csv('search_results.csv')


def main():
    driver = setup_chrome_driver()
    search_results = []

    # Specify a website you want to scrape
    go_to_website(driver, address="https://www.olx.pl/")

    accept_cookies(driver)

    search_for_offers(driver, search_word="botoks")

    next_page_button = driver.find_element(By.CSS_SELECTOR,
                                           value="a[data-testid='pagination-forward']").get_attribute("href")

    while True:
        try:

            scrape_offers(driver, search_results)

            print(next_page_button)

            driver.get(next_page_button)
            next_page_button = driver.find_element(By.CSS_SELECTOR,
                                                   value="a[data-testid='pagination-forward']").get_attribute("href")

        except NoSuchElementException:
            print("No more pages to scrape.")
            break

    save_to_csv(search_results)
    # Shutdown the entire browser
    driver.quit()


if __name__ == "__main__":
    main()
