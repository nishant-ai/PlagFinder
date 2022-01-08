import re
from googlesearch import search
from bs4 import BeautifulSoup
import requests

def get_urls(query, num_urls=10):
    url_list = []
    urls = search(query, num=num_urls, pause=0.5, stop=num_urls)
    for url in urls:
        url_list.append(url)
        response = requests.get(url)

        if response.status_code != 200:
            exit

        soup = BeautifulSoup(response.content, 'html5lib')
        data = soup.find_all('p')

        totalText = ""
        for extraction_p in data:
            extraction_p = re.sub('\[\d{0,}\]', '', extraction_p.text)
            extraction_p = re.sub('\[[a-z]\]', '', extraction_p)
            totalText += extraction_p
    
        with open(f'scraped_dat_{len(url_list)}.txt', 'w') as f:
            f.write(url+"\n")
            f.write(totalText)

get_urls("What is ML", 3)