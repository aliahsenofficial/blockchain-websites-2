import csv
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

def get_data(projects, new_scraped_writer, all_scraped_writer):
    for i, project in enumerate(tqdm(projects,desc='Project Scraping')):
        if project not in previous_reports:
            data = {}

            try:
                project_response = requests.get(project)
                project_soup = BeautifulSoup(project_response.content, 'lxml')
            except:
                continue

            data['Report'] = project
            try:
                data['Name'] = project_soup.select_one('h1.airdrop__title').text.split('(')[0].strip()
            except:
                continue

            try:
                data['Website'] = project_soup.select_one('a[title="Go to airdrops website for more information"]').get('href')
            except:
                data['Website'] = ''
                
            try:
                data['Twitter'] = project_soup.select_one('a[title="Go to the airdrops Twitter"]').get('href')
            except:
                data['Twitter'] = ''

            try:
                data['Telegram'] = project_soup.select_one('a[title="Join the airdrops Telegram"]').get('href')
            except:
                data['Telegram'] = ''

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

header = ['Name','Report','Website','Telegram','Twitter','Discord']
with open("All_Scraped.csv", mode='a', newline='', encoding='utf-8') as all_scraped_file, open("New_Scraped.csv", mode='a', newline='', encoding='utf-8') as new_scraped_file:
    new_scraped_writer = csv.DictWriter(new_scraped_file, fieldnames=header)
    all_scraped_writer = csv.DictWriter(all_scraped_file, fieldnames=header)

    links = [   'https://airdropalert.com/defi-airdrops', 
                'https://airdropalert.com/nft-airdrops',
                'https://airdropalert.com/new-airdrops',
                'https://airdropalert.com/featured-airdrops',
                'https://airdropalert.com/upcoming-airdrops',
                'https://airdropalert.com/past-airdrops'
            ]

    projects = []
    for link in links:
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'lxml')
        except:
            continue
        
        try:
            total_pages = int(soup.select_one('section.paging-section > div > ul > li:nth-child(12) > a').text)
        except:
            continue
            
        for i in range(2, total_pages+2):
            for project in soup.select('div.card.shadow.text-center > a'):
                projects.append(project.get('href'))
                
            if i < (total_pages+1):
                try:
                    response = requests.get(link + f'?page={i}')
                    soup = BeautifulSoup(response.content, 'lxml')
                except:
                    continue
    print(">> Scrolling Completed")

    print('>> Total Projects: ', len(list(set(projects))))

    print('>> Project Scraping Started')
    get_data(list(set(projects)), new_scraped_writer, all_scraped_writer)