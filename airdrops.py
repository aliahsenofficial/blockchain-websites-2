import csv
import requests
import pandas as pd
from tqdm import tqdm
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def get_data(projects, new_scraped_writer, all_scraped_writer):
    for i, project in enumerate(tqdm(projects, desc='Projects Scraping')):
        if project not in previous_reports:
            data = {}

            try:
                response = requests.get(project)
                soup = BeautifulSoup(response.content, 'lxml')
            except:
                continue

            try:
                data['Name'] = soup.select_one('h1.entry-title').text
            except:
                continue
            try:
                data['Website'] = 'https://airdrops.io' + soup.select_one('div.airdrop-conv > p > a').get('href')
            except:
                data['Website'] = ''
            data['Report'] = project
            data['Telegram'] = ''
            data['Twitter'] = ''
            data['Discord'] = ''

            print('>> ', i+1, data['Report'])
            new_scraped_writer.writerow(data)
            all_scraped_writer.writerow(data)
        else:
            continue

def read_reports_from_csv():
    df = pd.read_csv("All_Scraped.csv")
    report_list = df["Report"].tolist()
    return report_list

previous_reports = read_reports_from_csv()

options = Options()
driver = webdriver.Chrome(options=options)

url = 'https://airdrops.io/latest/'
try:
    driver.get(url)
    sleep(10)
except:
    driver.quit()
    exit()
    
header = ['Name','Report','Website','Telegram','Twitter','Discord']
with open("All_Scraped.csv", mode='a', newline='', encoding='utf-8') as all_scraped_file, open("New_Scraped.csv", mode='a', newline='', encoding='utf-8') as new_scraped_file:
    new_scraped_writer = csv.DictWriter(new_scraped_file, fieldnames=header)
    all_scraped_writer = csv.DictWriter(all_scraped_file, fieldnames=header)

    for i in range(30):
        try:
            driver.find_element(By.CSS_SELECTOR, 'div.showmore > span').click()
            sleep(1)
        except:
            pass

    print(">> Scrolling Completed")
    
    projects = [project.get_attribute('href') for project in driver.find_elements(By.CSS_SELECTOR, 'div.air-content-front > a')]
    print('>> Total Projects: ', len(projects))
    
    
    print('>> Project Scraping Started')
    get_data(list(set(projects)), new_scraped_writer, all_scraped_writer)

driver.quit()