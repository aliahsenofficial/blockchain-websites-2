import csv
import pandas as pd
from tqdm import tqdm
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def read_reports_from_csv():
    df = pd.read_csv("All_Scraped.csv")
    report_list = df["Report"].tolist()
    return report_list

def get_data(projects, new_scraped_writer, all_scraped_writer):
    for i, project in enumerate(tqdm(projects, desc='Projects Scraping')):
        data = {}
        data['Report'] = project.get_attribute('href')

        if data['Report'] not in previous_reports:
            data['Name'] = project.find_element(By.CSS_SELECTOR, 'h2.title').text
            
            links = project.find_elements(By.XPATH, './/div[2]/a')
            for link in links:
                style = link.get_attribute('style')
                
                if ('color: rgb(26, 26, 26);' == style):
                    data['Website'] = link.get_attribute('href')

                elif ('color: rgb(28, 187, 239);' == style):
                    data['Telegram'] = link.get_attribute('href')

                elif ('color: rgb(28, 186, 236);' == style):
                    data['Twitter'] = link.get_attribute('href')

                elif ('color: rgb(88, 101, 242);' == style):
                    data['Discord'] = link.get_attribute('href')

            if 'Website' not in data:
                data['Website'] = ''
            elif 'Telegram' not in data:
                data['Telegram'] = ''
            elif 'Twitter' not in data:
                data['Twitter'] = ''
            elif 'Discord' not in data:
                data['Discord'] = ''

            new_scraped_writer.writerow(data)
            all_scraped_writer.writerow(data)
        else:
            continue

options = Options()
driver = webdriver.Chrome(options=options)

url = 'https://giveaway.com/sponsor'

try:
    driver.get(url)
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.inner')))
except:
    driver.quit()
    exit()

previous_reports = read_reports_from_csv()

header = ['Name','Report','Website','Telegram','Twitter','Discord']
with open("All_Scraped.csv", mode='a', newline='', encoding='utf-8') as all_scraped_file, open("New_Scraped.csv", mode='a', newline='', encoding='utf-8') as new_scraped_file:
    new_scraped_writer = csv.DictWriter(new_scraped_file, fieldnames=header)
    all_scraped_writer = csv.DictWriter(all_scraped_file, fieldnames=header)

    next_button = driver.find_element(By.CSS_SELECTOR, 'button.pagination__btn.next')
    
    projects = []
    while 'disabled' not in next_button.get_attribute('class'):
        projects.extend(driver.find_elements(By.CSS_SELECTOR, 'a.sc-64ff9a54-1.fhJBXs.card'))

        try:
            next_button.click()
            sleep(3)
        except:
            break

    print(">> Scrolling Completed")

    projects = driver.find_elements(By.CSS_SELECTOR, 'a.sc-64ff9a54-1.fhJBXs.card')
    print('>> Total Projects: ', len(projects))

    print('>> Project Scraping Started')
    get_data(projects, new_scraped_writer, all_scraped_writer)
    
driver.quit()