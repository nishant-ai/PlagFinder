import re
from googlesearch import search
from bs4 import BeautifulSoup
import requests

def get_scrapes(query, num_urls=10, i=85):
    url_list = []
    urls = search(query, num=num_urls, pause=0.2, stop=num_urls)
    for url in urls:
        print(url)
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
    
        with open(f'scraped/scraped_test_{i}.txt', 'w') as f:
            f.write(totalText)
        i+=1    
    return i


j = get_scrapes("Computer Vision", 35)
i = get_scrapes("supervised machine learning", 25, j)
j = get_scrapes("deep learning", 25, i)
print(j)