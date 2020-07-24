import requests
from bs4 import BeautifulSoup as bs


def get_movies_info(myurl):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        header = {'user-agent': user_agent}
        response = requests.get(myurl , headers = header)      
        bs_info = bs(response.text , "html.parser")

        for tags in bs_info.find_all('div',attrs={'class':'movie-brief-container'}):
                #获取电影名称
                file_name = tags.h1.string
                print(file_name)
                #电影类型
                movie_type = '/'.join([tag.get_text().strip() for tag in tags.ul.li.find_all('a')])
                print(movie_type)
                #上映时间
                plan_date =  tags.ul.find_all('li',class_="ellipsis")[-1].string
                print(plan_date)
        
        

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'

header = {'user-agent': user_agent}

myurl = 'https://maoyan.com/board/4'

response = requests.get(myurl , headers = header)


bs_info = bs(response.text , "html.parser")


urls = tuple([f'https://maoyan.com{tags.p.a.get("href")}' for tags in bs_info.find_all('div',attrs={'class':'movie-item-info'})])
print(urls)


from time import sleep
for page in urls:
        get_movies_info(page)
        sleep(5)





