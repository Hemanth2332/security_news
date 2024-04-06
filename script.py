from bs4 import BeautifulSoup
import requests, datetime,socket
from uuid import uuid1
import pandas as pd

titles = []
links = []
topics = []

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
           Chrome/111.0.0.0 Safari/537.36'}

url_with_number = [f"https://www.bleepingcomputer.com/page/{i}/" for i in range(2,6)]
url_list = ["https://www.bleepingcomputer.com/"]
url_list.extend(url_with_number)


for i in url_list:
    req = requests.get(i, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")

    container = soup.find("ul",{"id":"bc-home-news-main-wrap"})
    list_container = container.find_all("li")
    for container in list_container:
    
        news_div = container.find("div",{"class":"bc_latest_news_text"})

        if news_div != None and news_div.a.text != 'Deals':
            title = news_div.h4.text
            titles.append(title)

            link = news_div.h4.a['href']
            links.append(link)
            
            topic_div = news_div.find("div",{"class":"bc_latest_news_category"})
            topic = topic_div.find_all("span")
            if len(topic) == 2:
                txt = ','.join((topic[0].text,topic[1].text))
            else:
                txt = news_div.a.text

            topics.append(txt)


data = {"titles":titles,"topic":topics,"links":links}

try: 
    df = pd.DataFrame(data).set_index('titles')
    df.to_csv(f"bleeping_computer_{datetime.date.today()}_{uuid1()}.csv")
    # print(df)
    print('successfully written as csv file')
except:
    print("failed to write into the csv file")
