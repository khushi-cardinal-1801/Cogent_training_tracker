import pandas as pd
from bs4 import BeautifulSoup
import requests
url="https://www.scrapingbee.com/blog/scraper-sites/"
r=requests.get(url)
print(r)
soup=BeautifulSoup(r.text,"html.parser")
# print(soup.prettify())
print(soup.title)
# print(soup.p)
# head=soup("h3",id="2-quotes-to-scrape-quotestoscrapecomhttpquotestoscrapecom")
# print(head)
# print(soup.find_all("a"))

# #extracting image link
# for i in soup.find_all("a"):
#     print(i.get("href"))

#extracting image info
for i in soup.find_all("img"):
    print(i.get("src"))