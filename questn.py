import csv
import pandas as pd
from tqdm import tqdm
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_data(projects, new_scraped_writer, all_scraped_writer):
    for i, project in enumerate(tqdm(projects, desc='>> Projects Scraping')):
        data = {}

        try:
            data['Name'] = project.find_element(By.CSS_SELECTOR, 'p.WalsheimBold').text
        except:
            continue

        data['Report'] = project.get_attribute('href')

        if data['Report'] not in previous_reports:

            data['Website'] = ''
            
            data['Telegram'] = ''

            data['Twitter'] = ''

            data['Discord'] = ''

            new_scraped_writer.writerow(data)
            all_scraped_writer.writerow(data)
        else:
            continue

def scroll_to_end():
    last_project = driver.find_elements(By.CSS_SELECTOR, 'div.style_communityBox__kzFrj > a')[-1]
    driver.execute_script("arguments[0].scrollIntoView(true);", last_project)

    sleep(8)

def read_reports_from_csv():
    df = pd.read_csv("All_Scraped.csv")
    report_list = df["Report"].tolist()
    return report_list

previous_reports = read_reports_from_csv()

options = Options()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

url = 'https://app.questn.com/communities'

try:
    driver.get(url)
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.style_communityBox__kzFrj')))
except:
    driver.quit()
    exit()

header = ['Name', 'Report', 'Website','Telegram','Twitter','Discord']
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

    projects = driver.find_elements(By.CSS_SELECTOR, 'div.style_communityBox__kzFrj > a')
    print('>> Total Projects: ', len(projects))

    print('>> Project Scraping Started')
    get_data(projects, new_scraped_writer, all_scraped_writer)

driver.quit()