import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs


user_agent = UserAgent(path='fake_useragent.json').random
headers = {
    'user_agent': user_agent,
    'referer': 'https://shimo.im/login?from=home',
    'x-requested-with': 'XmlHttpRequest'
}

s = requests.Session()
login_url = 'https://shimo.im/lizard-api/auth/password/login'
form_data = {
    'email': '111@qq.com',
    'mobile': '+86undefined',
    'password': '111111'
}

# pre_login = 'https://shimo.im/login?from=home'
# pre_resp = s.get(pre_login, headers=headers)
# print(pre_resp.status_code)
# # print(pre_resp.text)
# print('------------------')
# print(s.cookies)

# response = s.post(login_url, data=form_data, headers=headers, cookies=s.cookies)
response = s.post(login_url, data=form_data, headers=headers)
print(response.status_code)
print(response.text)
print(s.cookies)

# 获取收件箱标题(动态网页，获取为空)
url2 = 'https://shimo.im/inbox'
response2 = s.get(url2, headers=headers)
print(response2.text)
bs_info = bs(response2.text, 'html.parser')
card_info = bs_info.find_all('div', attrs={'class': 'Div-sc-2H_geb eDqDc'})
print(card_info)
