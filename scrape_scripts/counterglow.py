import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from tqdm import tqdm

"""
READ THIS https://towardsdatascience.com/advanced-web-scraping-concepts-to-help-you-get-unstuck-17c0203de7ab

Possibilities: add a user-agent request header when you request certian data
"""

URL = "https://map.counterglow.org/farm/"



def get_data():
    num = 100020
    """
    look at this
    https://stackoverflow.com/questions/60017438/how-can-i-scrape-from-a-webpage-that-uses-javascript-to-load-in-elements-as-you
    """

    driver = webdriver.Chrome(executable_path="C:\\Program Files\\chromedriver.exe")

    for i in range(5):
        driver.get(URL + str(num))
        num = num + 1
        sleep(10)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        ul_data = soup.find_all("ul")
        if not ul_data:
            continue
        else:
            print(ul_data)

    driver.close()
def main():
    get_data()


if __name__ == "__main__":
    main()
