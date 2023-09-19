import csv
import json
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

# Getting report links from All_Scraped.csv
def read_reports_from_csv():
    df = pd.read_csv("All_Scraped.csv")
    report_list = df["Report"].tolist()
    return report_list
previous_reports = read_reports_from_csv()

# Getting Twitter links from AlphaQuest.csv
def read_twitters_from_csv():
    df = pd.read_csv("AlphaQuest.csv")
    twitter_list = df["Twitter"].tolist()
    return twitter_list
twitter_reports = read_twitters_from_csv()

session = requests.Session()

categories = ['ai', 'Derivatives', 'dex', 'Friend.tech', 'gambling', 'identity', 'infrastructure', 'layer-1', 'layer-2', 'lending-borrowing', 'liquid-staking-tokens', 'meme', 'metaverse', 'music', 'NFT', 'nft-game', 'Oracle', 'perpetuals', 'Privacy', 'RWA', 'real-yield', 'socialfi', 'telebot', 'wallets', 'yield-farming']
chains = ['aptos', 'arbitrum', 'avalanche', 'Base', 'bnb-chain', 'brc-20', 'Cardano', 'cosmos', 'ethereum', 'fantom', 'injective', 'LayerZero', 'linea', 'mantle', 'MultiversX', 'near-protocol', 'opBNB', 'Optimism', 'Polygon', 'Pulse', 'Scroll', 'Sei', 'Shibarium', 'Solana', 'Starknet', 'sui-network', 'ZkSync']
sortings = ['SCORE', 'DISCOVERED_DATE', 'TWITTER_FOLLOWER', 'TWITTER_CREATED_DATE']
timeframes = ['1D', '3D', '7D', 'ALL']
twitter = []

header = ['Name', 'Report', 'Website','Telegram','Twitter','Discord']
with open("All_Scraped.csv", mode='a', newline='', encoding='utf-8') as all_scraped_file, open("New_Scraped.csv", mode='a', newline='', encoding='utf-8') as new_scraped_file, open("AlphaQuest.csv", mode='a', newline='', encoding='utf-8') as alphaquest_file:
    new_scraped_writer = csv.DictWriter(new_scraped_file, fieldnames=header)
    all_scraped_writer = csv.DictWriter(all_scraped_file, fieldnames=header)
    alphaquest_writer = csv.DictWriter(alphaquest_file, fieldnames=header)

    for category in tqdm(categories, desc='>> Projects Scraping'):
        for chain in chains:
            for sorting in sortings:
                for timeframe in timeframes:
                    url = f'https://api.alphaquest.io/api/app/twitter/for-guest?pageNumber=1&pageSize=20&sortBy={sorting}&timeFrame={timeframe}&newest=false&categories%5B0%5D={category}&chains%5B0%5D={chain}'
                    try:
                        r = session.get(url=url)
                        soup = BeautifulSoup(r.content, 'lxml')
                    except:
                        continue
                    json_data = soup.text
                    json_object = json.loads(json_data)
                    try:
                        items = json_object['items'][3:]
                        for item in items:
                            data = {}
                            data['Name'] = item['name']
                            data['Twitter'] = item['twitterUrl']
                            data['Report'] = ''
                            data['Website'] = ''
                            data['Telegram'] = ''
                            data['Discord'] = ''

                            if data['Twitter'] not in twitter:
                                twitter.append(data['Twitter'])

                                if data['Twitter'] not in twitter_reports:
                                    new_scraped_writer.writerow(data)
                                    all_scraped_writer.writerow(data)
                                    alphaquest_writer.writerow(data)
                    except:
                        continue