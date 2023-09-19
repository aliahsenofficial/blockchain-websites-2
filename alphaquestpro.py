import csv
import json
import requests
import pandas as pd
from tqdm import tqdm

# Getting report links from All_Scraped.csv
def read_reports_from_csv():
    df = pd.read_csv("All_Scraped.csv")
    report_list = df["Twitter"].tolist()
    return report_list
previous_reports = read_reports_from_csv()

session = requests.Session()
headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IlNNSVhJUEdOQzNPRUxTUURQTkxHREVKUkpMWjlQTUJZT1NWWUtUUE8iLCJ0eXAiOiJhdCtqd3QifQ.eyJzdWIiOiIzYTBkOTQ4My0wZmM4LTgyZWYtMmE2MC04MDY4MGU4MDkzMjgiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJoZWxsb3BybyIsImVtYWlsIjoicHJvdG9vbjAwNkBnbWFpbC5jb20iLCJwaG9uZV9udW1iZXJfdmVyaWZpZWQiOiJGYWxzZSIsImVtYWlsX3ZlcmlmaWVkIjoiVHJ1ZSIsInVuaXF1ZV9uYW1lIjoiaGVsbG9wcm8iLCJvaV9wcnN0IjoiQWxwaGFRdWVzdF9BcHAiLCJjbGllbnRfaWQiOiJBbHBoYVF1ZXN0X0FwcCIsIm9pX3Rrbl9pZCI6IjNhMGRiM2E3LTAwOGQtNmY2YS05OTcyLTM4MDZmMjBiYmFmYiIsImF1ZCI6IkFscGhhUXVlc3QiLCJzY29wZSI6IkFscGhhUXVlc3QiLCJqdGkiOiI4YWFlN2I2Ny01MWEyLTQ2NDYtYjU3Yi1lNWU1NjliOThlYzkiLCJleHAiOjE2OTc1MTgyNTIsImlzcyI6Imh0dHBzOi8vbG9jYWxob3N0OjQ0MzYxLyIsImlhdCI6MTY5NDkyNjI1Mn0.ZiRIEbYLJWvdIO-T9DjeyHFU4vMkWGzGoE-gY2ySj1S5O_Souj9qcVBdxGW6opZ_uh7P6L5-P_UWWDLIwSGo0hYbI8kgUfUY5gkzlzaiDoMiVNqHwkd-Ct9Iki-lGODclMJ01BrI0y8B48oV2iGKwYd1XaVf-3OOmgS06i7iOtEXsY5IufjxUzuF19Q6WTfks0Tzfw4XzyXVr_X526mY7C2kmF4N9kQDoMV-dWBjGOVEa_t-jXws525HUp17uDxo30EeRpKkF1oA1fUYDIg_CjfCPUOLewtFMacxDFlGbQT86Kl0B87ZdFFZocaOJV2JmSZpvZP0kmxDL1GXMK77hQ',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

url = 'https://api.alphaquest.io/api/app/twitter?pageNumber=1&pageSize=20000&sortBy=SCORE&timeFrame=ALL&newest=false'
try:
    r = session.get(url, headers=headers)
    json_data = r.text
    json_object = json.loads(json_data)

    items = json_object['items']
except:
    exit()

header = ['Name', 'Report', 'Website','Telegram','Twitter','Discord']
with open("All_Scraped.csv", mode='a', newline='', encoding='utf-8') as all_scraped_file, open("New_Scraped.csv", mode='a', newline='', encoding='utf-8') as new_scraped_file:
    new_scraped_writer = csv.DictWriter(new_scraped_file, fieldnames=header)
    all_scraped_writer = csv.DictWriter(all_scraped_file, fieldnames=header)
    
    for item in tqdm(items, desc='>> Projects Scraping'):
        if item['twitterUrl'] not in previous_reports:
                data = {}
                data['Twitter'] = item['twitterUrl']
                data['Name'] = item['name']
                data['Report'] = ''
                data['Website'] = ''
                data['Telegram'] = ''
                data['Discord'] = ''

                new_scraped_writer.writerow(data)
                all_scraped_writer.writerow(data)