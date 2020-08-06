"""
TODO:

INFO:
    Name
    Relevant (assumed)
    Dead (assumed)
    Website
    Original Pull

    Tags
"""


import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json
from datetime import date

URL = "https://boxgroup.com/#investments"

def get_company_data():
    companies = []
    tags = defaultdict(list)

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'lxml')
    investments = soup.find("div", {"class":"investments-list"}).find_all("div", {"class":"investments-list-item"})
    for investment in investments:
        company = {}
        link = investment.find('a')
        name = link["id"].strip()
        website = link["href"]
        page_tags = investment["data-category"].split(',')

        company["name"] = name
        company["website"] = website
        company['dead'] = False
        company['relevant'] = True
        company["original_pull"] = date.today().isoformat()

        for tag in page_tags:
            tags[tag.replace("_", " ")].append(name)
        companies.append(company)
    return companies, tags


def main():
    companies, tags = get_company_data()

    with open("..\\webapp\\outfiles\\tag_jsons\\tags.json", 'r') as existing_file:
        existing_tags = json.load(existing_file)
        existing_file.close()

    with open('..\\webapp\\outfiles\\company_jsons\\BoxGroup.json', 'w') as outfile:
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
