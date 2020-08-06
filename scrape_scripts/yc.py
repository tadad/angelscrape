"""
TODO: refactor with scrapy

INFO: This script can get the following data fields for each company from YC
    Name
    Description
    Website
    Year founded
    Team Size
    location
    Relevant (IPO/Acquired/Dead)
    Dead
    Original Pull

    Tags
"""

import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from tqdm import tqdm
import json
from datetime import date
from collections import defaultdict
import re
from unidecode import unidecode

PORTFOLIO_URL = "https://www.ycombinator.com/companies/"
BASE_URL = "https://www.ycombinator.com"

BATCHES = [
            ["S20", "W20"],
            ["S19", "S18", "S17","W19", "W18", "W17"],
            ["S16", "S15", "S14", "S13", "S12", "S11", "W16", "W15", "W14", "W13", "W12", "W11"],
            ["S10", "S09", "S08", "S07", "S06", "S05", "W10", "W09", "W08", "W07", "W06", "W05"],
]

def get_company_urls():
    driver = webdriver.Chrome(executable_path="C:\\Program Files\\chromedriver.exe")
    links = []

    for batch_list in BATCHES:
        payload = {"batch":batch_list}
        driver.get(requests.get(PORTFOLIO_URL, params=payload).url)

        # Scrolling Loop
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(.5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(driver.page_source, 'lxml')
        right_content = soup.find_all("a", {"class":"SharedDirectory-module__company___AVmr6"})

        for right in right_content:
            links.append(right['href'])
    driver.close()
    return links


def get_company_data(links):
    tags = defaultdict(list)
    companies = []
    for link in tqdm(links, desc="Getting company data"):
        company = {}
        r = requests.get(BASE_URL + link)
        soup = BeautifulSoup(r.content, 'lxml')
        name = soup.find("div", {"class":"main-box"}).find("h1").text.strip()
        description = soup.find("div", {"class":"main-box"}).find("p").text.strip()
        highlight_box = soup.find("div", {"class":"highlight-box"}).find("div", {"class":"facts"}).find_all("div")

        company["name"] = unidecode(name)
        company["description"] = description
        company["website"] = soup.find_all("div", {"class": "links"})[1].find("a")["href"]
        company["year_founded"] = int(highlight_box[0].find("span").text) if highlight_box[0].find("span").text else None
        company["team_size"] = int(highlight_box[1].find("span").text) if highlight_box[1].find("span").text else None
        company["location"] = highlight_box[2].find("span").text if highlight_box[2].find("span").text else None
        company["original_pull"] = date.today().isoformat()

        program = soup.find("div", {"class": "main-box"}).find("span", {"class": "pill"}).text
        page_tags = [tag.text for tag in soup.find("div", {"class": "main-box"}).find("div", {"class": "flex-row"}).find_all("div")[
                   1].find_all("span")[1:]]

        all_tags = "|".join(page_tags)

        r = re.compile(r'.*(Acquired|Public).*')
        if r.match(all_tags) is not None:
            company['relevant'] = False
            page_tags.remove(re.match(r'.*(Acquired|Public).*', all_tags).group(1))
        else:
            company['relevant'] = True
        r = re.compile(r'YC-[SW](\d{2})')
        if r.match(all_tags) is not None:
            if int(r.match(all_tags).group(1)) < 17:
                company['relevant'] = False
        r = re.compile(r'.*(Inactive).*')
        if r.match(all_tags) is not None:
            company['dead'] = True
            company['relevant'] = False
            page_tags.remove("Inactive")
        else:
            company['dead'] = False
        if company['dead'] is None or company['relevant']is None:
            print("Something is wrong with ", company['name'])
        companies.append(company)

        for tag in page_tags:
            tags[tag].append(company["name"])
        tags["YC-" + program].append(company["name"])
    return companies, tags


def main():
    companies, tags = get_company_data(get_company_urls())

    with open("..\\webapp\\outfiles\\tag_jsons\\tags.json", 'r') as existing_file:
        existing_tags = json.load(existing_file)
        existing_file.close()

    with open('..\\webapp\\outfiles\\company_jsons\\YC.json', 'w') as outfile:
        json.dump(companies, outfile)

        for tag in tags.keys():
            try:
                for company in tags[tag]:
                    if existing_tags[tag].contains(company):
                        continue
                    existing_tags[tag].append(company)
            except:
                existing_tags[tag] = tags[tag]
    with open("..\\webapp\\outfiles\\tag_jsons\\tags.json", 'w') as existing_file:
        json.dump(existing_tags, existing_file)


if __name__ == "__main__":
    main()
