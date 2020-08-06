"""
TODO: GET THE TAGS FROM THE WEBPAGE (UNDER TOPICS)

INFO: This script can get the following data fields for each company from YC
    Name
    location
    Description
    Website
    Year founded
    Relevant (assumed)
    Dead (always false since we are pulling from jobs page)
    Original Pull

    Tags
"""


from selenium import webdriver
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
from time import sleep
import re
from datetime import date

URL = "https://jobs.initialized.com/companies"
BASE_URL = "https://jobs.initialized.com"


def get_company_urls():
    driver = webdriver.Chrome(executable_path="C:\\Program Files\\chromedriver.exe")
    driver.get(URL)
    sleep(1)
    driver.find_element_by_class_name("load-more").click()

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    soup = BeautifulSoup(driver.page_source, 'lxml')
    links = [co.find("a")["href"] for co in soup.find_all("div", {"class":"organization-card"})]
    driver.close()
    return links



def get_company_data(links):
    companies = []
    driver = webdriver.Chrome(executable_path="C:\\Program Files\\chromedriver.exe")
    regex = re.compile(r'Founded in (\d+)')
    for link in tqdm(links, desc="Getting company data"):
        company = {}
        driver.get(BASE_URL+link)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        sleep(.75)

        name = soup.find("h1", {"class":"name"}).text.strip()
        if not name:
            continue
        try:
            website = soup.find("div", {"ng-if":"organization.website_url"}).find("a")["href"]
        except AttributeError:
            website = None
        try:
            location = soup.find("div", {"class":"icon-row-locations"}).find("span").text.strip()
        except AttributeError:
            location = None
        try:
            description = soup.find("p", {"class": "description"}).text.strip()
        except AttributeError:
            description = None
        try:
            year_founded = regex.match(soup.find("div", {"ng-if":"organization.founded"}).find("div", {"class":"founded"}).text.strip()).group(1)
        except AttributeError:
            year_founded = None
        company['name'] = name
        company['location'] = location
        company['description'] = description
        company['website'] = website
        company['year_foudned'] = year_founded
        company['dead'] = False
        company['relevant'] = True
        company['original_pull'] = date.today().isoformat()
        companies.append(company)
    driver.close()
    return companies


def main():
    companies = get_company_data(get_company_urls())

    with open('..\\webapp\\outfiles\\company_jsons\\initialized.json', 'w') as outfile:
        json.dump(companies, outfile)



if __name__ == "__main__":
    main()
