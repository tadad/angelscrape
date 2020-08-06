import scrapy
import scrapy_selenium
from selenium import webdriver
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json

class FiveHundredStartupsSpider(scrapy.Spider):
    name = "FiveHunderStartups"

    def parse(self, response):



def get_company_urls():
    pass


def get_company_data():
    companies = []
    tags = defaultdict(list)
    return companies, tags


def main():
    companies, tags = get_company_data(get_company_urls())

    with open("..\\webapp\\outfiles\\tag_jsons\\tags.json", 'r') as existing_file:
        existing_tags = json.load(existing_file)
        existing_file.close()

    with open('..\\webapp\\outfiles\\company_jsons\\FUND NAME.json', 'w') as outfile:
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
