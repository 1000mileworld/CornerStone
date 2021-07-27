from bs4 import BeautifulSoup
import urllib3

http = urllib3.PoolManager()

# url = 'http://www.bloomberg.com/quote/SPX:IND'
# response = http.request('GET', url)
# soup = BeautifulSoup(response.data,'html.parser')

# name_box = soup.find('h2', attrs={'class': 'main__heading'})
# name = name_box.text
# print(name)

url = 'https://graphfundamentals.com/'
response = http.request('GET', url)
soup = BeautifulSoup(response.data,'html.parser')
html = soup.find('h1', attrs={'id': 'title-banner'})
print(html)