from logging import exception

import requests
import bs4
import pandas as pd
from datetime import datetime
from time import sleep

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

title = ''
price = ''
stock = ''
tLog = ''


def tracker(url, TrackingPrice):
    res = requests.get(url, headers=HEADERS)
    soup = bs4.BeautifulSoup(res.content, features='lxml')
    title = soup.find(id="productTitle").get_text().strip()
    # to prevent script from crashing when there isn't a price for the product
    try:
        price = float(
            soup.find(id='priceblock_ourprice').get_text().replace(".", "").replace("$", "").replace(",", ".").strip())
    except:
        price = ''
    try:
        soup.select('#availability .a-color-state')[0].get_text().strip
        stock = 'out of stock'
    except:
        stock = 'Available'


df = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1cCBIqNC72lzo4YRqSmVXnnyPaTI5UUuuRIodw_UIC5w/export?format=csv")
for i in range(0, len(df["URL"])):
    tracker(df["URL"][i], df["Price"][i])

    log = pd.DataFrame({'date': datetime.now().strftime('%Y-%m-%d %Hh%Mm').replace('h', ':').replace('m', ''),

                    'url': df["URL"],
                    'title': title,
                    'buy_below': df.price[i],
                    'price': price,
                    'stock': stock, }
                   , index=[i])

    try:
        if price < df["Price"][i]:
            print("Buy the "+title+ " from: "+df.URL[i]+" It's price dropped by "+df.Price[i]-price+"\n")
    except:
        pass
    tLog = tLog.append((log))
    sleep(60*60*24)
