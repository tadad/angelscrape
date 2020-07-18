from selenium import webdriver
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json
from datetime import date

URL = "https://www.refactor.com/portfolio"

def get_company_data():
    companies = []
    tags = defaultdict(list)
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'lxml')
    summary_items = soup.find_all("div", {"class":"summary-item"})
    for summary in summary_items:
        company = {}
        name = summary.find("div", {"class":"summary-title"}).text.strip().replace(" ", "-")
        website = summary.find("div", {"class": "summary-title"}).find("a")['href']
        description = summary.find("div", {"class":"summary-excerpt"}).text.strip()
        company["name"] = name
        company["website"] = website
        company["description"] = description
        company["original_pull"] = date.today().isoformat()

        page_tags = summary.find("div", {"class":"summary-metadata-container"}).find_all("span", {"class":"summary-metadata-item"})
        for tag in page_tags:
            tags[tag.text].append(name)
        companies.append(company)
    return companies, tags


def main():
    companies, tags = get_company_data()

    with open("..\\webapp\\outfiles\\tag_jsons\\tags.json", 'r') as existing_file:
        existing_tags = json.load(existing_file)
        existing_file.close()

    with open('..\\webapp\\outfiles\\company_jsons\\Refactor-Capital.json', 'w') as outfile:
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
