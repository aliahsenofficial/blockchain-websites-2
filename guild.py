import csv
import requests
import pandas as pd
from tqdm import tqdm
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_data(projects, new_scraped_writer, all_scraped_writer):
    for i, project in enumerate(tqdm(projects, desc='Projects Scraping')):
        if project not in previous_reports:
            data = {}
            try:
                r = requests.get(project)
                soup = BeautifulSoup(r.content, 'lxml')
            except:
                continue
            
            try:
                data['Name'] = soup.select_one('h1.chakra-heading').text
            except:
                continue

            data['Report'] = project
            data['Telegram'] = ''
            data['Discord'] = ''
            
            logos = ['M128,88c0-22,18.5-40.3,40.5-40a40,40,0,0,1,36.2,24H240l-32.3,32.3A127.9,127.9,0,0,1,80,224c-32,0-40-12-40-12s32-12,48-36c0,0-64-32-48-120,0,0,40,40,88,48Z', 
                     'M49.6,183.4l12.1-7.3a8.4,8.4,0,0,0,3.8-6.1l3.7-37a7.3,7.3,0,0,1,1.2-3.5L90.1,98.6A8,8,0,0,1,102,96.8l15.4,12.9a7.8,7.8,0,0,0,6.2,1.8l31.2-4.2a7.8,7.8,0,0,0,4.9-2.7L181.9,79a8.1,8.1,0,0,0,1.9-5.6l-1.1-24.3'
                    ]
            try:
                websites = soup.select('ul.chakra-wrap__list > div')
                for website in websites:
                    if logos[0] == website.select_one('ul > div > div > svg > path').get('d'):
                        data['Website'] = website.select_one('a').get('href')
                    elif logos[1] == website.select_one('ul > div > div > svg > path').get('d'):
                        data['Twitter'] = website.select_one('a').get('href')
            except:
                data['Website'] = ''
                data['Twitter'] = ''
            
            if 'Website' not in data:
                data['Website'] = ''
            elif 'Twitter' not in data:
                data['Twitter'] = ''
                
            new_scraped_writer.writerow(data)
            all_scraped_writer.writerow(data)
        else:
            continue

def scroll_to_end():
    last_project = driver.find_elements(By.CSS_SELECTOR, 'a.chakra-link')[-1]
    driver.execute_script("arguments[0].scrollIntoView(true);", last_project)

    sleep(3)

def read_reports_from_csv():
    df = pd.read_csv("All_Scraped.csv")
    report_list = df["Report"].tolist()
    return report_list

previous_reports = read_reports_from_csv()

options = Options()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

url = 'https://guild.xyz/explorer?order=NEWEST'

try:
    driver.get(url)
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.chakra-link')))
except:
    driver.quit()
    exit()

header = ['Name', 'Report', 'Website', 'Telegram', 'Twitter', 'Discord']
with open("All_Scraped.csv", mode='a', newline='', encoding='utf-8') as all_scraped_file, open("New_Scraped.csv", mode='a', newline='', encoding='utf-8') as new_scraped_file:
    new_scraped_writer = csv.DictWriter(new_scraped_file, fieldnames=header)
    all_scraped_writer = csv.DictWriter(all_scraped_file, fieldnames=header)

    print(">> Scrolling Started")
    i = 1
    while True:
        i+=1
        old_page = driver.page_source
        try:
            scroll_to_end()
        except:
            break
        new_page = driver.page_source

        # If there is no change in the page source, we have reached the end of the content
        if old_page == new_page:
            break
    
    print(">> Scrolling Completed")
    
    projects = [project.get_attribute('href') for project in driver.find_elements(By.CSS_SELECTOR, 'a.chakra-link')]
    print('>> Total Projects: ', len(projects))

    print('>> Project Scraping Started')
    get_data(projects, new_scraped_writer, all_scraped_writer)

driver.quit()