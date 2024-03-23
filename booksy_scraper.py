from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import requests

def extract_links(raw_html):
    offer_links = []
    # process raw html using beautiful soup
    soup = BeautifulSoup(raw_html, 'html.parser')
    lis = soup.find_all('li')
    for li in lis:
        div1 = li.find('div')
        if div1 is not None: # ugly, maybe there is some more elegant way, TODO refactor
            div2 = div1.find('div')
            if div2 is not None:
                a = div2.find('a')
                if a is not None:
                    href = a.get('href')
                    offer_links.append(href)
    return offer_links

# starts from main booksy page, accepts cookies, enters search phrase and goes to first page with offers
# returns current page number = 1
def goto_first_offers_page_html(driver, search_phrase='botoks', starting_url="https://booksy.com/pl-pl/"):
    driver.get(starting_url)
    accept_cookies = driver.find_element(By.ID, value="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    accept_cookies.click()
    driver.find_element(By.CSS_SELECTOR, ".b-w-100p > .b-dropdown .b-form-control").click()
    driver.find_element(By.CSS_SELECTOR, ".b-w-100p > .b-dropdown .b-form-control").send_keys(search_phrase)
    driver.find_element(By.CSS_SELECTOR, ".b-w-100p > .b-dropdown .b-form-control").send_keys(Keys.ENTER)
    return 1 # current page number

# extracts html from the first page with offers - a div containing list of offers
def get_offers_html(driver):
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.ID, 'search-results')))
    raw_offers_html = driver.find_element(By.ID, "search-results").get_attribute('innerHTML')
    return raw_offers_html

# creates and returns an initial driver object
def get_driver(type='Chrome'):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    if type == 'Chrome':
        driver = webdriver.Chrome(options=chrome_options)
    return driver

# goes to the next page with offers and returns the new current page number
def enter_next_page(driver, current_page_number):
    current_page_number += 1
    wait = WebDriverWait(driver, 15)  # Adjust the timeout as needed
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, str(current_page_number)))).click()
    return current_page_number

# goes through specified number of pages with offers and extracts links to the offers
def get_links_from_n_pages(driver, offer_links, n=3):
    curr_page_num = goto_first_offers_page_html(driver)
    for x in range(n):
        curr_page_num = enter_next_page(driver, curr_page_num)
        time.sleep(3)
        raw_html = get_offers_html(driver)
        links = extract_links(raw_html)
        offer_links.extend(links)
        time.sleep(3)
    return offer_links


# TODO get time of visit
# TODO get listed employees
# TODO automatically make screenshot of the page ?
# extracts business name and address from the offer page
def extract_info_from_offer(driver, offer_address, base_url='https://booksy.com'):
    url = base_url + offer_address
    driver.get(url)
    driver.implicitly_wait(3)
    raw_html = driver.page_source
    soup = BeautifulSoup(raw_html, 'html.parser')
    business_name = soup.find('div', {'data-testid': 'business-name'}).get_text(strip=True)
    business_address = soup.find('div', {'data-testid': 'map-location-business-address'}).get_text(strip=True)
    return {'business_name': business_name, 'business_address': business_address}

offer_links = []
driver = get_driver(type='Chrome')
links = get_links_from_n_pages(driver, offer_links, 3)

links

extract_info_from_offer(driver, '/pl-pl/215062_beauty-boutique-bb_medycyna-estetyczna_3_warszawa#ba_s=sr_1')