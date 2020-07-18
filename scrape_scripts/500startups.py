from selenium import webdriver
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json
from time import sleep

"""
NOTES: 
"""

URL = "https://500.co/startups"
sectors = [
    "Fintech",
    "Health / Biotech",
    "HR / Education",
    "IT / Security",
    "Marketing / Customer Success",
    "Media / Collaboration",
    "Real Estate / Transportation",
    "Retail / eCommerce",
    "Smart Cities / Industrial"
]

platforms = [
    "Cloud / Content",
    "Direct sale",
    "Direct service",
    "Marketplace",
    "Mobile",
    "O2O",
    "On-demand / Delivery",
    "SaaS",
    "Token",
]

def get_company_data():
    companies = []
    tags = defaultdict(list)
    driver = webdriver.Chrome(executable_path="C:\\Program Files\\chromedriver.exe")
    for sector in tqdm(sectors, desc="Getting companies"):
        for platform in platforms:
            payload = {"filter":"1", "region":"", "sector":sector, "platform":platform}

            driver.get(requests.get(URL, params=payload).url)
            sleep(.5)
            soup = BeautifulSoup(driver.page_source, 'lxml')

            table = soup.find("table").find_all("tr")[1:]
            for tr in table:
                company = {}
                data = tr.find_all("td")
                name = data[0].text.strip().replace(" ", "-").replace("/", "-")
                website = data[1].find('a')['href']
                location = data[2].text.strip()
                tags[data[3].text.strip()].append(name)
                tags[data[4].text.strip()].append(name)
                company['name'] = name
                company['website'] = website
                company['location'] = location
                companies.append(company)
    driver.close()
    return companies, tags


def main():
    companies, tags = get_company_data()

    with open("..\\webapp\\outfiles\\tag_jsons\\tags.json", 'r') as existing_file:
        existing_tags = json.load(existing_file)
        existing_file.close()

    with open('..\\webapp\\outfiles\\company_jsons\\500-Startups.json', 'w') as outfile:
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
