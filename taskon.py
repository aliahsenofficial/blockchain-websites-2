import csv
import pandas as pd
from tqdm import tqdm
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scroll_to_end():
    last_project = driver.find_elements(By.CSS_SELECTOR, 'a.space-item-view')[-1]
    driver.execute_script("arguments[0].scrollIntoView(true);", last_project)
    sleep(5)

def read_reports_from_csv():
    df = pd.read_csv("All_Scraped.csv")
    report_list = df["Report"].tolist()
    return report_list

previous_reports = read_reports_from_csv()

options = Options()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

url = 'https://taskon.xyz/space'

try:
    driver.get(url)
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.space-item-view')))
except:
    driver.quit()
    exit()

header = ['Name','Report','Website','Telegram','Twitter','Discord']
with open("All_Scraped.csv", mode='a', newline='', encoding='utf-8') as all_scraped_file, open("New_Scraped.csv", mode='a', newline='', encoding='utf-8') as new_scraped_file:
    new_scraped_writer = csv.DictWriter(new_scraped_file, fieldnames=header)
    all_scraped_writer = csv.DictWriter(all_scraped_file, fieldnames=header)

    print(">> Scrolling Started")
    i = 1
    projects = []
    while True:
        if i == 75:
            break
        
        old_page = driver.page_source
        try:
            scroll_to_end()
        except:
            break
        new_page = driver.page_source
        i+=1

        # If there is no change in the page source, we have reached the end of the content
        if old_page == new_page:
            break
    
    print(">> Scrolling Completed")
    
    projects = driver.find_elements(By.CSS_SELECTOR, 'a.space-item-view')
    print('>> Total Projects: ', len(projects))

    
    print('>> Project Scraping Started')
    for i, project in enumerate(tqdm(projects, desc='Projects Scraping')):
        data = {}

        data['Report'] = project.get_attribute('href')

        if data['Report'] not in previous_reports:
            data['Name'] = project.text.split('\n')[0]
            data['Website'] = ''
            data['Telegram'] = ''
            data['Twitter'] = ''
            data['Discord'] = ''

            new_scraped_writer.writerow(data)
            all_scraped_writer.writerow(data)
        else:
            continue

driver.quit()