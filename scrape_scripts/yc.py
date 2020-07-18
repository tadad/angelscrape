import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from tqdm import tqdm
import json
from datetime import date
from collections import defaultdict

PORTFOLIO_URL = "https://www.ycombinator.com/companies/"
BASE_URL = "https://www.ycombinator.com"
SCROLL_PAUSE_TIME = 0.5

def get_company_urls(batch=["S20", "W20", "S19", "W19"], status="active"):
    payload = {"status":status, "batch":batch}
    driver = webdriver.Chrome(executable_path="C:\\Program Files\\chromedriver.exe")
    driver.get(requests.get(PORTFOLIO_URL, params=payload).url)

    # Scrolling Loop
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'lxml')
    right_content = soup.find_all("a", {"class":"_3FfkL2cvyxXTDzOIMrMwry"})

    links = []
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
        name = soup.find("div", {"class":"main-box"}).find("h1").text.strip().replace(" ", "-")
        description = soup.find("div", {"class":"main-box"}).find("p").text.strip()
        facts = soup.find("div", {"class":"highlight-box"}).find("div", {"class":"facts"}).find_all("div")

        company["name"] = name
        company["description"] = description
        company["website"] = soup.find_all("div", {"class": "links"})[1].find("a")["href"]
        company["year_founded"] = int(facts[0].find("span").text) if facts[0].find("span").text else None
        company["team_size"] = int(facts[1].find("span").text) if facts[1].find("span").text else None
        company["original_pull"] = date.today().isoformat()
        company["location"] = facts[2].find("span").text
        companies.append(company)

        program = soup.find("div", {"class": "main-box"}).find("span", {"class": "pill"}).text
        page_tags = soup.find("div", {"class": "main-box"}).find("div", {"class": "flex-row"}).find_all("div")[
                   1].find_all("span")[1:]

        for tag in page_tags:
            tags[tag.text].append(company["name"])
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
