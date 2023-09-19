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
                data['Name'] = soup.select_one('h1.pb-2.mb-0.mt-0.mt-lg-2.h4.pl-2.pl-md-0 > span').text
            except:
                continue
            try:
                data['Website'] = soup.select_one('a.btn.btn-link.my-auto.px-2').get('href')
            except:
                data['Website'] = ''
            data['Report'] = project
            data['Telegram'] = ''
            data['Twitter'] = ''
            data['Discord'] = ''

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

header = ['Name','Report','Website','Telegram','Twitter','Discord']
with open("All_Scraped.csv", mode='a', newline='', encoding='utf-8') as all_scraped_file, open("New_Scraped.csv", mode='a', newline='', encoding='utf-8') as new_scraped_file:
    new_scraped_writer = csv.DictWriter(new_scraped_file, fieldnames=header)
    all_scraped_writer = csv.DictWriter(all_scraped_file, fieldnames=header)

    links = [   'https://airdropking.io/en/', 
                'https://airdropking.io/en/best-airdrops/', 
                'https://airdropking.io/en/high-value-airdrops/', 
                'https://airdropking.io/en/ending-soon-airdrops/'
            ]

    projects = []
    for link in links:
        try:
            driver.get(link)
            sleep(10)
        except:
            continue

        for project in driver.find_elements(By.CSS_SELECTOR, 'div > a.list_item'):
            if project not in previous_reports:
                if '/go/' not in project.get_attribute('href'):
                    projects.append(project.get_attribute('href'))

    print(">> Scrolling Completed")
    
    print('>> Total Projects: ', len(list(set(projects))))


    print('>> Project Scraping Started')
    get_data(list(set(projects)), new_scraped_writer, all_scraped_writer)

driver.quit()