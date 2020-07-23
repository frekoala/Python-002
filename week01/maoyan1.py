import requests
from bs4 import BeautifulSoup as bs

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'

header = {'user-agent':user_agent}
myurl = 'https://maoyan.com/board'

response = requests.get(myurl,headers = header)

bs_info = bs(response.text,"html.parser")

# print(response.text)
# print(f'返回码是：{response.status_code}')

for tags in bs_info.find_all('div',attrs={'class':'movie-item-info'}):
    for atag in tags.find_all('a'):
        #获取所有链接
        print(atag.get('href'))
        #获取电影名字
        print(atag.get('title'))
