"""
TODO: Funding info is sometimes just a round date. Mark irrelevant if they haven't gotten funding since 2016

Info:
    Relevant
    Dead
    Name
    Description
    Website
    Location
    Size
    Total Raised
    Original Pull

    Tags
"""


from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from tqdm import tqdm
import re
from collections import defaultdict
import json
from datetime import date

URL = "https://angel.co/"

ANGELS = {
    "Julia_Dewahl":"u/julia-dewahl",
    "Elad_Gil":"p/eladgil",
    "Jude_Gomila":"p/gomila",
    "Gaurav_Jain":"p/gaurav-jain-1",
    "Max_Levchin":"p/mlevchin",
    "Ben_Ling":"p/bling0",
    "Alexis_Ohanian":"p/alexisohanian",
}

def get_company_urls(angels, captcha=True):
    driver = webdriver.Chrome(executable_path="C:\\Program Files\\chromedriver.exe")

    angel_urls = {}
    for angel in angels:
        angel_urls[angel] = []
        driver.get(URL + angels[angel])

        if captcha:
            captcha_status = input("\nPress enter when you have finished solving the CAPTCHA. \n If there are no more CAPTCHAs, press 'n': ")
            if captcha_status == 'n':
                captcha = False
        else:
            sleep(10)

        try:
            driver.find_element_by_class_name("more_button").click()
        except:
            pass
        soup = BeautifulSoup(driver.page_source, "lxml")
        investments = soup.find_all("div", {"class":"investment"})

        for investment in investments:
            if investment.find("div", {"class":"copy"}):
                angel_urls[angel].append(investment.find("a")["href"])
    driver.close()
    return angel_urls


def get_company_data(angel_urls, captcha=True):
    companies = {}
    tags = defaultdict(list)
    driver = webdriver.Chrome(executable_path="C:\\Program Files\\chromedriver.exe")
    for angel in angel_urls.keys():
        this_angels_companies = []
        for investment in tqdm(angel_urls[angel], desc="Getting company data from " + angel):
            company = {}
            driver.get(investment)
            if captcha:
                captcha_status = input(
                    "\nPress enter when you have finished solving the CAPTCHA.\nIf there are no more CAPTCHAs, press 'n': ")
                if captcha_status == 'n':
                    captcha = False
            soup = BeautifulSoup(driver.page_source, 'lxml')

            # Checking if the company is too late stage for us
            if soup.find_all(text="Latest round"):
                funding = soup.find("span", text="Latest round").parent.find("h4").text
                series_re = re.compile(r"Series.*|IPO.*|Acquired.*")
                company["relevant"] = False if (series_re.match(funding) is not None) else True
            else:
                company['relevant'] = True
            company["dead"] = True if soup.find("span", {"class":"closedFlair_a3c49"}) is not None else False

            # Getting the data
            try:
                aside = soup.find("aside", {"class": "sidebar_ffba9"}).find("dl")
                if not aside:
                    continue

                name = soup.find("h1").text.strip()
                company["name"] = name
                description = soup.find("h2").text
                company["description"] = description

                aside_titles = [aside.find_all("dd")[i].text for i in range(len(aside.find_all("dd")))]
                aside_values = aside.find_all("dt")
                for i in range(len(aside_titles)):
                    if aside_titles[i]=="Website":
                        company["website"] = aside_values[i].find("a")["href"]
                    elif re.match(r"Location[s]?", aside_titles[i]):
                        company["location"] = aside_values[i].find_all("li")[0].text
                    elif aside_titles[i]=="Company size":
                        team_range = [int(aside_values[i].text.split()[0].split("-")[j]) for j in range(2)]
                        company["team_size"] = sum(team_range)//2
                    elif aside_titles[i]=="Total raised":
                        company["total_raised"] = aside_values[i].text
                    elif aside_titles[i]=="Markets":
                        for tag in aside_values[i].find_all("a"):
                            tags[tag.text].append(name)
                company["original_pull"] = date.today().isoformat()
                this_angels_companies.append(company)
            except:
                print("There was an error scraping ", investment)
        companies[angel] = this_angels_companies
    driver.close()
    return companies, tags


def main():
    companies, tags = get_company_data(get_company_urls(ANGELS))


    with open("..\\webapp\\outfiles\\tag_jsons\\tags.json", 'r') as existing_file:
        existing_tags = json.load(existing_file)
        existing_file.close()
    for angel in companies.keys():
        with open('..\\webapp\\outfiles\\company_jsons\\' + angel + '.json', 'w') as outfile:
            json.dump(companies[angel], outfile)

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


if __name__=="__main__":
    main()
