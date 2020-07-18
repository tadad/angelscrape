from selenium import webdriver
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json

"""
NOTES: This script is strictly for crossreferencing companies that we are already interested in.
       Crunchbase has way too much data to scrape all of it.
"""

def get_company_urls():
    pass


def get_company_data():
    companies = []
    tags = defaultdict(list)
    return companies, tags


def main():
    companies, tags = get_company_data(get_company_urls())

if __name__ == "__main__":
    main()
