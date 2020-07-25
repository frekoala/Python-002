import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import pandas as pd


def get_movies_info(myurl):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'

    cookie = 'BIDUPSID=0E70B0EE7251C1784CE3E2EEBB75E826; PSTM=1593183705; \
        BAIDUID=0E70B0EE7251C17844E93FD4E3C80424:FG=1; HMACCOUNT=AF056519A25710AD; BDUSS=mdDTEl1RGxYYlFNSVB0SThMV1V-bXFVYn5ZTXNpUVoxTUd5V0ljNGZFWn5jVEpmSVFBQUFBJCQAAAAAAAAAAAEAAADOiaITyrW8-dbQtcS~vMCtAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH~kCl9~5Apfd; HMACCOUNT_BFESS=AF056519A25710AD; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=1; H_PS_PSSID=32294_1431_32361_32045_32116; HMVT=6bcd52f51e9b3dce32bec4a3997715ac|1595609764|'

    header = {'user-agent': user_agent, 'cookie': cookie}
    response = requests.get(myurl, headers=header)
    bs_info = bs(response.text, "html.parser")

    for tags in bs_info.find_all('div',
                                 attrs={'class': 'movie-brief-container'}):
        # 获取电影名称
        file_name = tags.h1.string

        # 电影类型
        movie_type = '/'.join(
            [tag.get_text().strip() for tag in tags.ul.li.find_all('a')])

        # 上映时间
        plan_date = tags.ul.find_all('li', class_="ellipsis")[-1].string

        mylist = [file_name, movie_type, plan_date]

        return mylist


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'

cookie = 'BIDUPSID=0E70B0EE7251C1784CE3E2EEBB75E826; PSTM=1593183705; BAIDUID=0E70B0EE7251C17844E93FD4E3C80424:FG=1; HMACCOUNT=AF056519A25710AD; BDUSS=mdDTEl1RGxYYlFNSVB0SThMV1V-bXFVYn5ZTXNpUVoxTUd5V0ljNGZFWn5jVEpmSVFBQUFBJCQAAAAAAAAAAAEAAADOiaITyrW8-dbQtcS~vMCtAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH~kCl9~5Apfd; HMACCOUNT_BFESS=AF056519A25710AD; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=1; H_PS_PSSID=32294_1431_32361_32045_32116; HMVT=6bcd52f51e9b3dce32bec4a3997715ac|1595609764|'

header = {'user-agent': user_agent, 'cookie': cookie}

myurl = 'https://maoyan.com/board/4'

response = requests.get(myurl, headers=header)

print(response.status_code)

bs_info = bs(response.text, "html.parser")

urls = tuple([
    f'https://maoyan.com{tags.p.a.get("href")}'
    for tags in bs_info.find_all('div', attrs={'class': 'movie-item-info'})
])

print(urls)

# 将电影信息写入csv文件
mydict = {"电影名称": [], "电影类型": [], "上映时间": []}
for page in urls:
    list_tmp = get_movies_info(page)
    assert list_tmp, f"获取电影信息失败,请检查是否验证:{list_tmp}"
    mydict["电影名称"].append(list_tmp[0])
    mydict["电影类型"].append(list_tmp[1])
    mydict["上映时间"].append(list_tmp[2])
    sleep(5)

movie1 = pd.DataFrame(data=mydict)
# 序号设置从1开始
movie1.index += 1
movie1.to_csv('movie1.csv', encoding='gbk', index=True, header=True)
