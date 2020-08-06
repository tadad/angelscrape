"""
TODO:

Info:
    Name
    Decription
    Location
    Website
    Relevant
    Dead (assumed)

    Tags
"""

import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json
from datetime import date

URL = "https://afore.vc/#!/portfolio"

def get_company_data():
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'lxml')
    tags = defaultdict(list)
    companies = []
    for li in soup.find("section", {"id": "portfolio"}).find_all("li"):
        company = {}
        if li.find("span", {"class":"acquired"}):
            company["relevant"] = False
        else:
            company["relevant"] = True
        name = li.find("h3")
        if name.text.strip() == "Stealth":
            continue
        name = name.find("a", {"target":"_blank"}).text.strip()
        info = [x.strip() for x in li.find("aside").text.split("\n") if x]
        location = info[0]
        tag = info[1]
        website = li.find("h3").find("a")['href']
        description = li.find("p").text.strip()

        company["name"] = name
        company["description"] = description.strip()
        company["location"] = location.strip()
        company["dead"] = False
        company["website"] = website
        company["original_pull"] = date.today().isoformat()

        tags[tag].append(name)
        companies.append(company)

    return companies, tags


def main():
    companies, tags = get_company_data()

    with open("..\\webapp\\outfiles\\tag_jsons\\tags.json", 'r') as existing_file:
        existing_tags = json.load(existing_file)
        existing_file.close()

    with open('..\\webapp\\outfiles\\company_jsons\\Afore-Capital.json', 'w') as outfile:
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
