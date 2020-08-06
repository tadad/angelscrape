"""
TODO: Ajdust stages in get_company_urls() to get everything, and then add relevant/dead fields, rather than just only getting the relevant ones

INFO: This script can get the following data fields for each company from YC
    Name
    Description
    location
    Website
    Year founded
    Team Size

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
from collections import defaultdict
import json
from datetime import date
import time

PORTFOLIO_URL = "https://sosv.com/portfolio/"
BASE_URL = "https://sosv.com"

def get_company_urls(stages=["Accelerator","Seed","Pre-seed"]):
    stages = ",".join(stages)
    payload= {"stage":stages, "page":"1"}
    r = requests.get(PORTFOLIO_URL, params=payload)
    driver = webdriver.Chrome(executable_path="C:\\Program Files\\chromedriver.exe")
    driver.get(r.url)
    sleep(.5)

    # getting max page number so we can loop through it
    driver.find_element_by_class_name("ais-pagination__item--last").click()

    pages = int(driver.current_url[len(driver.current_url)-2:]) # implicit assumption that it is two digit...fix maybe...
    links = set()
    for page in tqdm(range(1, pages+1), desc="Getting links"):
        payload = {"stage":stages, "page":page}
        driver.get(requests.get(PORTFOLIO_URL, params=payload).url)
        soup = BeautifulSoup(driver.page_source, "lxml")
        sosv_cards = soup.find_all("div", {"class":["card", "sosv-card"]})
        for card in sosv_cards:
            links.add(card.find("a", {"class":"card-body"})['href'])
    driver.close()
    return list(links)


def get_company_data(links):
    companies = []
    tags = defaultdict(list)
    #driver = webdriver.Chrome(executable_path="C:\\Program Files\\chromedriver.exe")
    for link in tqdm(links, desc="Gettting company data"):
        company = {}
        try:
            t0 = time.time()
            r = requests.get(BASE_URL + link)

            soup = BeautifulSoup(r.content, 'lxml')
            t1 = time.time()
            print(t1 - t0)

            # driver.get(BASE_URL + link)
            # soup = BeautifulSoup(driver.page_source, 'lxml')

            portfolio_header = soup.find("div", {"class": "portfolio-header"})
            name = portfolio_header.find("h1").text
            description = portfolio_header.find("h3").text
            right_col = soup.find("div", {"class": "company-dingbats"})
            page_tags = right_col.find_all("svg", {"data-icon":"tag"})
            location = right_col.find("svg", {"data-icon":"flag"}).parent.text
            website = right_col.find("svg", {"data-icon":"globe"}).parent.text.strip()

            company["name"] = name
            company["description"] = description.strip()
            company["location"] = location.strip()
            company["website"] = website
            company["original_pull"] = date.today().isoformat()
            company["relevant"] = True
            company["dead"] = False

            try:
                accelerator = right_col.find("svg", {"data-icon":"power-off"}).parent.text.strip()
            except:
                #print("{0} didn't go through an accelerator".format(name))
                pass
            try:
                for tag in page_tags:
                    tags[tag.parent.text.strip()].append(company["name"])
                tags[accelerator].append(company["name"])
            except:
                print("No tags for ", name)
            companies.append(company)
        except:
            print("Something went wrong trying to access " + BASE_URL + link)
    return companies, tags


def main():
    companies, tags = get_company_data(get_company_urls())

    with open("..\\webapp\\outfiles\\tag_jsons\\tags.json", 'r') as existing_file:
        existing_tags = json.load(existing_file)
        existing_file.close()

    with open('..\\webapp\\outfiles\\company_jsons\\SOSV.json', 'w') as outfile:
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
