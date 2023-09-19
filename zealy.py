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
    for i, project in enumerate(tqdm(projects, desc='Projects Scraping')):
        if project not in previous_reports:
            data = {}

            try:
                driver.get(project)
                element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.css-1qvd2xe > a')))
            except:
                continue
            
            try:
                data['Name'] = driver.find_element(By.CSS_SELECTOR, 'h2.chakra-heading.css-1jb3vzl').text
                data['Report'] = project
                data['Telegram'] = ''
            except:
                continue
            
            logos = ['M4.715 6.542 3.343 7.914a3 3 0 1 0 4.243 4.243l1.828-1.829A3 3 0 0 0 8.586 5.5L8 6.086a1.002 1.002 0 0 0-.154.199 2 2 0 0 1 .861 3.337L6.88 11.45a2 2 0 1 1-2.83-2.83l.793-.792a4.018 4.018 0 0 1-.128-1.287z', 'M492 109.5c-17.4 7.7-36 12.9-55.6 15.3 20-12 35.4-31 42.6-53.6-18.7 11.1-39.4 19.2-61.5 23.5C399.8 75.8 374.6 64 346.8 64c-53.5 0-96.8 43.4-96.8 96.9 0 7.6.8 15 2.5 22.1-80.5-4-151.9-42.6-199.6-101.3-8.3 14.3-13.1 31-13.1 48.7 0 33.6 17.2 63.3 43.2 80.7-16-.4-31-4.8-44-12.1v1.2c0 47 33.4 86.1 77.7 95-8.1 2.2-16.7 3.4-25.5 3.4-6.2 0-12.3-.6-18.2-1.8 12.3 38.5 48.1 66.5 90.5 67.3-33.1 26-74.9 41.5-120.3 41.5-7.8 0-15.5-.5-23.1-1.4C62.8 432 113.7 448 168.3 448 346.6 448 444 300.3 444 172.2c0-4.2-.1-8.4-.3-12.5C462.6 146 479 129 492 109.5z', 'M524.531,69.836a1.5,1.5,0,0,0-.764-.7A485.065,485.065,0,0,0,404.081,32.03a1.816,1.816,0,0,0-1.923.91,337.461,337.461,0,0,0-14.9,30.6,447.848,447.848,0,0,0-134.426,0,309.541,309.541,0,0,0-15.135-30.6,1.89,1.89,0,0,0-1.924-.91A483.689,483.689,0,0,0,116.085,69.137a1.712,1.712,0,0,0-.788.676C39.068,183.651,18.186,294.69,28.43,404.354a2.016,2.016,0,0,0,.765,1.375A487.666,487.666,0,0,0,176.02,479.918a1.9,1.9,0,0,0,2.063-.676A348.2,348.2,0,0,0,208.12,430.4a1.86,1.86,0,0,0-1.019-2.588,321.173,321.173,0,0,1-45.868-21.853,1.885,1.885,0,0,1-.185-3.126c3.082-2.309,6.166-4.711,9.109-7.137a1.819,1.819,0,0,1,1.9-.256c96.229,43.917,200.41,43.917,295.5,0a1.812,1.812,0,0,1,1.924.233c2.944,2.426,6.027,4.851,9.132,7.16a1.884,1.884,0,0,1-.162,3.126,301.407,301.407,0,0,1-45.89,21.83,1.875,1.875,0,0,0-1,2.611,391.055,391.055,0,0,0,30.014,48.815,1.864,1.864,0,0,0,2.063.7A486.048,486.048,0,0,0,610.7,405.729a1.882,1.882,0,0,0,.765-1.352C623.729,277.594,590.933,167.465,524.531,69.836ZM222.491,337.58c-28.972,0-52.844-26.587-52.844-59.239S193.056,219.1,222.491,219.1c29.665,0,53.306,26.82,52.843,59.239C275.334,310.993,251.924,337.58,222.491,337.58Zm195.38,0c-28.971,0-52.843-26.587-52.843-59.239S388.437,219.1,417.871,219.1c29.667,0,53.307,26.82,52.844,59.239C470.715,310.993,447.538,337.58,417.871,337.58Z', ]
            try:
                websites = driver.find_elements(By.CSS_SELECTOR, 'div.css-1qvd2xe > a')
                for website in websites:
                    if logos[0] == website.find_element(By.CSS_SELECTOR, 'svg > path').get_attribute('d'):
                        data['Website'] = website.get_attribute('href')
                    elif logos[1] == website.find_element(By.CSS_SELECTOR, 'svg > path').get_attribute('d'):
                        data['Twitter'] = website.get_attribute('href')
                    elif logos[2] == website.find_element(By.CSS_SELECTOR, 'svg > path').get_attribute('d'):
                        data['Discord'] = website.get_attribute('href')
            except:
                data['Website'] = ''
                data['Twitter'] = ''
                data['Discord'] = ''

            new_scraped_writer.writerow(data)
            all_scraped_writer.writerow(data)
        else:
            continue

def scroll_to_end():
    last_project = driver.find_elements(By.CSS_SELECTOR, 'div.flex.gap-200.items-center > a')[-1]
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

url = 'https://zealy.io/explore'

try:
    driver.get(url)
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.flex.gap-200.items-center > a')))
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

    projects = [project.get_attribute('href') for project in driver.find_elements(By.CSS_SELECTOR, 'div.flex.gap-200.items-center > a')]
    print('>> Total Projects: ', len(projects))

    print('>> Project Scraping Started')
    get_data(projects, new_scraped_writer, all_scraped_writer)

driver.quit()