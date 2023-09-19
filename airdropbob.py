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
    for i, project in enumerate(tqdm(projects, desc='Projects Scrapping')):
        if project not in previous_reports:
            data = {}
            
            try:
                response = requests.get(project)
                soup = BeautifulSoup(response.content, 'lxml')
            except:
                continue
            try:
                data['Name'] = soup.select_one('div.provider-name').text
            except:
                continue
            try:
                data['Website'] = soup.select_one('a.btn.btn-secondary.btn-block').get('href')
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
driver.maximize_window()

url = 'https://www.airdropbob.com/'

try:
    driver.get(url)
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, 'resultsRow')))
except:
    driver.quit()
    exit()

header = ['Name','Report','Website','Telegram','Twitter','Discord']
with open("All_Scraped.csv", mode='a', newline='', encoding='utf-8') as all_scraped_file, open("New_Scraped.csv", mode='a', newline='', encoding='utf-8') as new_scraped_file:
    new_scraped_writer = csv.DictWriter(new_scraped_file, fieldnames=header)
    all_scraped_writer = csv.DictWriter(all_scraped_file, fieldnames=header)

    try:
        next_button = driver.find_elements(By.CSS_SELECTOR, 'a.page-link')[-1]
    except:
        driver.quit()
        exit()
        
    projects = []
    i = 1
    while 'disabled' not in next_button.get_attribute('class'):
        temp = [i.get_attribute('href') for i in driver.find_elements(By.CSS_SELECTOR, 'div.col-md-4 > a')]
        try:
            temp.pop(4)
            try:
                temp.pop(9)
            except:
                pass
        except:
            pass

        try:
            driver.execute_script("window.scrollBy(0, 1200);")
            sleep(1)

            next_button = driver.find_elements(By.CSS_SELECTOR, 'a.page-link')[-1]
            next_button.click()
            sleep(5)
        except: 
            continue
        
        projects.extend(temp)
        
        next_button = driver.find_elements(By.CSS_SELECTOR, 'a.page-link')[-1]
        
        i+=1

    temp = [i.get_attribute('href') for i in driver.find_elements(By.CSS_SELECTOR, 'div.col-md-4 > a')]
    try:
        temp.pop(4)
        try:
            temp.pop(9)
        except:
            pass
    except:
        pass
    projects.extend(temp)
    print(">> Scrolling Completed")
    
    # projects = [project.get_attribute('href') for project in projects]
    print(">> Total Projects: ", len(projects))

    # print('>> Project Scraping Started')
    get_data(projects, new_scraped_writer, all_scraped_writer)

driver.quit()